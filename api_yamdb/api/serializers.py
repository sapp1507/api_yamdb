from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email")
        model = User

    def validate(self, data):
        username = data["username"]
        if username == "me":
            raise serializers.ValidationError(
                "Имя пользователя me - недоступно"
            )
        return super().validate(data)


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=256)
    confirmation_code = serializers.CharField(max_length=512)

    class Meta:
        fields = ("username", "confirmation_code")
        model = User

    def validate(self, data):
        if not data["username"]:
            raise serializers.ValidationError(
                "Имя пользователя me - недоступно"
            )
        user = get_object_or_404(User, username=data["username"])
        confirmation_code = data["confirmation_code"]
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError()
        return super().validate(data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "username",
            "email",
            "role",
            "bio",
            "first_name",
            "last_name",
        )
        model = User


class UserMeSerializer(UserSerializer):
    role = serializers.ChoiceField(choices=settings.CHOICES, read_only=True)
