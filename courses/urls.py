from rest_framework.routers import DefaultRouter

from courses.views import (
    ContentViewSet,
    CourseViewSet,
    EnrollmentViewSet,
    ProgressViewSet,
)

router = DefaultRouter()

router.register("courses", CourseViewSet, basename="course")
router.register("enrollments", EnrollmentViewSet, basename="enrollment")
router.register("content", ContentViewSet, basename="content")
router.register("progresses", ProgressViewSet, basename="progress")

urlpatterns = router.urls
