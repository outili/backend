from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models

from core.models import BaseModel
from courses.models import Content

User = get_user_model()


class Question(BaseModel):
    content = models.ForeignKey(
        Content, on_delete=models.CASCADE, related_name="questions"
    )
    text = models.TextField()
    multiple_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Answer(BaseModel):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Submission(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="quiz_submissions"
    )
    content = models.ForeignKey(
        Content, on_delete=models.CASCADE, related_name="submissions"
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        unique_together = ["user", "content"]

    def __str__(self):
        return f"{self.user}: {self.content} - {self.score}"
