from datetime import date
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from budgets.models import Budget
from expenses.models import Expense
from expenses.services import budget_status, next_due
from .forms import RecurringExpenseForm, SavingsGoalForm
from .models import RecurringExpense, RecurringPayment, SavingsGoal


def ensure_next_cycle(payment):
	recurring = payment.recurring_expense
	if not payment.paid:
		return
	due = next_due(payment.due_date, recurring.frequency)
	recurring.next_due_date = due
	recurring.save(update_fields=['next_due_date'])
	RecurringPayment.objects.get_or_create(recurring_expense=recurring, due_date=due)


@login_required
def recurring_list(request):
	recurring = RecurringExpense.objects.filter(user=request.user, active=True).prefetch_related('payments')
	return render(request, 'recurring/list.html', {'recurring': recurring, 'today': timezone.localdate()})


@login_required
def recurring_create(request):
	form = RecurringExpenseForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		item = form.save(commit=False)
		item.user = request.user
		item.save()
		RecurringPayment.objects.create(recurring_expense=item, due_date=item.next_due_date)
		return redirect('recurring:list')
	return render(request, 'recurring/form.html', {'form': form, 'title': 'Add Recurring Expense'})


@login_required
def recurring_edit(request, pk):
	item = get_object_or_404(RecurringExpense, pk=pk, user=request.user)
	form = RecurringExpenseForm(request.POST or None, instance=item)
	if request.method == 'POST' and form.is_valid():
		form.save()
		return redirect('recurring:list')
	return render(request, 'recurring/form.html', {'form': form, 'title': 'Edit Recurring Expense'})


@login_required
def recurring_delete(request, pk):
	item = get_object_or_404(RecurringExpense, pk=pk, user=request.user)
	if request.method == 'POST':
		item.delete()
		return redirect('recurring:list')
	return render(request, 'recurring/delete.html', {'item': item})


@login_required
def reminder(request):
	pending = list(RecurringPayment.objects.filter(recurring_expense__user=request.user, paid=False, recurring_expense__active=True).select_related('recurring_expense', 'recurring_expense__category'))
	for payment in pending:
		if payment.due_date < timezone.localdate():
			payment.recurring_expense.next_due_date = payment.due_date
			payment.recurring_expense.save(update_fields=['next_due_date'])
	savings = SavingsGoal.objects.filter(user=request.user)
	return render(request, 'recurring/reminder.html', {'pending': pending, 'weekly': budget_status(request.user, Budget.WEEKLY), 'monthly': budget_status(request.user, Budget.MONTHLY), 'savings': savings, 'savings_total': savings.aggregate(total=Sum('amount')).get('total') or 0, 'form': SavingsGoalForm()})


@login_required
@transaction.atomic
def mark_paid(request, pk):
	payment = get_object_or_404(RecurringPayment.objects.select_for_update().select_related('recurring_expense'), pk=pk, recurring_expense__user=request.user)
	if request.method == 'POST' and not payment.paid:
		recurring = payment.recurring_expense
		payment.paid = True
		payment.paid_date = timezone.localdate()
		payment.expense = Expense.objects.create(user=request.user, name=recurring.name, amount=recurring.amount, category=recurring.category, date=payment.paid_date, time=timezone.localtime().time(), note=f'Recurring payment due {payment.due_date}')
		payment.save(update_fields=['paid', 'paid_date', 'expense'])
		ensure_next_cycle(payment)
	return redirect('recurring:reminder')


@login_required
def push_date(request, pk):
	payment = get_object_or_404(RecurringPayment, pk=pk, recurring_expense__user=request.user, paid=False)
	if request.method == 'POST':
		payment.due_date = next_due(payment.due_date, payment.recurring_expense.frequency)
		payment.save(update_fields=['due_date'])
		payment.recurring_expense.next_due_date = payment.due_date
		payment.recurring_expense.save(update_fields=['next_due_date'])
	return redirect('recurring:reminder')


@login_required
def savings(request):
	form = SavingsGoalForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		goal = form.save(commit=False)
		goal.user = request.user
		goal.save()
		return redirect('recurring:reminder')
	savings = SavingsGoal.objects.filter(user=request.user)
	return render(request, 'recurring/reminder.html', {'pending': [], 'weekly': budget_status(request.user, Budget.WEEKLY), 'monthly': budget_status(request.user, Budget.MONTHLY), 'savings': savings, 'savings_total': savings.aggregate(total=Sum('amount')).get('total') or 0, 'form': form})

# Create your views here.
