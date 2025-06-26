from django_filters import rest_framework as filters

from users.models import User


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = []

    is_student = filters.BooleanFilter(field_name="is_student")
    is_instructor = filters.BooleanFilter(field_name="is_instructor")
