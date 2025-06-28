from decimal import Decimal

from rest_framework import serializers

from courses.enums import ContentType
from courses.models import Content, Progress
from quizzes.models import Answer, Question, Submission


class QuestionSerializer(serializers.ModelSerializer):
    content = serializers.PrimaryKeyRelatedField(
        queryset=Content.objects.filter(content_type=ContentType.QUIZ)
    )

    class Meta:
        model = Question
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"


class SubmissionSerializer(serializers.ModelSerializer):
    content = serializers.PrimaryKeyRelatedField(
        queryset=Content.objects.filter(content_type=ContentType.QUIZ)
    )
    answers = serializers.DictField(
        child=serializers.ListField(child=serializers.UUIDField()),
        help_text="Mapping of question_id to selected answer_id(s)",
        write_only=True,
    )

    class Meta:
        model = Submission
        fields = "__all__"
        read_only_fields = ["id", "submitted_at", "score", "user"]

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user
        content = validated_data["content"]
        submitted_answers = validated_data.pop("answers")

        correct_answers = 0
        total_questions = 0

        for question_id, selected_ids in submitted_answers.items():
            try:
                question = Question.objects.get(id=question_id, content=content)
            except Question.DoesNotExist as err:
                raise serializers.ValidationError(
                    {"answers": f"Question with id {question_id} does not exist"}
                ) from err

            correct_ids = list(
                question.answers.filter(is_correct=True).values_list("id", flat=True)
            )
            if set(selected_ids) == set(correct_ids):
                correct_answers += 1
            total_questions += 1

        score = (
            correct_answers / total_questions
            if total_questions > 0
            else Decimal("0.00")
        )

        submission = Submission.objects.create(user=user, content=content, score=score)

        # Mark the quiz content as completed in Progress
        Progress.objects.update_or_create(
            user=user,
            course=content.course,
            content=content,
            defaults={"is_completed": True},
        )

        return submission
