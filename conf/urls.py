from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^api/(?P<version>v[0-9]+)/", include("users.urls")),
    # Documentation
    re_path(
        r"^api/(?P<version>v[0-9]+)/schema$",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    re_path(
        r"^doc/$", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    re_path(r"^redoc/$", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
