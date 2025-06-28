from django.db.models import TextChoices


class ContentType(TextChoices):
    VIDEO = "video", "Video"
    DOCUMENT = "document", "Document"
    QUIZ = "quiz", "Quiz"
