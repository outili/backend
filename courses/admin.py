from django.contrib import admin

from courses.models import Content, Course, Enrollment, Progress

admin.register(Course)
admin.register(Content)
admin.register(Enrollment)
admin.register(Progress)
