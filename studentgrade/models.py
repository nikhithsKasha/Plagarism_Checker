from django.db import models
from authentication.models import User
from studentactivity.models import ClassActivity

class StudentGrade(models.Model):

    activity = models.ForeignKey(to=ClassActivity, null=False, blank=False, on_delete=models.CASCADE)

    student = models.ForeignKey(to=User, null=False, blank=False, on_delete=models.CASCADE, related_name='student')

    given_by = models.ForeignKey(to=User,  null=False, blank=False, on_delete=models.CASCADE, related_name='lecturer')

    score = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.first_name + '-' + self.activity.name

    @property
    def student_name(self):
        return self.student.first_name

    @property
    def activity_name(self):
        return self.activity.name

