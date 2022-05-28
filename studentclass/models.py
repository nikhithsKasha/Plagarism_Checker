from django.db import models
from authentication.models import User
# Create your models here.

class StudentClass(models.Model):

    name = models.CharField(max_length=255, blank=False, null=False)

    number = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.name + ' ' + self.number
    

class StudentEnrolled(models.Model):

    student = models.ForeignKey(to=User, null=False, blank=False, on_delete=models.CASCADE)

    student_class = models.ForeignKey(to=StudentClass, null=False, blank=False, on_delete=models.CASCADE)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.student.first_name + '-' + self.student_class.name
