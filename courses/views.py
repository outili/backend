from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated

from courses.filters import (
    ContentFilter,
    CourseFilter,
    EnrollmentFilter,
    ProgressFilter,
)
from courses.models import Content, Course, Enrollment, Progress
from courses.serializers import (
    ContentSerializer,
    CourseSerializer,
    EnrollmentSerializer,
    ProgressSerializer,
)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    filterset_class = CourseFilter
    search_fields = ["title", "description", "instructor__name"]
    ordering_fields = ["title", "instructor__name", "created_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == "my":
            user = self.request.user
            queryset = queryset.filter(enrollments__user=user)
        return queryset

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.action == "my":
            permissions = [IsAuthenticated()]
        return permissions

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

    @extend_schema(responses=CourseSerializer(many=True))
    @action(detail=False, methods=["GET"])
    def my(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]
    filterset_class = ContentFilter
    searching_fields = ["title"]
    ordering_fields = ["order"]

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


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    filterset_class = EnrollmentFilter
    search_fields = ["course__title", "course__description", "course__instructor__name"]
    ordering_fields = [
        "course__title",
        "course__instructor__name",
        "course__created_at",
        "enrolled_at",
    ]

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


class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProgressFilter
    ordering_fields = ["content__order"]

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
