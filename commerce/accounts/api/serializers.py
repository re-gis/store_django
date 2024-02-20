from rest_framework import serializers
from rest_auth.serializers import LoginSerializer
from django.contrib.auth import get_user_model

try:
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
    from allauth.utils import email_address_exists
except ImportError:
    raise ImportError("Please install allauth in the project!")


User = get_user_model()


class CustomerUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(style={"input_type": "password"})


class CustomerRegisterSerializer(serializers.Serializer):
    username = None
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True, style={"input_type": "password"})
    password2 = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if email and email_address_exists(email):
            raise serializers.ValidationError("Email address already exists!")
        return email

    def validate_password(self, password):
        return get_adapter().validate_password(password)

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords mismatch!")
        return data

    def get_clean_data(self):
        return {
            "first_name": self.validated_data.get("first_name"),
            "last_name": self.validated_data.get("last_name"),
            "password1": self.validated_data.get("password1"),
            "email": self.validated_data.get("email"),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        return user
