from django import forms

from .models import Budget


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['amount']
        widgets = {'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0'})}
