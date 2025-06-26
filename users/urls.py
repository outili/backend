from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from users.views import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, "user")

urlpatterns = [
    path("", include(router.urls)),
    path("users/login", TokenObtainPairView.as_view(), name="login"),
    path("users/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/token/verify", TokenVerifyView.as_view(), name="token_refresh"),
]
