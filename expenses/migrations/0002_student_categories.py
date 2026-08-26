from django.db import migrations


CATEGORY_NAMES = [
    'Food & Dining',
    'Groceries',
    'Transportation',
    'Education',
    'Accommodation',
    'Utilities',
    'Shopping',
    'Entertainment',
    'Technology',
    'Health',
    'Fitness & Sports',
    'Travel',
    'Personal Care',
    'Gifts & Social',
    'Financial',
    'Other',
]


def migrate_categories(apps, schema_editor):
    Category = apps.get_model('expenses', 'Category')
    Expense = apps.get_model('expenses', 'Expense')
    RecurringExpense = apps.get_model('recurring', 'RecurringExpense')

    categories = {}
    for name in CATEGORY_NAMES:
        category, _ = Category.objects.get_or_create(name=name)
        categories[name] = category

    other = categories['Other']
    Expense.objects.exclude(category__name__in=CATEGORY_NAMES).update(category=other)
    RecurringExpense.objects.exclude(category__name__in=CATEGORY_NAMES).update(category=other)
    Category.objects.exclude(name__in=CATEGORY_NAMES).delete()


def reverse_categories(apps, schema_editor):
    # The legacy category names are not recoverable after remapping to Other.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('expenses', '0001_initial'),
        ('recurring', '0001_initial'),
    ]

    operations = [migrations.RunPython(migrate_categories, reverse_categories)]
