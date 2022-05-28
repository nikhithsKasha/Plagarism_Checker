from django.db import models
from authentication.models import User
from studentactivity.models import ClassActivity
from os.path import splitext

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT
    file_name,extension = splitext(filename)
    return 'submissions/student_{0}_{1}{2}'.format(instance.student.id, instance.activity.id, extension)

class StudentActivity(models.Model):

    student = models.ForeignKey(to=User, null=True, blank=False, on_delete=models.SET_NULL)

    activity = models.ForeignKey(to=ClassActivity, null=True, blank=False, on_delete=models.SET_NULL)

    document = models.FileField(upload_to=user_directory_path)

    description = models.TextField(null=True, blank=True)

    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.student.first_name + self.activity.name