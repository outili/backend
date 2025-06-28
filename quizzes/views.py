from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from quizzes.filters import AnswerFilter, QuestionFilter, SubmissionFilter
from quizzes.models import Answer, Question, Submission
from quizzes.serializers import (
    AnswerSerializer,
    QuestionSerializer,
    SubmissionSerializer,
)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuestionFilter


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnswerFilter


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    http_method_names = ["post", "get"]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = SubmissionFilter
    ordering_fields = ["score", "submitted_at"]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="ordering",
                description="Field to order by (use prefix '-' for descending order).",
                enum=ordering_fields + [f"-{field}" for field in ordering_fields],
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
