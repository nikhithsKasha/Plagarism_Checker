from django.contrib import admin
from .models import StudentClass, StudentEnrolled
# Register your models here.

admin.site.register(StudentClass)
admin.site.register(StudentEnrolled)