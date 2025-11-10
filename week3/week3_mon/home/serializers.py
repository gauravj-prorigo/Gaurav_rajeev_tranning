from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class peopleserilazers(serializers.ModelSerializer):
    
    class Meta:
        model = person
        fields = '__all__'
        
        
class blogserilazers(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'     
        
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True) 
    
    class Meta:
        model = loginuser    
        fields = ['username', 'email', 'password', 'role']

        
    def create(self,validated_data):
        user = loginuser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            role=validated_data.get('role', 'user'),
        )  
        
        return user          
    
    
    
class LoginSerialize(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)  
    
    def validate(self,data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        
        if not user:
                raise serializers.ValidationError("Invalid username or password")

        data['user'] = user  
        return data
    
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'completed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        title = validated_data.get('title', '').strip()
        if not title:
            raise serializers.ValidationError({"title": "This field may not be blank."})
        return Task.objects.create(title=title)    