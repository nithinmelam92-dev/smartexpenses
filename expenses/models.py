from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


STUDENT_CATEGORY_NAMES = [
	'Food & Dining', 'Groceries', 'Transportation', 'Education',
	'Accommodation', 'Utilities', 'Shopping', 'Entertainment',
	'Technology', 'Health', 'Fitness & Sports', 'Travel',
	'Personal Care', 'Gifts & Social', 'Financial', 'Other',
]


class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)
	icon = models.CharField(max_length=20, blank=True)
	color = models.CharField(max_length=20, blank=True)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name


class Expense(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses')
	name = models.CharField(max_length=200)
	amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.01)])
	category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='expenses')
	date = models.DateField()
	time = models.TimeField()
	note = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-date', '-time', '-id']
		indexes = [models.Index(fields=['user', 'date'])]

	def __str__(self):
		return f'{self.name} ({self.amount})'

# Create your models here.
