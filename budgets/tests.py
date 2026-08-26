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
		recurring = RecurringExpense.objects.create(user=self.user, category=self.category, name='Rent', amount='500.00', frequency='monthly', next_due_date=self.day)
		recurring_expense = Expense.objects.create(user=self.user, category=self.category, name='Rent', amount='500.00', date=self.day, time=time(13))
		RecurringPayment.objects.create(recurring_expense=recurring, due_date=self.day, paid=True, paid_date=self.day, expense=recurring_expense)

		weekly = budget_status(self.user, Budget.WEEKLY, self.day)
		monthly = budget_status(self.user, Budget.MONTHLY, self.day)

		self.assertEqual(weekly['spent'], Decimal('100.00'))
		self.assertEqual(monthly['spent'], Decimal('600.00'))
		self.assertEqual(total_for(self.user, self.day, self.day), Decimal('600.00'))

# Create your tests here.
