from django.shortcuts import render
from .models import User
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework import status
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import logout
# Create your views here.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'role')
        write_only_fields = ('password',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role= validated_data['role'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)


class CreateUserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UpdateUserView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@csrf_exempt
@api_view(('POST',))
def api_logout(request):
    try:
        request.user.auth_token.delete()
    except Exception as e:
        pass
    logout(request)
    return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(('GET',))
def getCurrentUser(request):

    return Response({
        'role': request.user.role,
        'name': request.user.first_name +' ' + request.user.last_name,
        'email': request.user.email
    })