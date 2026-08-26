from datetime import date, time
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from expenses.models import Category, Expense
from expenses.services import budget_status, total_for
from recurring.models import RecurringExpense, RecurringPayment
from .models import Budget


class BudgetAccountingTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(username='budget-tester', password='password-123')
		self.category = Category.objects.get(name='Food & Dining')
		self.day = date(2026, 8, 26)

	def test_recurring_expense_is_only_counted_in_monthly_budget(self):
		Expense.objects.create(user=self.user, category=self.category, name='Direct expense', amount='100.00', date=self.day, time=time(12))
		weekly_recurring = RecurringExpense.objects.create(user=self.user, category=self.category, name='Weekly transit', amount='50.00', frequency='weekly', next_due_date=self.day)
		weekly_expense = Expense.objects.create(user=self.user, category=self.category, name='Weekly transit', amount='50.00', date=self.day, time=time(13))
		RecurringPayment.objects.create(recurring_expense=weekly_recurring, due_date=self.day, paid=True, paid_date=self.day, expense=weekly_expense)
		monthly_recurring = RecurringExpense.objects.create(user=self.user, category=self.category, name='Rent', amount='500.00', frequency='monthly', next_due_date=self.day)
		monthly_expense = Expense.objects.create(user=self.user, category=self.category, name='Rent', amount='500.00', date=self.day, time=time(14))
		RecurringPayment.objects.create(recurring_expense=monthly_recurring, due_date=self.day, paid=True, paid_date=self.day, expense=monthly_expense)

		weekly = budget_status(self.user, Budget.WEEKLY, self.day)
		monthly = budget_status(self.user, Budget.MONTHLY, self.day)

		self.assertEqual(weekly['spent'], Decimal('150.00'))
		self.assertEqual(monthly['spent'], Decimal('650.00'))
		self.assertEqual(total_for(self.user, self.day, self.day), Decimal('650.00'))

# Create your tests here.
