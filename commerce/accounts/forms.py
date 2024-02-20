from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomerUser


class CustomerUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomerUser
        fields = ("first_name", "last_name", "email")


class CustomerUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomerUser
        fields = ("first_name", "last_name", "email")
