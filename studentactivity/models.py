from django.db import models
from studentclass.models import StudentClass
from authentication.models import User
# Create your models here.

class ClassActivity(models.Model):

    name = models.CharField(max_length=255, blank=False, null=False)

    number = models.IntegerField(null=False, blank=False)

    max_points = models.IntegerField(blank=False, null=False)

    due_date = models.DateTimeField(blank=False, null=False)

    instructions = models.TextField(null=False, blank=False)

    student_class = models.ForeignKey(to=StudentClass, null=True,  blank=True, on_delete=models.SET_NULL, related_name='student_class')

    given_by = models.ForeignKey(to=User, null=True,  blank=True, on_delete=models.SET_NULL, related_name='lecturer_name')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ' ' + str(self.number)

