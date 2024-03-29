from rest_auth.registration.views import RegisterView
from rest_auth.views import LoginView
from accounts.api.serializers import CustomerRegisterSerializer


class CustomLoginView(LoginView):
    pass


class CustomRegisterView(RegisterView):
    serializer_class = CustomerRegisterSerializer
