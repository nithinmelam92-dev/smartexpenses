import calendar
from datetime import date, timedelta
from decimal import Decimal

from django.db.models import Sum

from budgets.models import Budget
from .models import Expense

ZERO = Decimal('0.00')


def week_start(day):
    return day - timedelta(days=day.weekday())


def month_start(day):
    return day.replace(day=1)


def month_end(day):
    return day.replace(day=calendar.monthrange(day.year, day.month)[1])


def period_range(period_type, day):
    if period_type == Budget.WEEKLY:
        start = week_start(day)
        return start, start + timedelta(days=6)
    start = month_start(day)
    return start, month_end(day)


def total_for(user, start, end):
    return Expense.objects.filter(user=user, date__range=(start, end)).aggregate(total=Sum('amount')).get('total') or ZERO


def budget_total_for(user, start, end, period_type):
    expenses = Expense.objects.filter(user=user, date__range=(start, end))
    if period_type == Budget.WEEKLY:
        expenses = expenses.filter(recurring_payment__isnull=True)
    return expenses.aggregate(total=Sum('amount')).get('total') or ZERO


def category_totals(user, start, end):
    return list(Expense.objects.filter(user=user, date__range=(start, end)).values('category__name').annotate(total=Sum('amount')).order_by('-total'))


def budget_status(user, period_type, day=None):
    day = day or date.today()
    start, end = period_range(period_type, day)
    budget = Budget.objects.filter(user=user, period_type=period_type, start_date=start).first()
    spent = budget_total_for(user, start, end, period_type)
    return {'budget': budget, 'spent': spent, 'start': start, 'end': end, 'remaining': (budget.amount - spent) if budget else None}


def average_spend(user, day=None):
    day = day or date.today()
    current_week = period_range(Budget.WEEKLY, day)
    current_month = period_range(Budget.MONTHLY, day)
    total = total_for(user, date.min, day)
    days = Expense.objects.filter(user=user, date__lte=day).values('date').distinct().count()
    return {
        'daily': total / days if days else ZERO,
        'weekly': total_for(user, *current_week) / 7,
        'monthly': total_for(user, *current_month) / day.day,
    }


def daily_totals(user, start, end):
    return list(Expense.objects.filter(user=user, date__range=(start, end)).values('date').annotate(total=Sum('amount')).order_by('date'))


def next_due(current, frequency):
    if frequency == 'weekly':
        return current + timedelta(days=7)
    year = current.year + (1 if current.month == 12 else 0)
    month = 1 if current.month == 12 else current.month + 1
    return date(year, month, min(current.day, calendar.monthrange(year, month)[1]))
