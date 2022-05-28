from django.shortcuts import render

# Create your views here.
from .models import StudentClass
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# Create your views here.


class StudentClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentClass
        fields = '__all__'

class CreateStudentClassView(ListCreateAPIView):
    queryset = StudentClass.objects.all()
    serializer_class = StudentClassSerializer

class UpdateStudentClassView(RetrieveUpdateDestroyAPIView):
    queryset = StudentClass.objects.all()
    serializer_class = StudentClassSerializer