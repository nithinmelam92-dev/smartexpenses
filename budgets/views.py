from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from expenses.services import budget_status
from .forms import BudgetForm
from .models import Budget


@login_required
def budget_page(request):
	today = timezone.localdate()
	statuses = {period: budget_status(request.user, period, today) for period in (Budget.WEEKLY, Budget.MONTHLY)}
	if request.method == 'POST':
		period = request.POST.get('period_type')
		if period in statuses:
			form = BudgetForm(request.POST)
			if form.is_valid():
				Budget.objects.update_or_create(user=request.user, period_type=period, start_date=statuses[period]['start'], defaults={'amount': form.cleaned_data['amount']})
				return redirect('budgets:list')
		else:
			form = BudgetForm()
	else:
		form = BudgetForm()
	return render(request, 'budgets/index.html', {'statuses': statuses, 'form': form})

# Create your views here.
