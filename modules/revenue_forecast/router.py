from __future__ import annotations

from datetime import datetime
import pytz
from typing import Any

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from hooks.hooks import register_hook
from logger import logger

from . import db, settings, texts


router = Router()


async def _build_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(text=texts.BTN_REFRESH, callback_data="rf|refresh")
    builder.button(text=texts.BTN_BACK, callback_data=settings.STATS_ANCHOR_CALLBACK)
    builder.adjust(1, 1)
    return builder


async def _render_summary(callback: CallbackQuery, session: AsyncSession):
    moscow_tz = pytz.timezone("Europe/Moscow")
    now_msk = datetime.now(moscow_tz)
    now = now_msk.astimezone(pytz.UTC).replace(tzinfo=None)
    dt_start, dt_end = await db.get_month_bounds(now)
    expiring = await db.get_expiring_by_plan(session, dt_start, dt_end, settings)
    baseline_expiring = await db.get_baseline_expiring_by_plan(session, dt_start, dt_end, settings)
    received = await db.get_received(session, dt_start, dt_end, settings)
    probs_to_use = settings.PLAN_PROB_OVERRIDES or {}
    global_p = settings.RENEWAL_PROBABILITY
    if (not probs_to_use) and (global_p is None):
        probs_to_use = await db.estimate_auto_renewal_probs(session, months_back=3, grace_days=0, flags=settings)
        global_p = None
    
    data = db.compute_forecast(
        expiring,
        received,
        probs=probs_to_use,
        global_prob=global_p,
    )
    baseline = db.compute_forecast(
        baseline_expiring,
        {"net": 0.0, "paid": 0.0, "refunds": 0.0},
        probs=probs_to_use,
        global_prob=global_p,
    )
    data["plan_baseline"] = baseline.get("forecast", 0.0)
    data["by_plans_baseline"] = baseline_expiring  
    data["by_plans_current"]  = expiring           
    mode = getattr(settings, "COMPLETION_MODE", "cash")
    plan_sum = float(data["plan_baseline"])
    recognized_total = None
    if plan_sum > 0:
        if mode == "plan_vs_forecast":
            forecast_sum = float(data.get("forecast", 0.0))
            data["plan_completion_pct"] = max(0.0, min(100.0, (plan_sum - forecast_sum) / plan_sum * 100.0))
        elif mode == "accrual":
            recognized = await db.get_recognized_revenue_accrual(session, dt_start, now, settings)
            recognized_total = float(recognized.get("total", 0.0))
            data["plan_completion_pct"] = (recognized_total / plan_sum) * 100.0
        else:  
            fact_sum = float(data.get("received", 0.0))
            data["plan_completion_pct"] = (fact_sum / plan_sum) * 100.0
    else:
        data["plan_completion_pct"] = None

    if plan_sum > 0:
        if mode == "plan_vs_forecast":
            data["plan_gap"] = float(data.get("forecast", 0.0))
        elif mode == "accrual":
            if recognized_total is None:
                rec = await db.get_recognized_revenue_accrual(session, dt_start, now, settings)
                recognized_total = float(rec.get("total", 0.0))
            data["plan_gap"] = max(0.0, plan_sum - recognized_total)
        else:  
            fact = float(data.get("received", 0.0))
            data["plan_gap"] = max(0.0, plan_sum - fact)
    else:
        data["plan_gap"] = 0.0
    kpis = await db.calc_kpis(
        session, dt_start, dt_end, settings,
        data.get("by_plans", {}),
        probs=probs_to_use,
        global_prob=global_p,
    )
    data["metrics"] = kpis
    data["updated_human_msk"] = now_msk.strftime("%d.%m.%y %H:%M:%S")
    text = texts.render_summary(data)
    kb = await _build_keyboard()
    await callback.message.edit_text(text=text, reply_markup=kb.as_markup())


@router.callback_query(F.data == "rf|open")
async def open_forecast(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    try:
        await _render_summary(callback, session)
    except Exception as exc:  
        await state.clear()
        logger.error(f"[RF] open_forecast error: {exc}")
        await callback.answer(texts.ERROR, show_alert=True)


@router.callback_query(F.data == "rf|refresh")
async def refresh_forecast(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    try:
        await _render_summary(callback, session)
    except Exception as exc:  
        await state.clear()
        logger.error(f"[RF] refresh_forecast error: {exc}")
        await callback.answer(texts.ERROR, show_alert=True)


async def statistics_menu_hook(**kwargs: Any):
    return {
        "after": settings.STATS_ANCHOR_CALLBACK,
        "button": InlineKeyboardButton(text=texts.BTN_ADMIN_FORECAST, callback_data="rf|admin"),
    }


register_hook("statistics_menu", statistics_menu_hook)

if settings.SHOW_IN_ADMIN_PANEL:
    async def admin_panel_hook(**kwargs: Any):
        return {
            "button": InlineKeyboardButton(text=texts.BTN_ADMIN_FORECAST, callback_data="rf|admin"),
        }

    register_hook("admin_panel", admin_panel_hook)


@router.callback_query(F.data == "rf|admin")
async def admin_open(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    try:
        await _render_summary(callback, session)
    except Exception as exc: 
        await state.clear()
        logger.error(f"[RF] admin_open error: {exc}")
        await callback.answer(texts.ERROR, show_alert=True)
