from django.urls import path

from . import views

app_name = 'expenses'

urlpatterns = [
	path('api/categories/', views.category_api, name='category_api'),
	path('', views.expense_list, name='list'),
	path('add/', views.expense_create, name='add'),
	path('<int:pk>/edit/', views.expense_edit, name='edit'),
	path('<int:pk>/delete/', views.expense_delete, name='delete'),
]
