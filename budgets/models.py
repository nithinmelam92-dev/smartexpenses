from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Budget(models.Model):
	WEEKLY = 'weekly'
	MONTHLY = 'monthly'
	PERIOD_CHOICES = [(WEEKLY, 'Weekly'), (MONTHLY, 'Monthly')]

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
	period_type = models.CharField(max_length=10, choices=PERIOD_CHOICES)
	amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
	start_date = models.DateField()

	class Meta:
		ordering = ['period_type', '-start_date']
		constraints = [models.UniqueConstraint(fields=['user', 'period_type', 'start_date'], name='unique_budget_period')]

	def __str__(self):
		return f'{self.user} {self.get_period_type_display()} {self.start_date}'

# Create your models here.
