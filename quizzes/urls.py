from rest_framework.routers import DefaultRouter

from quizzes.views import AnswerViewSet, QuestionViewSet, SubmissionViewSet

router = DefaultRouter()

router.register("questions", QuestionViewSet, basename="question")
router.register("answers", AnswerViewSet, basename="answer")
router.register("submissions", SubmissionViewSet, basename="submission")
urlpatterns = router.urls
