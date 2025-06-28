from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from courses.enums import ContentType
from courses.models import Content, Course, Enrollment, Progress

User = get_user_model()


class CourseFilter(filters.FilterSet):
    instructor = filters.ModelMultipleChoiceFilter(
        field_name="instructor__id",
        queryset=User.objects.filter(is_instructor=True),
        to_field_name="id",
        help_text="Filter by the ID of instructor",
    )
    created_at = filters.DateTimeFromToRangeFilter(
        field_name="created_at",
        help_text="Filter by the date-time of creation",
    )

    class Meta:
        model = Course
        fields = []


class ContentFilter(filters.FilterSet):
    course = filters.ModelMultipleChoiceFilter(
        field_name="course__id",
        queryset=Course.objects.filter(),
        to_field_name="id",
        help_text="Filter by the ID of course",
    )
    content_type = filters.MultipleChoiceFilter(choices=ContentType.choices)

    class Meta:
        model = Content
        fields = []


class EnrollmentFilter(filters.FilterSet):
    user = filters.ModelMultipleChoiceFilter(
        field_name="user__id",
        queryset=User.objects.filter(),
        to_field_name="id",
        help_text="Filter by the ID of user",
    )
    course = filters.ModelMultipleChoiceFilter(
        field_name="course__id",
        queryset=Course.objects.filter(),
        to_field_name="id",
        help_text="Filter by the ID of course",
    )
    enrolled_at = filters.DateTimeFromToRangeFilter(
        field_name="enrolled_at",
        help_text="Filter by the date-time of enrolment",
    )

    class Meta:
        model = Enrollment
        fields = []


class ProgressFilter(filters.FilterSet):
    user = filters.ModelMultipleChoiceFilter(
        field_name="user__id",
        queryset=User.objects.filter(),
        to_field_name="id",
        help_text="Filter by the ID of user",
    )
    course = filters.ModelMultipleChoiceFilter(
        field_name="course__id",
        queryset=Course.objects.filter(),
        to_field_name="id",
        help_text="Filter by the ID of course",
    )

    class Meta:
        model = Progress
        fields = []
