
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

import sqlalchemy

from sqlalchemy import Table, func, select, case, cast, BigInteger, literal, text
from sqlalchemy.ext.asyncio import AsyncSession

from logger import logger

from . import settings


try:  
    from database.models import (
        Key as KeyModel,
        Payment as PaymentModel,
        Tariff as PlanModel,
    )
except Exception:  
    KeyModel = PlanModel = PaymentModel = None

async def estimate_auto_renewal_probs(
    session: AsyncSession,
    months_back: int = 3,
    grace_days: int = 0,
    flags: Any = settings,
) -> Dict[str, float]:
    sql = """
    WITH months AS (
      SELECT
        date_trunc('month', (now() AT TIME ZONE 'UTC')) - (s.i * INTERVAL '1 month') AS m_start_utc,
        date_trunc('month', (now() AT TIME ZONE 'UTC')) - ((s.i - 1) * INTERVAL '1 month') AS m_end_utc
      FROM generate_series(1, :months_back) AS s(i)
    ), months_ms AS (
      SELECT
        m_start_utc,
        m_end_utc,
        (EXTRACT(EPOCH FROM m_start_utc)*1000)::bigint AS start_ms,
        (EXTRACT(EPOCH FROM m_end_utc)*1000)::bigint   AS end_ms
      FROM months
    ), plans AS (
      SELECT
        t.id,
        t.group_code,
        COALESCE(t.duration_days, 30) AS duration_days,
        (COALESCE(t.duration_days,30)::bigint * 86400000::bigint) AS dur_ms
      FROM tariffs t
    ), base AS (
      SELECT
        k.client_id,
        k.expiry_time,
        COALESCE(k.is_frozen, false) AS is_frozen,
        p.group_code,
        p.duration_days,
        (k.expiry_time - p.dur_ms) AS prev_ms
      FROM keys k
      JOIN plans p ON p.id = k.tariff_id
    ), filtered AS (
      SELECT
        b.client_id, b.expiry_time, b.is_frozen, b.group_code, b.duration_days,
        b.prev_ms, mm.start_ms, mm.end_ms
      FROM base b
      JOIN months_ms mm
        ON b.prev_ms >= mm.start_ms AND b.prev_ms < mm.end_ms
    ), prepared AS (
      SELECT
        CASE
          WHEN duration_days BETWEEN 25 AND 40  THEN '1m'
          WHEN duration_days BETWEEN 80 AND 100 THEN '3m'
          WHEN duration_days BETWEEN 360 AND 390 THEN '12m'
          ELSE 'other'
        END AS bucket,
        expiry_time, is_frozen, group_code, start_ms, end_ms
      FROM filtered
    )
    SELECT
      bucket,
      COUNT(*)::bigint                                   AS cohort,
      COUNT(*) FILTER (WHERE expiry_time >= end_ms + (:grace_ms)::bigint)::bigint AS renewed
    FROM prepared
    WHERE (:skip_frozen)::boolean IS FALSE OR is_frozen IS FALSE
      AND (
           (:exclude_trials)::boolean IS FALSE
           OR (group_code IS DISTINCT FROM 'trial')
          )
    GROUP BY bucket;
    """
    params = {
        "months_back": int(months_back),
        "grace_ms": int(grace_days) * 86400000,
        "skip_frozen": bool(getattr(flags, "SKIP_FROZEN", False)),
        "exclude_trials": bool(getattr(flags, "EXCLUDE_TRIALS", False)),
    }
    rows = (await session.execute(text(sql), params)).all()

    result: Dict[str, float] = {}
    totals = {"1m": (0,0), "3m": (0,0), "12m": (0,0), "other": (0,0)}
    for bucket, cohort, renewed in rows:
        c = int(cohort or 0)
        r = int(renewed or 0)
        if bucket not in totals:
            totals[bucket] = (0,0)
        C,R = totals[bucket]
        totals[bucket] = (C + c, R + r)
    for b, (C, R) in totals.items():
        if C > 0:
            p = (R + 1) / (C + 2)
        else:
            p = 1.0 
        result[b] = max(0.0, min(1.0, float(p)))
    return result


