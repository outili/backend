from django.contrib.auth import get_user_model
from django.db import models

from core.models import BaseModel
from courses.enums import ContentType

User = get_user_model()


def course_content_upload_path(instance, filename):
    return f"courses/{instance.course.id}/{filename}"


class Course(BaseModel):
    title = models.CharField()
    description = models.TextField()
    instructor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="courses"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Content(BaseModel):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="contents"
    )
    content_type = models.CharField(
        choices=ContentType.choices,
        default=ContentType.VIDEO,
    )
    title = models.CharField()
    file = models.FileField(upload_to=course_content_upload_path)
    order = models.PositiveIntegerField()

    class Meta:
        unique_together = ["course", "order"]

    def __str__(self):
        return self.title


class Enrollment(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="enrollments",
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "course"]

    def __str__(self):
        return f"{self.user}: {self.course} - {self.enrolled_at}"


class Progress(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="progresses",
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="progresses"
    )
    content = models.ForeignKey(
        Content, on_delete=models.CASCADE, related_name="progresses"
    )
    is_completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "course", "content"]

    def __str__(self):
        return (
            f"{self.user}: {self.content} ({self.course}) "
            f"- {'completed' if self.is_completed else 'in_progress'}"
        )
