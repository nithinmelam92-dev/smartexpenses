from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from recurring.models import RecurringExpense, RecurringPayment
from .forms import ExpenseForm
from .models import Category, Expense, STUDENT_CATEGORY_NAMES
from .services import total_for


class ExpenseAndRecurringTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(username='tester', password='password-123')
		self.category = Category.objects.get(name='Food & Dining')
		self.client.login(username='tester', password='password-123')

	def test_empty_total_is_zero(self):
		self.assertEqual(total_for(self.user, date.min, date.today()), Decimal('0.00'))

	def test_expense_form_uses_student_categories(self):
		labels = [label for value, label in ExpenseForm().fields['category'].choices if value]
		self.assertEqual(set(labels), set(STUDENT_CATEGORY_NAMES))

	def test_category_api_returns_exact_student_categories(self):
		response = self.client.get('/expenses/api/categories/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual({item['name'] for item in response.json()['categories']}, set(STUDENT_CATEGORY_NAMES))

	def test_expense_create_is_owned_by_logged_in_user(self):
		response = self.client.post('/expenses/add/', {'category': self.category.pk, 'name': 'Lunch', 'amount': '125.50', 'date': '2026-08-26', 'time': '12:00', 'note': ''})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Expense.objects.get().user, self.user)

	def test_paid_recurring_payment_creates_one_expense_and_next_cycle(self):
		recurring = RecurringExpense.objects.create(user=self.user, name='Internet', amount='500.00', category=self.category, frequency='monthly', next_due_date=date(2026, 8, 26))
		payment = RecurringPayment.objects.create(recurring_expense=recurring, due_date=date(2026, 8, 26))
		response = self.client.post(f'/recurring/payment/{payment.pk}/paid/')
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Expense.objects.filter(name='Internet').count(), 1)
		self.assertEqual(RecurringPayment.objects.filter(recurring_expense=recurring).count(), 2)
		self.client.post(f'/recurring/payment/{payment.pk}/paid/')
		self.assertEqual(Expense.objects.filter(name='Internet').count(), 1)

# Create your tests here.
