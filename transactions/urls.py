from django.urls import path
from . import views
from .views import register, login_view, logout_view, dashboard, add_transaction, edit_transaction, delete_transaction

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('add_transaction/income/', views.add_transaction, name='add_income_transaction'),
    path('add_transaction/expense/', views.add_transaction, name='add_expense_transaction'),

    path('edit/<int:id>/', edit_transaction, name='edit_transaction'),
    path('delete/<int:id>/', delete_transaction, name='delete_transaction'),
]
