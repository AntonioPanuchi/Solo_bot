"""
Мониторинг бизнес-метрик
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

from .. import settings
from ..privacy import PrivacyComplianceChecker
from logger import logger


class BusinessMonitor:
    """Мониторинг бизнес-метрик с соблюдением приватности"""
    
    def __init__(self):
        self.privacy_checker = PrivacyComplianceChecker()
        self.business_cache = {}
        
    async def collect_business_metrics(self):
        """Сбор бизнес-метрик"""
        try:
            # Метрики пользователей
            user_metrics = await self.get_user_metrics()
            
            # Метрики выручки
            revenue_metrics = await self.get_revenue_metrics()
            
            # Метрики подписок
            subscription_metrics = await self.get_subscription_metrics()
            
            # Метрики конверсии
            conversion_metrics = await self.get_conversion_metrics()
            
            # Объединяем все метрики
            metrics = {
                "timestamp": datetime.utcnow().isoformat(),
                "user_metrics": user_metrics,
                "revenue_metrics": revenue_metrics,
                "subscription_metrics": subscription_metrics,
                "conversion_metrics": conversion_metrics
            }
            
            # Проверяем соответствие требованиям приватности
            if not self.privacy_checker.validate_metrics(metrics):
                logger.warning("[Business Monitor] Бизнес-метрики не прошли проверку приватности")
                return
            
            # Сохраняем метрики
            await self.store_business_metrics(metrics)
            
            # Кэшируем для быстрого доступа
            self.business_cache = {
                "data": metrics,
                "timestamp": datetime.utcnow()
            }
            
            logger.debug("[Business Monitor] Бизнес-метрики собраны успешно")
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка сбора бизнес-метрик: {e}")
    
    async def get_user_metrics(self) -> Dict[str, Any]:
        """Получение метрик пользователей (анонимизированно)"""
        try:
            # Общее количество пользователей
            total_users = await self.get_total_users()
            
            # Активные пользователи
            active_users = await self.get_active_users()
            
            # Новые пользователи за период
            new_users = await self.get_new_users()
            
            # Удержание пользователей
            retention_rate = await self.get_retention_rate()
            
            # Отток пользователей
            churn_rate = await self.get_churn_rate()
            
            return {
                "total_users": total_users,
                "active_users": active_users,
                "new_users_today": new_users.get("today", 0),
                "new_users_this_week": new_users.get("week", 0),
                "new_users_this_month": new_users.get("month", 0),
                "retention_rate_percent": retention_rate,
                "churn_rate_percent": churn_rate,
                "user_growth_rate": await self.get_user_growth_rate()
            }
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения метрик пользователей: {e}")
            return {}
    
    async def get_revenue_metrics(self) -> Dict[str, Any]:
        """Получение метрик выручки"""
        try:
            # Выручка за разные периоды
            daily_revenue = await self.get_daily_revenue()
            weekly_revenue = await self.get_weekly_revenue()
            monthly_revenue = await self.get_monthly_revenue()
            
            # Рост выручки
            revenue_growth = await self.get_revenue_growth()
            
            # Выручка по тарифам
            revenue_by_tariff = await self.get_revenue_by_tariff()
            
            # Средний чек
            average_receipt = await self.get_average_receipt()
            
            return {
                "daily_revenue": daily_revenue,
                "weekly_revenue": weekly_revenue,
                "monthly_revenue": monthly_revenue,
                "revenue_growth_percent": revenue_growth,
                "revenue_by_tariff": revenue_by_tariff,
                "average_receipt": average_receipt,
                "revenue_per_user": await self.get_revenue_per_user()
            }
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения метрик выручки: {e}")
            return {}
    
    async def get_subscription_metrics(self) -> Dict[str, Any]:
        """Получение метрик подписок"""
        try:
            # Общее количество подписок
            total_subscriptions = await self.get_total_subscriptions()
            
            # Активные подписки
            active_subscriptions = await self.get_active_subscriptions()
            
            # Новые подписки
            new_subscriptions = await self.get_new_subscriptions()
            
            # Продления подписок
            renewals = await self.get_subscription_renewals()
            
            # Отмены подписок
            cancellations = await self.get_subscription_cancellations()
            
            return {
                "total_subscriptions": total_subscriptions,
                "active_subscriptions": active_subscriptions,
                "new_subscriptions_today": new_subscriptions.get("today", 0),
                "new_subscriptions_this_week": new_subscriptions.get("week", 0),
                "renewal_rate_percent": renewals.get("rate", 0),
                "cancellation_rate_percent": cancellations.get("rate", 0),
                "average_subscription_duration": await self.get_average_subscription_duration()
            }
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения метрик подписок: {e}")
            return {}
    
    async def get_conversion_metrics(self) -> Dict[str, Any]:
        """Получение метрик конверсии"""
        try:
            # Общая конверсия
            overall_conversion = await self.get_overall_conversion_rate()
            
            # Конверсия по источникам
            conversion_by_source = await self.get_conversion_by_source()
            
            # Конверсия по тарифам
            conversion_by_tariff = await self.get_conversion_by_tariff()
            
            # Воронка конверсии
            conversion_funnel = await self.get_conversion_funnel()
            
            return {
                "overall_conversion_rate": overall_conversion,
                "conversion_by_source": conversion_by_source,
                "conversion_by_tariff": conversion_by_tariff,
                "conversion_funnel": conversion_funnel,
                "trial_to_paid_conversion": await self.get_trial_to_paid_conversion()
            }
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения метрик конверсии: {e}")
            return {}
    
    async def get_total_users(self) -> int:
        """Получение общего количества пользователей"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return random.randint(1000, 5000)
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения общего количества пользователей: {e}")
            return 0
    
    async def get_active_users(self) -> int:
        """Получение количества активных пользователей"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return random.randint(200, 800)
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения активных пользователей: {e}")
            return 0
    
    async def get_new_users(self) -> Dict[str, int]:
        """Получение количества новых пользователей за периоды"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return {
                "today": random.randint(5, 25),
                "week": random.randint(30, 150),
                "month": random.randint(100, 500)
            }
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения новых пользователей: {e}")
            return {}
    
    async def get_retention_rate(self) -> float:
        """Получение процента удержания пользователей"""
        try:
            # Здесь должна быть логика расчета удержания
            import random
            return round(random.uniform(75, 90), 2)
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения удержания: {e}")
            return 0.0
    
    async def get_churn_rate(self) -> float:
        """Получение процента оттока пользователей"""
        try:
            # Здесь должна быть логика расчета оттока
            import random
            return round(random.uniform(5, 15), 2)
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения оттока: {e}")
            return 0.0
    
    async def get_user_growth_rate(self) -> float:
        """Получение темпа роста пользователей"""
        try:
            # Здесь должна быть логика расчета роста
            import random
            return round(random.uniform(5, 25), 2)
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения темпа роста: {e}")
            return 0.0
    
    async def get_daily_revenue(self) -> float:
        """Получение дневной выручки"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return round(random.uniform(10000, 50000), 2)
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения дневной выручки: {e}")
            return 0.0
    
    async def get_weekly_revenue(self) -> float:
        """Получение недельной выручки"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return round(random.uniform(70000, 350000), 2)
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения недельной выручки: {e}")
            return 0.0
    
    async def get_monthly_revenue(self) -> float:
        """Получение месячной выручки"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return round(random.uniform(300000, 1500000), 2)
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения месячной выручки: {e}")
            return 0.0
    
    async def get_revenue_growth(self) -> float:
        """Получение темпа роста выручки"""
        try:
            # Здесь должна быть логика расчета роста выручки
            import random
            return round(random.uniform(-5, 30), 2)
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения роста выручки: {e}")
            return 0.0
    
    async def get_revenue_by_tariff(self) -> Dict[str, float]:
        """Получение выручки по тарифам"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return {
                "1_month": round(random.uniform(10000, 30000), 2),
                "3_months": round(random.uniform(20000, 50000), 2),
                "6_months": round(random.uniform(15000, 40000), 2),
                "12_months": round(random.uniform(10000, 30000), 2)
            }
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения выручки по тарифам: {e}")
            return {}
    
    async def get_average_receipt(self) -> float:
        """Получение среднего чека"""
        try:
            # Здесь должна быть логика расчета среднего чека
            import random
            return round(random.uniform(500, 2000), 2)
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения среднего чека: {e}")
            return 0.0
    
    async def get_revenue_per_user(self) -> float:
        """Получение выручки на пользователя"""
        try:
            # Здесь должна быть логика расчета выручки на пользователя
            import random
            return round(random.uniform(100, 500), 2)
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения выручки на пользователя: {e}")
            return 0.0
    
    async def get_total_subscriptions(self) -> int:
        """Получение общего количества подписок"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return random.randint(500, 2000)
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения общего количества подписок: {e}")
            return 0
    
    async def get_active_subscriptions(self) -> int:
        """Получение количества активных подписок"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return random.randint(300, 1200)
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения активных подписок: {e}")
            return 0
    
    async def get_new_subscriptions(self) -> Dict[str, int]:
        """Получение количества новых подписок за периоды"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return {
                "today": random.randint(2, 15),
                "week": random.randint(10, 80),
                "month": random.randint(40, 300)
            }
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения новых подписок: {e}")
            return {}
    
    async def get_subscription_renewals(self) -> Dict[str, Any]:
        """Получение метрик продления подписок"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return {
                "rate": round(random.uniform(70, 85), 2),
                "count_today": random.randint(5, 20),
                "count_this_week": random.randint(30, 100)
            }
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения продлений: {e}")
            return {}
    
    async def get_subscription_cancellations(self) -> Dict[str, Any]:
        """Получение метрик отмены подписок"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return {
                "rate": round(random.uniform(5, 15), 2),
                "count_today": random.randint(1, 8),
                "count_this_week": random.randint(5, 30)
            }
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения отмен: {e}")
            return {}
    
    async def get_average_subscription_duration(self) -> float:
        """Получение средней продолжительности подписки"""
        try:
            # Здесь должна быть логика расчета продолжительности
            import random
            return round(random.uniform(30, 120), 2)  # дни
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения продолжительности подписки: {e}")
            return 0.0
    
    async def get_overall_conversion_rate(self) -> float:
        """Получение общей конверсии"""
        try:
            # Здесь должна быть логика расчета конверсии
            import random
            return round(random.uniform(2, 8), 2)
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения общей конверсии: {e}")
            return 0.0
    
    async def get_conversion_by_source(self) -> Dict[str, float]:
        """Получение конверсии по источникам"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return {
                "telegram_ads": round(random.uniform(3, 10), 2),
                "referral": round(random.uniform(5, 15), 2),
                "organic": round(random.uniform(1, 5), 2),
                "direct": round(random.uniform(2, 8), 2)
            }
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения конверсии по источникам: {e}")
            return {}
    
    async def get_conversion_by_tariff(self) -> Dict[str, float]:
        """Получение конверсии по тарифам"""
        try:
            # Здесь должна быть логика получения из базы данных
            import random
            return {
                "1_month": round(random.uniform(2, 6), 2),
                "3_months": round(random.uniform(3, 8), 2),
                "6_months": round(random.uniform(4, 10), 2),
                "12_months": round(random.uniform(5, 12), 2)
            }
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения конверсии по тарифам: {e}")
            return {}
    
    async def get_conversion_funnel(self) -> Dict[str, Any]:
        """Получение воронки конверсии"""
        try:
            # Здесь должна быть логика расчета воронки
            import random
            return {
                "visitors": random.randint(1000, 5000),
                "registrations": random.randint(100, 500),
                "trials": random.randint(50, 200),
                "paid_subscriptions": random.randint(20, 100)
            }
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения воронки конверсии: {e}")
            return {}
    
    async def get_trial_to_paid_conversion(self) -> float:
        """Получение конверсии из пробной в платную подписку"""
        try:
            # Здесь должна быть логика расчета конверсии
            import random
            return round(random.uniform(15, 35), 2)
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения конверсии пробной подписки: {e}")
            return 0.0
    
    async def store_business_metrics(self, metrics: Dict[str, Any]):
        """Сохранение бизнес-метрик"""
        try:
            # Здесь должна быть логика сохранения в базу данных
            logger.debug("[Business Monitor] Сохранение бизнес-метрик")
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка сохранения метрик: {e}")
    
    async def get_business_summary(self) -> Dict[str, Any]:
        """Получение сводки по бизнес-метрикам"""
        try:
            if not self.business_cache:
                return {"status": "no_data"}
            
            metrics = self.business_cache["data"]
            
            return {
                "status": "ok",
                "last_update": metrics["timestamp"],
                "total_users": metrics.get("user_metrics", {}).get("total_users", 0),
                "active_users": metrics.get("user_metrics", {}).get("active_users", 0),
                "daily_revenue": metrics.get("revenue_metrics", {}).get("daily_revenue", 0),
                "monthly_revenue": metrics.get("revenue_metrics", {}).get("monthly_revenue", 0),
                "conversion_rate": metrics.get("conversion_metrics", {}).get("overall_conversion_rate", 0),
                "retention_rate": metrics.get("user_metrics", {}).get("retention_rate_percent", 0)
            }
            
        except Exception as e:
            logger.error(f"[Business Monitor] Ошибка получения сводки: {e}")
            return {"status": "error"}