async def get_recognized_revenue_accrual(
    session: AsyncSession,
    dt_start: datetime,
    dt_now: datetime,
    flags: Any,
) -> dict[str, Any]:
    key_model, plan_model, _ = await _get_models(session)

    start_ms = int(dt_start.timestamp() * 1000)
    now_ms   = int(dt_now.timestamp()   * 1000)

    dur_ms = (func.coalesce(
        (plan_model.c.duration_days if isinstance(plan_model, Table) else plan_model.duration_days),
        30
    ).cast(BigInteger) * literal(86400000, type_=BigInteger))

    prev_expiry_ms = (
        (key_model.c.expiry_time if isinstance(key_model, Table) else key_model.expiry_time)
        - dur_ms
    )

    cols = {
        "id": (plan_model.c.id if isinstance(plan_model, Table) else plan_model.id),
        "name": (plan_model.c.name if isinstance(plan_model, Table) else plan_model.name),
        "group_code": (plan_model.c.group_code if isinstance(plan_model, Table) else plan_model.group_code),
        "price": (plan_model.c.price_rub if isinstance(plan_model, Table) else plan_model.price_rub),
        "dur": (plan_model.c.duration_days if isinstance(plan_model, Table) else plan_model.duration_days),
        "client": (key_model.c.client_id if isinstance(key_model, Table) else key_model.client_id),
        "frozen": (key_model.c.is_frozen if isinstance(key_model, Table) else key_model.is_frozen),
    }

    stmt = (
        select(
            cols["id"], cols["name"], cols["group_code"],
            func.count(cols["client"]),
            cols["price"], cols["dur"],
        )
        .join(plan_model, (key_model.c.tariff_id if isinstance(key_model, Table) else key_model.tariff_id) == cols["id"])
        .where(prev_expiry_ms >= start_ms, prev_expiry_ms < now_ms)
    )

    if getattr(flags, "SKIP_FROZEN", False):
        stmt = stmt.where(cols["frozen"].is_(False))

    if getattr(flags, "EXCLUDE_TRIALS", False):
        price_col = cols["price"]
        gc_col    = cols["group_code"]
        stmt = stmt.where(~((gc_col == "trial") | (func.coalesce(price_col, 0) == 0)))

    stmt = stmt.group_by(cols["id"], cols["name"], cols["group_code"], cols["price"], cols["dur"])
    res = await session.execute(stmt)

    total = 0.0
    by_plans: dict[str, dict[str, Any]] = {}
    for _id, name, gcode, cnt, price, dur in res:
        cnt = int(cnt or 0); price = float(price or 0.0)
        s = cnt * price
        total += s
        by_plans[str(name)] = {
            "count": cnt,
            "price": price,
            "sum": s,
            "period_months": round((dur or 0) / 30) if dur else None,
            "group_code": gcode,
        }
    return {"total": total, "by_plans": by_plans}

async def get_month_bounds(now_utc: datetime) -> tuple[datetime, datetime]:
    start = now_utc.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if start.month == 12:
        end = start.replace(year=start.year + 1, month=1)
    else:
        end = start.replace(month=start.month + 1)
    return start, end


async def _reflect_tables(session: AsyncSession) -> tuple[Table, Table, Table]: 
    engine = session.bind
    insp = sqlalchemy.inspect(engine)
    metadata = sqlalchemy.MetaData()

    tables_cfg = settings.DISCOVERY_FALLBACKS["tables"]
    names = {k: tables_cfg.get(k) for k in ("keys", "plans", "payments")}

    def resolve(name_hint: str | None, candidates: list[str]) -> str:
        if name_hint and name_hint in candidates:
            return name_hint
        for cand in candidates:
            if name_hint and cand.startswith(name_hint):
                return cand
        for cand in candidates:
            if name_hint is None and any(x in cand for x in ("key", "plan", "payment")):
                return cand
        raise LookupError(f"Table for {name_hint or 'unknown'} not found")

    table_names = insp.get_table_names()
    key_table = Table(resolve(names["keys"], table_names), metadata, autoload_with=engine)
    plan_table = Table(resolve(names["plans"], table_names), metadata, autoload_with=engine)
    payment_table = Table(resolve(names["payments"], table_names), metadata, autoload_with=engine)
    return key_table, plan_table, payment_table


