from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from courses.enums import ContentType
from courses.models import Content
from quizzes.models import Answer, Question, Submission

User = get_user_model()


class QuestionFilter(filters.FilterSet):
    quiz = filters.ModelChoiceFilter(
        field_name="content__id",
        queryset=Content.objects.filter(content_type=ContentType.QUIZ),
        to_field_name="id",
        help_text="Filter by the ID of the Quiz",
    )

    class Meta:
        model = Question
        fields = []


class AnswerFilter(filters.FilterSet):
    question = filters.ModelChoiceFilter(
        field_name="question__id",
        queryset=Question.objects.filter(),
        to_field_name="id",
        help_text="Filter by the ID of the Question",
    )

    class Meta:
        model = Answer
        fields = []


class SubmissionFilter(filters.FilterSet):
    quiz = filters.ModelChoiceFilter(
        field_name="content__id",
        queryset=Content.objects.filter(content_type=ContentType.QUIZ),
        to_field_name="id",
        help_text="Filter by the ID of the Quiz",
    )
    user = filters.ModelChoiceFilter(
        field_name="user__id",
        queryset=User.objects.all(),
        to_field_name="id",
        help_text="Filter by the ID of the User",
    )
    submitted_at = filters.DateTimeFromToRangeFilter(
        field_name="submitted_at",
        help_text="Filter by the date-time of submission",
    )
    score = filters.NumericRangeFilter(
        field_name="score",
        help_text="Filter by the score of the submission",
    )

    class Meta:
        model = Submission
        fields = []
