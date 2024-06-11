from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Transaction


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['description', 'amount', 'date']  # transaction_type ni o'zgartirdik

    def clean(self):
        cleaned_data = super().clean()
        if 'amount' in cleaned_data:
            amount = cleaned_data['amount']
            if amount > 0:
                cleaned_data['transaction_type'] = 'income'  # Agar mablag' musbat bo'lsa, transaction_type = 'income'
            elif amount < 0:
                cleaned_data['transaction_type'] = 'expense'  # Agar mablag' manfiy bo'lsa, transaction_type = 'expense'
        return cleaned_data