async def _get_models(session: AsyncSession):
    global KeyModel, PlanModel, PaymentModel
    if KeyModel and PlanModel and PaymentModel:
        return KeyModel, PlanModel, PaymentModel
    try:
        KeyModel, PlanModel, PaymentModel = await _reflect_tables(session)
        logger.info("[RF] Using reflected tables for discovery")
        return KeyModel, PlanModel, PaymentModel
    except Exception as exc: 
        logger.error(f"[RF] Discovery failed: {exc}")
        raise

def _bucket_plan(group_code: str | None, duration_days: int | None) -> str:
    if group_code in ("1m", "3m", "12m"):
        return group_code
    months = round((duration_days or 0) / 30) if duration_days else 0
    if months == 1:
        return "1m"
    if months == 3:
        return "3m"
    if 10 <= months <= 13:
        return "12m"
    return "other"




async def get_expiring_by_plan(
    session: AsyncSession,
    dt_start: datetime,
    dt_end: datetime,
    flags: Any,
) -> dict[str, dict[str, Any]]:
    key_model, plan_model, _ = await _get_models(session)

    start_ms = int(dt_start.timestamp() * 1000)
    end_ms = int(dt_end.timestamp() * 1000)

    stmt = (
        select(
            (plan_model.c.id if isinstance(plan_model, Table) else plan_model.id),
            (plan_model.c.name if isinstance(plan_model, Table) else plan_model.name),
            (plan_model.c.group_code if isinstance(plan_model, Table) else plan_model.group_code),
            func.count((key_model.c.client_id if isinstance(key_model, Table) else key_model.client_id)),
            (plan_model.c.price_rub if isinstance(plan_model, Table) else plan_model.price_rub),
            (plan_model.c.duration_days if isinstance(plan_model, Table) else plan_model.duration_days),
        )
        .join(
            plan_model,
            (key_model.c.tariff_id if isinstance(key_model, Table) else key_model.tariff_id)
            == (plan_model.c.id if isinstance(plan_model, Table) else plan_model.id),
        )
    )

    expiry_col = (
        key_model.c.expiry_time if isinstance(key_model, Table) else key_model.expiry_time
    )
    stmt = stmt.where(expiry_col >= start_ms, expiry_col < end_ms)

    if flags.SKIP_FROZEN and (
        hasattr(key_model, "is_frozen")
        or (isinstance(key_model, Table) and "is_frozen" in key_model.c)
    ):
        frozen_col = (
            key_model.c.is_frozen if isinstance(key_model, Table) else key_model.is_frozen
        )
        stmt = stmt.where(frozen_col.is_(False))

    if getattr(flags, "EXCLUDE_TRIALS", False):
        price_col = (plan_model.c.price_rub if isinstance(plan_model, Table) else plan_model.price_rub)
        gc_col = (plan_model.c.group_code if isinstance(plan_model, Table) else plan_model.group_code)
        stmt = stmt.where(~( (gc_col == "trial") | (func.coalesce(price_col, 0) == 0) ))

    stmt = stmt.group_by(
        (plan_model.c.id if isinstance(plan_model, Table) else plan_model.id),
        (plan_model.c.name if isinstance(plan_model, Table) else plan_model.name),
        (plan_model.c.group_code if isinstance(plan_model, Table) else plan_model.group_code),
        (plan_model.c.price_rub if isinstance(plan_model, Table) else plan_model.price_rub),
        (plan_model.c.duration_days if isinstance(plan_model, Table) else plan_model.duration_days),
    )

    result = await session.execute(stmt)
    data: dict[str, dict[str, Any]] = {}
    for _id, name, gcode, count, price, duration in result:
        bucket = _bucket_plan(gcode, duration)
        data[str(name)] = {
            "count": int(count or 0),
            "price": float(price or 0.0),
            "period_months": round((duration or 0) / 30) if duration else None,
            "group_code": gcode,
            "bucket": bucket,
        }
    return data

