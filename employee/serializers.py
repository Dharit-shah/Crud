from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'groups']
#
#
# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'fname', 'lname', 'email', 'contact']

class ProductSerializer(serializers.ModelSerializer):
    user_id = EmployeeSerializer(many=False, read_only=True)
    class Meta:
        model = Product
        fields = ['user_id', 'id', 'name', 'categry']


#
# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Employee
#         fields = ['id', 'fname', 'lname', 'email', 'contact']