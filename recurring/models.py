from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from expenses.models import Category


class RecurringExpense(models.Model):
	WEEKLY = 'weekly'
	MONTHLY = 'monthly'
	FREQUENCY_CHOICES = [(WEEKLY, 'Weekly'), (MONTHLY, 'Monthly')]

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recurring_expenses')
	name = models.CharField(max_length=200)
	amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
	category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='recurring_expenses')
	frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
	next_due_date = models.DateField()
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ['next_due_date', 'name']

	def __str__(self):
		return self.name


class RecurringPayment(models.Model):
	recurring_expense = models.ForeignKey(RecurringExpense, on_delete=models.CASCADE, related_name='payments')
	due_date = models.DateField()
	paid = models.BooleanField(default=False)
	paid_date = models.DateField(null=True, blank=True)
	expense = models.OneToOneField('expenses.Expense', on_delete=models.SET_NULL, null=True, blank=True, related_name='recurring_payment')

	class Meta:
		ordering = ['due_date', 'id']
		constraints = [models.UniqueConstraint(fields=['recurring_expense', 'due_date'], name='unique_recurring_due_date')]


class SavingsGoal(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='savings_goals')
	label = models.CharField(max_length=200)
	amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
	created_date = models.DateField(auto_now_add=True)

	class Meta:
		ordering = ['-created_date', '-id']

# Create your models here.