async def get_baseline_expiring_by_plan(
    session: AsyncSession,
    dt_start: datetime,
    dt_end: datetime,
    flags: Any,
) -> dict[str, dict[str, Any]]:
    key_model, plan_model, _ = await _get_models(session)

    start_ms = int(dt_start.timestamp() * 1000)
    end_ms = int(dt_end.timestamp() * 1000)

    current = await get_expiring_by_plan(session, dt_start, dt_end, flags)

    expiry_col = key_model.c.expiry_time if isinstance(key_model, Table) else key_model.expiry_time
    dur_col = plan_model.c.duration_days if isinstance(plan_model, Table) else plan_model.duration_days
    prev_expiry_ms = (
        expiry_col
        - (
            cast(func.coalesce(dur_col, 0), BigInteger)
            * literal(86400000, BigInteger)
        )
    )

    stmt_prev = (
        select(
            (plan_model.c.id if isinstance(plan_model, Table) else plan_model.id),
            (plan_model.c.name if isinstance(plan_model, Table) else plan_model.name),
            (plan_model.c.group_code if isinstance(plan_model, Table) else plan_model.group_code),
            func.count((key_model.c.client_id if isinstance(key_model, Table) else key_model.client_id)),
            (plan_model.c.price_rub if isinstance(plan_model, Table) else plan_model.price_rub),
            (plan_model.c.duration_days if isinstance(plan_model, Table) else plan_model.duration_days),
        )
        .join(
            plan_model,
            (key_model.c.tariff_id if isinstance(key_model, Table) else key_model.tariff_id)
            == (plan_model.c.id if isinstance(plan_model, Table) else plan_model.id),
        )
        .where(prev_expiry_ms >= start_ms, prev_expiry_ms < end_ms)
    )

    if flags.SKIP_FROZEN and (
        hasattr(key_model, "is_frozen")
        or (isinstance(key_model, Table) and "is_frozen" in key_model.c)
    ):
        frozen_col = key_model.c.is_frozen if isinstance(key_model, Table) else key_model.is_frozen
        stmt_prev = stmt_prev.where(frozen_col.is_(False))

    if getattr(flags, "EXCLUDE_TRIALS", False):
        price_col = plan_model.c.price_rub if isinstance(plan_model, Table) else plan_model.price_rub
        gc_col = plan_model.c.group_code if isinstance(plan_model, Table) else plan_model.group_code
        stmt_prev = stmt_prev.where(~((gc_col == "trial") | (func.coalesce(price_col, 0) == 0)))

    stmt_prev = stmt_prev.group_by(
        (plan_model.c.id if isinstance(plan_model, Table) else plan_model.id),
        (plan_model.c.name if isinstance(plan_model, Table) else plan_model.name),
        (plan_model.c.group_code if isinstance(plan_model, Table) else plan_model.group_code),
        (plan_model.c.price_rub if isinstance(plan_model, Table) else plan_model.price_rub),
        (plan_model.c.duration_days if isinstance(plan_model, Table) else plan_model.duration_days),
    )

    result_prev = await session.execute(stmt_prev)
    prev_data: dict[str, dict[str, Any]] = {}
    for _id, name, gcode, count, price, duration in result_prev:
        bucket = _bucket_plan(gcode, duration)
        entry = prev_data.get(str(name))
        if entry is None:
            prev_data[str(name)] = {
                "count": int(count or 0),
                "price": float(price or 0.0),
                "period_months": round((duration or 0) / 30) if duration else None,
                "group_code": gcode,
                "bucket": bucket,
            }
        else:
            entry["count"] += int(count or 0)
            if price and float(price) != entry.get("price", 0.0):
                entry["price"] = float(price)

    merged: dict[str, dict[str, Any]] = {}
    for src in (current, prev_data):
        for name, info in src.items():
            if name not in merged:
                merged[name] = dict(info)
            else:
                merged[name]["count"] += int(info.get("count", 0))
                if "price" in info and info["price"]:
                    merged[name]["price"] = float(info["price"])
    return merged


async def get_received(
    session: AsyncSession,
    dt_start: datetime,
    dt_end: datetime,
    flags: Any,
) -> dict[str, float]:
    _, _, payment_model = await _get_models(session)

    paid_col = (
        payment_model.c.amount if isinstance(payment_model, Table) else payment_model.amount
    )
    status_col = (
        payment_model.c.status if isinstance(payment_model, Table) else payment_model.status
    )
    created_col = (
        payment_model.c.created_at if isinstance(payment_model, Table) else payment_model.created_at
    )

    stmt = select(func.coalesce(func.sum(paid_col), 0)).where(
        created_col >= dt_start, created_col < dt_end, status_col == "success"
    )
    result = await session.execute(stmt)
    paid = float(result.scalar() or 0.0)
    return {"paid": paid, "refunds": 0.0, "net": paid}


