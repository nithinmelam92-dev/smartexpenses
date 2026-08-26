from datetime import timedelta
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from budgets.models import Budget
from expenses.services import category_totals, period_range, total_for


@login_required
def reports(request):
	today = timezone.localdate()
	current_week = period_range(Budget.WEEKLY, today)
	previous_week = (current_week[0] - timedelta(days=7), current_week[0] - timedelta(days=1))
	current_month = period_range(Budget.MONTHLY, today)
	previous_month_end = current_month[0] - timedelta(days=1)
	previous_month = period_range(Budget.MONTHLY, previous_month_end)
	return render(request, 'analysis/index.html', {
		'week': comparison(request.user, current_week, previous_week),
		'month': comparison(request.user, current_month, previous_month),
		'week_chart': json.dumps([float(total_for(request.user, *current_week)), float(total_for(request.user, *previous_week))]),
		'month_chart': json.dumps([float(total_for(request.user, *current_month)), float(total_for(request.user, *previous_month))]),
	})


def comparison(user, current, previous):
	return {'current': total_for(user, *current), 'previous': total_for(user, *previous), 'current_categories': category_totals(user, *current), 'previous_categories': category_totals(user, *previous)}

# Create your views here.
