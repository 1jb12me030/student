
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

from rest_framework.serializers import ModelSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(required=True)
    class Meta:
        model=Registration
        fields=['id','email','username','password','mobile_no']

    def create(self, validated_data):
        password=validated_data['password']
        obj=Registration.objects.create(
            username=validated_data['username'],
            mobile_no=validated_data['mobile_no'],
            email=validated_data['email'],
            password=password
        )
        obj.set_password(password)
        obj.save()
        return obj
    
class RegistrationSerializer1(serializers.ModelSerializer):
    class Meta:
        model=Registration
        fields=['location','gender','profile_pic','email','mobile_no']
    

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)
    
    
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'    
