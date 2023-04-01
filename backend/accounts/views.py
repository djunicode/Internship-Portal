from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout


class RegisterApi(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = RegistrationSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        Data = {}
        user_data = serializer.data
        request_user = App_User.objects.get(email=user_data['email'])
        token = Token.objects.get_or_create(user=request_user)[0].key
        Data['Message'] = 'User registered successfully'
        Data['Email'] = user_data['email']
        Data['Type'] = user_data['type']
        Data['Token'] = token
        
        return Response(Data, status=status.HTTP_201_CREATED)


class LoginApi(GenericAPIView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutApi(GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response('User Logged out successfully')