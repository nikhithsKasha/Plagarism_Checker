from django.shortcuts import render

# Create your views here.
from .models import ClassActivity
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from student.models import StudentActivity
from studentclass.models import StudentClass,StudentEnrolled
from django.db.models import Q
from rest_framework.response import Response
import datetime

class StudentClassActivitySerializer(serializers.ModelSerializer):

    lecture_name = serializers.CharField(source='given_by.name')

    class Meta:
        model = ClassActivity
        fields = '__all__'

class CreateStudentClassActivityView(ListCreateAPIView):
    queryset = ClassActivity.objects.all()
    serializer_class = StudentClassActivitySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']
    filterset_fields = ['max_points', 'student_class']


class UpdateStudentClassActivityView(RetrieveUpdateDestroyAPIView):
    queryset = ClassActivity.objects.all()
    serializer_class = StudentClassActivitySerializer
    
class GetStudentPendingClassActivityView(APIView):
    

    def get(self, request, format=None):
        """
        Return a list of all assignments.
        """

        student_class = [x.student_class for x in StudentEnrolled.objects.filter(student=request.user, active=True)]
        activities = [i.activity for i in StudentActivity.objects.filter(student=request.user)]
        activities = ClassActivity.objects.filter(student_class__in=student_class, due_date__gt=datetime.datetime.now()).exclude(id__in=activities)
        activities_list = [StudentClassActivitySerializer(i).data for i in activities]

        return Response(activities_list)