def compute_forecast(
    expiring: dict[str, dict[str, Any]],
    received_dict: dict[str, float],
    probs: dict[str, float] | None = None,
    global_prob: float | None = None,
) -> dict[str, Any]:
    overrides = probs or {}
    forecast = 0.0
    by_plans: dict[str, dict[str, Any]] = {}

    for code, info in expiring.items():
        price = info.get("price", 0.0)
        count = info.get("count", 0)
        prob = (
            overrides.get(code)
            or overrides.get(info.get("group_code"))
            or overrides.get(info.get("bucket"))
            or (global_prob if global_prob is not None else 1.0)
        )
        expected = price * count * prob
        forecast += expected
        by_plans[code] = {**info, "expected": expected, "prob": prob}

    received = received_dict.get("net", 0.0)
    to_earn = max(0.0, forecast - received)
    return {
        "forecast": forecast,
        "received": received,
        "to_earn": to_earn,
        "by_plans": by_plans,
    }



async def calc_kpis(
    session: AsyncSession,
    dt_start: datetime,
    dt_end: datetime,
    flags: Any,
    by_plans: dict[str, dict[str, Any]],
    probs: dict[str, float] | None = None,
    global_prob: float | None = None,
) -> dict[str, Any]:
    _, _, Payment = await _get_models(session)
    paid_col = Payment.c.amount if isinstance(Payment, Table) else Payment.amount
    status_col = Payment.c.status if isinstance(Payment, Table) else Payment.status
    created_col = Payment.c.created_at if isinstance(Payment, Table) else Payment.created_at

    q_pay = (
        select(
            func.coalesce(func.sum(case((status_col == "success", paid_col), else_=0.0)), 0.0),
            func.count().filter(status_col == "success"),
        )
        .where(created_col >= dt_start, created_col < dt_end)
    )
    paid_sum, paid_count = (await session.execute(q_pay)).one()
    paid_sum = float(paid_sum or 0.0)
    paid_count = int(paid_count or 0)
    avg_check = (paid_sum / paid_count) if paid_count > 0 else 0.0

    Key, _, _ = await _get_models(session)
    k_expiry = Key.c.expiry_time if isinstance(Key, Table) else Key.expiry_time  
    k_created = Key.c.created_at if isinstance(Key, Table) else Key.created_at   
    k_tg = Key.c.tg_id if isinstance(Key, Table) else Key.tg_id
    cond_frozen = True
    if hasattr(Key, "is_frozen") or (isinstance(Key, Table) and "is_frozen" in Key.c):
        k_frozen = Key.c.is_frozen if isinstance(Key, Table) else Key.is_frozen
        cond_frozen = k_frozen.is_(False) if flags.SKIP_FROZEN else True
    q_active = (
        select(func.count(func.distinct(k_tg)))
        .where(
            (k_created <= int(dt_end.timestamp() * 1000)),
            (k_expiry >= int(dt_start.timestamp() * 1000)),
            cond_frozen,
        )
    )
    active_users = int((await session.execute(q_active)).scalar() or 0)
    arpu = (paid_sum / active_users) if active_users > 0 else 0.0

    retention_block = await _calc_retention_churn(
        session, dt_start, dt_end, flags, probs=probs, global_prob=global_prob
    )

    return {
        "avg_check": avg_check,
        "paid_count": paid_count,
        "active_users": active_users,
        "arpu": arpu,
        "mrr_active": await _calc_mrr_active_base(session, flags),  
        **retention_block,
    }


