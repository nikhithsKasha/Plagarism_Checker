from django.shortcuts import render
from .models import StudentActivity
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django.conf import settings
import os
from .pysimilar import compare

class StudentActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentActivity
        fields = '__all__'

    def create(self, validated_data):
        try:
            activity = StudentActivity.objects.get(
            student=validated_data.get('student', None),
            activity= validated_data.get('activity', None)
            )
            return super().update(activity, validated_data)
        except StudentActivity.DoesNotExist:
            return super().create(validated_data)
        

class CreateStudentActivityView(ListCreateAPIView):
    queryset = StudentActivity.objects.all()
    serializer_class = StudentActivitySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]


class UpdateStudentActivityView(RetrieveUpdateDestroyAPIView):
    queryset = StudentActivity.objects.all()
    serializer_class = StudentActivitySerializer

class checkPlagiarism(RetrieveAPIView):
    queryset = StudentActivity.objects.all()
    serializer_class = StudentActivitySerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        path = serializer.data['document'].replace('http://localhost:8001' , os.path.abspath(os.path.dirname(__name__)))
        print(path)
        others_submission = StudentActivity.objects.filter(activity=serializer.data['activity']).exclude(id=serializer.data['id'])
        for sub in others_submission:
            print(sub.document)

        da = [ {'id': sub.id, 'student': sub.student.first_name, 'match_percentage':compare(path, os.path.abspath(os.path.dirname(__name__)) + '/media/' + str(sub.document), isfile=True) } for sub in others_submission]


        # d = compare(
        #     '/home/tapclicks/Desktop/Plagiarism-checker-Python-master/fatma.txt',
        #      '/home/tapclicks/Desktop/Plagiarism-checker-Python-master/john.txt',
        #       isfile=True
        #       )
        return Response({
            "data":da
        })