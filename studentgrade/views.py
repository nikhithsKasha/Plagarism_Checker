from django.shortcuts import render

# Create your views here.
from .models import StudentGrade
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class StudentGradeSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name')

    class Meta:
        model = StudentGrade
        fields = '__all__'

class CreateStudentGradeView(ListCreateAPIView):
    queryset = StudentGrade.objects.all()
    serializer_class = StudentGradeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['score']
    filterset_fields = ['activity', 'student']



class UpdateStudentGradeView(RetrieveUpdateDestroyAPIView):
    queryset = StudentGrade.objects.all()
    serializer_class = StudentGradeSerializer