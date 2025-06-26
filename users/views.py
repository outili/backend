from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjoserUserViewSet
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from users.filters import UserFilter
from users.serializers import (
    RoleAssignSerializer,
    UserCreateSerializer,
    UserSerializer,
)

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    filterset_class = UserFilter
    search_fields = ["email", "first_name", "last_name"]
    ordering_fields = [
        "email",
        "first_name",
        "last_name",
    ]

    def get_queryset(self):
        user = self.request.user

        if self.action == "list" and not (
            user.is_staff or user.is_superuser or user.is_instructor
        ):
            return User.objects.filter(
                is_staff=False,
                is_superuser=False,
            )

        if self.action in ["list", "assign_position"] and user.is_staff:
            return User.objects.filter(is_active=True)

        return super().get_queryset()

    def get_permissions(self):
        if self.action == "assign_role":
            return [IsAdminUser]
        return super().get_permissions()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="ordering",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Field to order by (use prefix '-' for descending order).",
                enum=ordering_fields + [f"-{field}" for field in ordering_fields],
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def create(self, request, *args, **kwargs):
        pass

    @action(
        detail=False,
        methods=["post"],
        url_path="signup",
        serializer_class=UserCreateSerializer,
        permission_classes=[AllowAny],
    )
    def signup(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


def assign_role(self, request, *args, **kwargs):
    user = self.get_object()
    serializer = RoleAssignSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
