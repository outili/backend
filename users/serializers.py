from django.contrib.auth import get_user_model
from djoser import serializers as djoser_serializers
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer,
)

User = get_user_model()


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)
        token["roles"] = [
            role
            for role, has_role in {
                "student": user.is_student,
                "instructor": user.is_instructor,
            }.items()
            if has_role
        ]

        return token


class UserCreateSerializer(djoser_serializers.UserCreateSerializer):
    class Meta(djoser_serializers.UserCreateSerializer.Meta):
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
        ]


class UserSerializer(djoser_serializers.UserSerializer):
    class Meta(djoser_serializers.UserSerializer.Meta):
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_student",
            "is_instructor",
        ]
        read_only_fields = ["id", "is_active", "is_student", "is_instructor"]


class RoleAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "is_student",
            "is_instructor",
        ]
