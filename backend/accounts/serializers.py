from rest_framework import serializers
from .models import *
from rest_framework.validators import UniqueValidator
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=App_User.objects.all())])
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = App_User
        fields = [
            "email",
            "first_name",
            "last_name",
            "dept_name",
            "contact_number",
            "type",
            "password",
        ]


        def create(self, validated_data):
            user = App_User.objects.create(
                email = validated_data['email'],
                first_name = validated_data['first_name'],
                last_name = validated_data['last_name'],
                dept_name = validated_data['dept_name'],
                contact_number = validated_data['contact_number'],
                type = validated_data['type']
            )
            user.set_password(validated_data['password'])
            user.save()
            return user
    

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)
    tokens = serializers.CharField(max_length=255, read_only=True)
    message = serializers.CharField(max_length=255, read_only=True)
    type = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = App_User
        fields = ['message', 'email', 'type', 'password', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', )
        password = attrs.get('password', )

        request_user = auth.authenticate(email=email, password=password)
        user = App_User.objects.get(email=email)

        if not request_user:
            raise AuthenticationFailed('Invalid credintials, try again')
        if not request_user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        
        return {
            'message' : 'User Logged in', 
            'email' : request_user.email,
            'type' : request_user.type,
            'tokens' : Token.objects.get_or_create(user=user)[0].key
        }

class UserDetailsSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='App_User.email')
    class Meta:
        model=App_User
        fields=['email','first_name','last_name','dept_name','contact_number','profile_picture']

class ProfessorDetailsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='professor.email')
    class Meta:
        model = ProfessorMore
        fields=['user','joining_year','designation','cv']