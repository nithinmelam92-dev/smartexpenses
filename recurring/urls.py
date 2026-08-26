from django.urls import path

from . import views

app_name = 'recurring'

urlpatterns = [
	path('', views.recurring_list, name='list'),
	path('add/', views.recurring_create, name='add'),
	path('<int:pk>/edit/', views.recurring_edit, name='edit'),
	path('<int:pk>/delete/', views.recurring_delete, name='delete'),
	path('reminder/', views.reminder, name='reminder'),
	path('payment/<int:pk>/paid/', views.mark_paid, name='mark_paid'),
	path('payment/<int:pk>/push/', views.push_date, name='push_date'),
	path('savings/', views.savings, name='savings'),
]
