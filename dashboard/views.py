from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import render
from expenses.services import average_spend, budget_status, category_totals, daily_totals, period_range, total_for
from budgets.models import Budget


@login_required
def dashboard(request):
	from datetime import date
	today = date.today()
	start = date(today.year, today.month, 1)
	return render(request, 'dashboard/index.html', {
		'total': total_for(request.user, date.min, today),
		'categories': category_totals(request.user, date.min, today),
		'daily': daily_totals(request.user, start, today),
		'averages': average_spend(request.user, today),
		'budget': budget_status(request.user, Budget.MONTHLY, today),
		'category_labels': json.dumps([item['category__name'] for item in category_totals(request.user, date.min, today)]),
		'category_values': json.dumps([float(item['total']) for item in category_totals(request.user, date.min, today)]),
		'daily_labels': json.dumps([item['date'].isoformat() for item in daily_totals(request.user, date.min, today)]),
		'daily_values': json.dumps([float(item['total']) for item in daily_totals(request.user, date.min, today)]),
	})

# Create your views here.