async def _calc_mrr_active_base(session: AsyncSession, flags: Any) -> float:
    Key, Plan, _ = await _get_models(session)

    now_ms = int(datetime.utcnow().timestamp() * 1000)

    expiry_col = Key.c.expiry_time if isinstance(Key, Table) else Key.expiry_time
    tg_col = Key.c.client_id if isinstance(Key, Table) else Key.client_id

    stmt = select(
        Plan.c.group_code if isinstance(Plan, Table) else Plan.group_code,
        func.count(tg_col),
        Plan.c.price_rub if isinstance(Plan, Table) else Plan.price_rub,
        Plan.c.duration_days if isinstance(Plan, Table) else Plan.duration_days,
    ).join(
        Plan,
        (Key.c.tariff_id if isinstance(Key, Table) else Key.tariff_id)
        == (Plan.c.id if isinstance(Plan, Table) else Plan.id),
    ).where(
        expiry_col > now_ms
    )

    if flags.SKIP_FROZEN and (
        hasattr(Key, "is_frozen")
        or (isinstance(Key, Table) and "is_frozen" in Key.c)
    ):
        frozen_col = Key.c.is_frozen if isinstance(Key, Table) else Key.is_frozen
        stmt = stmt.where(frozen_col.is_(False))

    if getattr(flags, "EXCLUDE_TRIALS", False):
        gc_col = Plan.c.group_code if isinstance(Plan, Table) else Plan.group_code
        price_col = Plan.c.price_rub if isinstance(Plan, Table) else Plan.price_rub
        stmt = stmt.where(~((gc_col == "trial") | (func.coalesce(price_col, 0) == 0)))

    stmt = stmt.group_by(
        (Plan.c.group_code if isinstance(Plan, Table) else Plan.group_code),
        (Plan.c.price_rub if isinstance(Plan, Table) else Plan.price_rub),
        (Plan.c.duration_days if isinstance(Plan, Table) else Plan.duration_days),
    )

    res = await session.execute(stmt)
    mrr_active = 0.0
    for code, count, price, duration in res:
        months = round((duration or 0) / 30) if duration else 1
        months = months if months and months > 0 else 1
        mrr_active += float(price or 0.0) / months * int(count or 0)
    return mrr_active



