from django import forms

from .models import RecurringExpense, SavingsGoal


class RecurringExpenseForm(forms.ModelForm):
    class Meta:
        model = RecurringExpense
        fields = ['category', 'name', 'amount', 'frequency', 'next_due_date']
        widgets = {'next_due_date': forms.DateInput(attrs={'type': 'date'}), 'amount': forms.NumberInput(attrs={'step': '0.01'})}


class SavingsGoalForm(forms.ModelForm):
    class Meta:
        model = SavingsGoal
        fields = ['label', 'amount']
        widgets = {'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'})}
