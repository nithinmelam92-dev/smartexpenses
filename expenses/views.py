from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import ExpenseForm
from .models import Category, Expense


def category_api(request):
	return JsonResponse({'categories': list(Category.objects.values('id', 'name'))})


@login_required
def expense_list(request):
	expenses = Expense.objects.filter(user=request.user)
	if request.GET.get('date_from'):
		expenses = expenses.filter(date__gte=request.GET['date_from'])
	if request.GET.get('date_to'):
		expenses = expenses.filter(date__lte=request.GET['date_to'])
	if request.GET.get('amount_min'):
		expenses = expenses.filter(amount__gte=request.GET['amount_min'])
	if request.GET.get('amount_max'):
		expenses = expenses.filter(amount__lte=request.GET['amount_max'])
	if request.GET.get('amount'):
		expenses = expenses.filter(amount=request.GET['amount'])
	return render(request, 'expenses/list.html', {'expenses': expenses, 'filters': request.GET})


@login_required
def expense_create(request):
	initial = {'date': timezone.localdate(), 'time': timezone.localtime().time().replace(microsecond=0)}
	form = ExpenseForm(request.POST or None, initial=initial)
	if request.method == 'POST' and form.is_valid():
		expense = form.save(commit=False)
		expense.user = request.user
		expense.save()
		return redirect('expenses:list')
	return render(request, 'expenses/form.html', {'form': form, 'title': 'Add Expense'})


@login_required
def expense_edit(request, pk):
	expense = get_object_or_404(Expense, pk=pk, user=request.user)
	form = ExpenseForm(request.POST or None, instance=expense)
	if request.method == 'POST' and form.is_valid():
		form.save()
		return redirect('expenses:list')
	return render(request, 'expenses/form.html', {'form': form, 'title': 'Edit Expense'})


@login_required
def expense_delete(request, pk):
	expense = get_object_or_404(Expense, pk=pk, user=request.user)
	if request.method == 'POST':
		expense.delete()
		return redirect('expenses:list')
	return render(request, 'expenses/delete.html', {'expense': expense})

# Create your views here.
