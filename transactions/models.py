from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """
    CustomUser model extends the AbstractUser model to include additional 
    fields for first name, last name, groups, and user permissions.

    Attributes:
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        groups (ManyToManyField): The groups the user belongs to.
        user_permissions (ManyToManyField): The permissions the user has.
    """
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    groups = models.ManyToManyField(Group, verbose_name=_("groups"), blank=True, related_name="custom_user_set")
    user_permissions = models.ManyToManyField(Permission, verbose_name=_("user permissions"), blank=True, related_name="custom_user_set")

class Transaction(models.Model):
    """
    Transaction model represents a financial transaction made by a user, 
    which can be either an income or an expense.

    Attributes:
        user (ForeignKey): The user who made the transaction.
        description (str): A description of the transaction.
        amount (Decimal): The amount of the transaction.
        date (Date): The date of the transaction.
        transaction_type (str): The type of the transaction (income or expense).
    """
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES, default='income')  # Default value added

    def __str__(self):
        return self.description
