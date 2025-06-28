from django.contrib import admin

from quizzes.models import Answer, Question, Submission

admin.register(Question)
admin.register(Answer)
admin.register(Submission)
