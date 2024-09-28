from datetime import datetime, timedelta
import pytz


class Utc:
    """Provides reusable date-time utilities."""

    day_delta = timedelta(days=1)
    week_delta = timedelta(days=7)
    month_delta = timedelta(days=30)

    @staticmethod
    def get_now() -> datetime:
        return datetime.now(pytz.utc)

    @staticmethod
    def get_hours_prior(hours: int, reference: datetime = None) -> datetime:
        reference = reference or Utc.get_now()
        delta = timedelta(hours=hours)
        return reference - delta

    @staticmethod
    def get_days_prior(days: int, reference: datetime = None) -> datetime:
        reference = reference or Utc.get_now()
        delta = timedelta(days=days)
        return reference - delta

    @staticmethod
    def get_days_after(days: int, reference: datetime = None) -> datetime:
        reference = reference or Utc.get_now()
        delta = timedelta(days=days)
        return reference + delta

    @staticmethod
    def get_yesterday() -> datetime:
        return Utc.get_days_prior(1)

    @staticmethod
    def get_tomorrow() -> datetime:
        return Utc.get_days_after(1)

    @staticmethod
    def get_a_week_prior(reference: datetime = None) -> datetime:
        return Utc.get_days_prior(7, reference)

    @staticmethod
    def get_a_week_after(reference: datetime = None) -> datetime:
        return Utc.get_days_after(7, reference)

    @staticmethod
    def get_a_month_prior(reference: datetime = None) -> datetime:
        return Utc.get_days_prior(30, reference)

    @staticmethod
    def get_a_month_after(reference: datetime = None) -> datetime:
        return Utc.get_days_after(30, reference)

    @staticmethod
    def was_in_the_last_n_hours(moment: datetime, n: int) -> bool:
        upper = Utc.get_now()
        lower = Utc.get_hours_prior(n)
        return lower < moment and moment < upper
