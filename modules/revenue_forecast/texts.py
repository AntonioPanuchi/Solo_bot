"""User-visible texts for revenue forecast module."""

BTN_FINANCE = "Финансы"
BTN_REFRESH = "🔄 Обновить"
BTN_BACK = "⬅️ Назад"

TITLE = "<b>📈 Финансовая статистика</b>"
CUR_MONTH = "📅 <b>Текущий месяц</b>"
DETAILS = "📊 <b>Детали</b>"
DETAILS_PLAN = "📊 <b>План на начало месяца — детализация</b>"
DETAILS_REMAIN = "📊 <b>Остаток на сегодня — детализация</b>"
RETENTION_TITLE = "🧲 <b>Удержание и отток</b>"

ADMIN_TITLE = "<b>📈 Прогноз выручки</b>"
BTN_ADMIN_FORECAST = "💰 Прогноз выручки"
ADMIN_META = "Диагностика"
BTN_ADMIN_SETTINGS = "⚙️ Настройки"
BTN_EXPORT = "📤 Экспорт CSV"
BTN_RECALC = "🔄 Пересчитать"

ERROR = "Статистика временно недоступна"


def _render_details(by_plans: dict) -> list[str]:
    lines = [DETAILS]
    items = []
    for name, d in (by_plans or {}).items():
        items.append((
            int(d.get("period_months") or 999),
            str(name or "").lower(),
            str(name or ""),
            int(d.get("count", 0)),
            float(d.get("price", 0.0)),
        ))
    items.sort(key=lambda x: (x[0], x[1]))
    if not items:
        lines.append("└ —")
        return lines
    for i, (_m, _key, name, cnt, price) in enumerate(items):
        prefix = "└" if i == len(items) - 1 else "├"
        total = float(cnt) * float(price)
        lines.append(f"{prefix} {name}: <b>{cnt} × {price:.2f} ₽ = {total:.2f} ₽</b>")
    return lines


def _render_details_with_heading(by_plans: dict, heading: str) -> list[str]:
    lines: list[str] = []
    if heading:
        lines.append(heading)
    items = []
    for name, d in (by_plans or {}).items():
        items.append((
            int(d.get("period_months") or 999),
            str(name or "").lower(),
            str(name or ""),
            int(d.get("count", 0)),
            float(d.get("price", 0.0)),
        ))
    items.sort(key=lambda x: (x[0], x[1]))
    if not items:
        lines.append("└ —")
        return lines
    for i, (_m, _key, name, cnt, price) in enumerate(items):
        prefix = "└" if i == len(items) - 1 else "├"
        total = float(cnt) * float(price)
        lines.append(f"{prefix} {name}: <b>{cnt} × {price:.2f} ₽ = {total:.2f} ₽</b>")
    return lines


def render_summary(data: dict) -> str:
    by_plans = data.get("by_plans", {}) 
    bp_baseline = data.get("by_plans_baseline", {})  
    bp_current  = data.get("by_plans_current", {})   
    top_lines = [
        f"└ 💰 Прогноз: <b>{data.get('forecast', 0.0):.2f} ₽</b>",
        f"└ 🎯 План на начало месяца: <b>{data.get('plan_baseline', 0.0):.2f} ₽</b>",
        f"└ ✅ Факт: <b>{data.get('received', 0.0):.2f} ₽</b>",
        f"└ ⏳ Осталось: <b>{data.get('to_earn', 0.0):.2f} ₽</b>",
        (
            f"└ 📏 Выполнено: <b>{data.get('plan_completion_pct'):.1f}%</b>"
            if data.get('plan_completion_pct') is not None
            else "└ 📏 Выполнено: <b>—</b>"
        ),
        f"└ 🎯 Осталось до плана: <b>{data.get('plan_gap', 0.0):.2f} ₽</b>",
    ]
    plan_details_lines = _render_details_with_heading(bp_baseline, "")
    remain_details_lines = _render_details_with_heading(bp_current, "")
    metrics = data.get("metrics") or {}
    metrics_lines = [
        f"├ 💳 Средний чек: <b>{metrics.get('avg_check', 0.0):.2f} ₽</b>",
        f"├ 📦 Оплат за месяц: <b>{metrics.get('paid_count', 0)}</b>",
        f"├ 👥 Активные пользователи: <b>{metrics.get('active_users', 0)}</b>",
        f"├ 📊 ARPU: <b>{metrics.get('arpu', 0.0):.2f} ₽</b>",
        f"└ 🔁 MRR (активная база): <b>{metrics.get('mrr_active', 0.0):.2f} ₽/мес</b>",
    ]
    ret_lines = [
        (f"├ 🧲 Retention: <b>{ (metrics.get('retention_rate')*100):.1f}%</b>"
         if metrics.get('retention_rate') is not None else "├ 🧲 Retention: <b>—</b>"),
        (f"├ 💔 Churn: <b>{ (metrics.get('churn_rate')*100):.1f}%</b>"
         if metrics.get('churn_rate') is not None else "├ 💔 Churn: <b>—</b>"),
        f"├ ✅ Продлили: <b>{metrics.get('renewed_count', 0)}</b>",
        f"├ ⏳ Ещё не продлили: <b>{metrics.get('not_renewed_yet', 0)}</b>",
        f"└ 🔮 Прогноз оттока: <b>{metrics.get('predicted_churn', 0.0):.0f} ключ(ей)</b>",
    ]
    def _blockquote(lines: list[str]) -> str:
        compact = [ln for ln in lines if ln and ln.strip()]
        return "<blockquote>" + "\n".join(compact) + "</blockquote>"

    parts = []
    parts.append(TITLE)
    parts.append("")  
    parts.append("📅 <b>Текущий месяц</b>")
    parts.append(_blockquote(top_lines))
    parts.append("")  
    parts.append(DETAILS_PLAN)
    parts.append(_blockquote(plan_details_lines))
    parts.append("") 
    parts.append(DETAILS_REMAIN)
    parts.append(_blockquote(remain_details_lines))
    parts.append("") 
    parts.append("📐 <b>Метрики</b>")
    parts.append(_blockquote(metrics_lines))
    parts.append("")  
    parts.append(RETENTION_TITLE)
    parts.append(_blockquote(ret_lines))
    out: list[str] = []
    last_blank = False
    for p in parts:
        if p == "":
            if not last_blank:
                out.append(p)
            last_blank = True
        else:
            out.append(p)
            last_blank = False
    upd = data.get("updated_human_msk")
    if upd:
        out.append("")
        out.append(f"⏱️ <i>Последнее обновление:</i> <code>{upd}</code>")
    return "\n".join(out)