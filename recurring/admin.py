from django.contrib import admin

from .models import RecurringExpense, RecurringPayment, SavingsGoal


admin.site.register(RecurringExpense)
admin.site.register(RecurringPayment)
admin.site.register(SavingsGoal)

# Register your models here.
