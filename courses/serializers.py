from rest_framework import serializers

from courses.models import Content, Course, Enrollment, Progress
from users.serializers import UserSerializer


class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    is_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_is_enrolled(self, obj) -> bool:
        request = self.context.get("request")
        if not request.user or not request.user.is_authenticated:
            print("no user")
            return False
        if not hasattr(obj, "enrollments"):
            print("no users")
            return False
        print("no user")
        return obj.enrollments.filter(user__id=request.user.id).exists()


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = "__all__"


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = "__all__"