async def _calc_retention_churn(
    session: AsyncSession,
    dt_start: datetime,
    dt_end: datetime,
    flags: Any,
    probs: dict[str, float] | None = None,
    global_prob: float | None = None,
) -> dict[str, Any]:
    Key, Plan, Payment = await _get_models(session)

    start_ms = int(dt_start.timestamp() * 1000)
    end_ms = int(dt_end.timestamp() * 1000)
    now_ms = int(datetime.utcnow().timestamp() * 1000)

    expiry_col = Key.c.expiry_time if isinstance(Key, Table) else Key.expiry_time
    dur_col = Plan.c.duration_days if isinstance(Plan, Table) else Plan.duration_days
    prev_expiry_ms = (
        expiry_col
        - (cast(func.coalesce(dur_col, 0), BigInteger) * literal(86400000, BigInteger))
    )

    q_candidates = (
        select(
            expiry_col.label("expiry_ms"),
            (Plan.c.group_code if isinstance(Plan, Table) else Plan.group_code).label("gcode"),
            (Plan.c.duration_days if isinstance(Plan, Table) else Plan.duration_days).label("days"),
            (Plan.c.price_rub if isinstance(Plan, Table) else Plan.price_rub).label("price"),
            (Key.c.tg_id if isinstance(Key, Table) else Key.tg_id).label("tg_id"),
        )
        .join(
            Plan,
            (Key.c.tariff_id if isinstance(Key, Table) else Key.tariff_id)
            == (Plan.c.id if isinstance(Plan, Table) else Plan.id),
        )
        .where(prev_expiry_ms >= start_ms, prev_expiry_ms < end_ms)
    )

    if flags.SKIP_FROZEN and (
        hasattr(Key, "is_frozen")
        or (isinstance(Key, Table) and "is_frozen" in Key.c)
    ):
        frozen_col = Key.c.is_frozen if isinstance(Key, Table) else Key.is_frozen
        q_candidates = q_candidates.where(frozen_col.is_(False))

    if getattr(flags, "EXCLUDE_TRIALS", False):
        gc_col = Plan.c.group_code if isinstance(Plan, Table) else Plan.group_code
        price_col = Plan.c.price_rub if isinstance(Plan, Table) else Plan.price_rub
        q_candidates = q_candidates.where(~((gc_col == "trial") | (func.coalesce(price_col, 0) == 0)))

    cand_rows = (await session.execute(q_candidates)).all()
    candidates_total = len(cand_rows)
    cand_tg_ids = {tg for *_rest, tg in cand_rows}  

    _, _, Payment = await _get_models(session)
    status_col = Payment.c.status if isinstance(Payment, Table) else Payment.status
    created_col = Payment.c.created_at if isinstance(Payment, Table) else Payment.created_at
    pay_tg_in_month = await session.execute(
        select((Payment.c.tg_id if isinstance(Payment, Table) else Payment.tg_id))
        .where(created_col >= dt_start, created_col < dt_end, status_col == "success")
        .group_by((Payment.c.tg_id if isinstance(Payment, Table) else Payment.tg_id))
    )
    paid_in_month_tg = {tg for (tg,) in pay_tg_in_month.all()}

    plan_map_rows = await session.execute(
        select(
            (Plan.c.price_rub if isinstance(Plan, Table) else Plan.price_rub),
            (Plan.c.duration_days if isinstance(Plan, Table) else Plan.duration_days),
            (Plan.c.group_code if isinstance(Plan, Table) else Plan.group_code),
        )
    )
    price_to_plan = {}
    for price_rub, dd, gcode in plan_map_rows.all():
        price_to_plan.setdefault(int(price_rub or 0), (int(dd or 30), gcode))

    p = Payment
    base = select(
        (p.c.tg_id if isinstance(p, Table) else p.tg_id).label("tg_id"),
        (p.c.amount if isinstance(p, Table) else p.amount).label("amount"),
        (p.c.created_at if isinstance(p, Table) else p.created_at).label("paid_at"),
        func.row_number().over(
            partition_by=(p.c.tg_id if isinstance(p, Table) else p.tg_id),
            order_by=(p.c.created_at if isinstance(p, Table) else p.created_at).desc(),
        ).label("rn"),
    ).where(created_col < dt_end, status_col == "success")

    subq = base.subquery("last_payments_ranked")
    last_pays = await session.execute(
        select(subq.c.tg_id, subq.c.amount, subq.c.paid_at).where(subq.c.rn == 1)
    )
    fallback_rows = []
    for tg_id, amount, paid_at in last_pays.all():
        if tg_id in cand_tg_ids:
            continue  
        price_key = int(round(float(amount or 0.0)))
        plan_info = price_to_plan.get(price_key)
        if not plan_info:
            continue  
        dd, gcode = plan_info
        prev_expiry_dt = paid_at + timedelta(days=dd or 30)
        if dt_start <= prev_expiry_dt < dt_end:
            fallback_rows.append((None, gcode, dd, price_key, tg_id))

    cand_rows.extend(fallback_rows)
    candidates_total = len(cand_rows)
    if candidates_total == 0:
        return {
            "retention_rate": None,
            "churn_rate": None,
            "renewed_count": 0,
            "not_renewed_yet": 0,
            "predicted_churn": 0.0,
        }

    paid_col = Payment.c.amount if isinstance(Payment, Table) else Payment.amount
    status_col = Payment.c.status if isinstance(Payment, Table) else Payment.status
    created_col = Payment.c.created_at if isinstance(Payment, Table) else Payment.created_at
    p_rows = await session.execute(
        select((Payment.c.tg_id if isinstance(Payment, Table) else Payment.tg_id))
        .where(created_col >= dt_start, created_col < dt_end, status_col == "success")
        .group_by((Payment.c.tg_id if isinstance(Payment, Table) else Payment.tg_id))
    )
    paid_tg_set = {tg for (tg,) in p_rows.all()}

    renewed = 0
    not_renewed = 0
    bucket_counts: dict[str, int] = {}
    for expiry_ms, gcode, days, price, tg_id in cand_rows:
        if expiry_ms is not None:
            if (expiry_ms or 0) >= end_ms:
                renewed += 1
            else:
                not_renewed += 1
                bucket = _bucket_plan(gcode, days)
                bucket_counts[bucket] = bucket_counts.get(bucket, 0) + 1
            continue
        if tg_id in paid_in_month_tg:
            renewed += 1
        else:
            not_renewed += 1
            bucket = _bucket_plan(gcode, days)
            bucket_counts[bucket] = bucket_counts.get(bucket, 0) + 1

    retention_rate = renewed / candidates_total
    churn_rate = not_renewed / candidates_total

    p_map = probs or {}
    default_p = global_prob if global_prob is not None else 1.0
    predicted_churn = 0.0
    for bucket, cnt in bucket_counts.items():
        p = p_map.get(bucket, default_p)
        predicted_churn += (1.0 - float(p or 0.0)) * cnt

    return {
        "retention_rate": retention_rate,
        "churn_rate": churn_rate,
        "renewed_count": renewed,
        "not_renewed_yet": not_renewed,
        "predicted_churn": predicted_churn,
    }