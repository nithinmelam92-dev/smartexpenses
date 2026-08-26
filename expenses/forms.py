from django import forms

from .models import Category, Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'date', 'name', 'amount', 'time', 'note']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}), 'time': forms.TimeInput(attrs={'type': 'time'}), 'amount': forms.NumberInput(attrs={'step': '0.01'})}


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'icon', 'color']
