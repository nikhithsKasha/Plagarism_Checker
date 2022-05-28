from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
ROLES = (
    ('S', 'Student'),
    ('L', 'Lecturer'),
    (None, 'Unknown'),
)

class User(AbstractUser):

    role = models.CharField(default=None, null=True, blank=True, choices=ROLES, max_length=7)

    phone = models.CharField(max_length=255, blank=True, null=True)

    address = models.CharField(max_length=255, blank=True, null=True)

    code = models.CharField(max_length=255, blank=True, null=True, unique=True)


    @property
    def name(self):
        return self.get_full_name()