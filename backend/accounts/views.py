from django.shortcuts import render
from rest_framework.generics import GenericAPIView,ListCreateAPIView,UpdateAPIView,ListAPIView
from rest_framework.permissions import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from .models import *

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
        
#To list a User's Profile (common to both students and professors) 
class UserDetailsL(ListAPIView):
    serializer_class = UserDetailsSerializer
    permission_classes=(IsAuthenticated,)
    def get_queryset(self):
        try:
            user = self.request.user
            return App_User.objects.filter(email=user)
        except:
            return Response({'status':403,'message': 'Some error has occured'})

#To Update a User's profile (pk must be equal to self.request.user)
class UserDetailsU(UpdateAPIView):
    serializer_class = UserDetailsSerializer
    permission_classes=(IsAuthenticated,)
    def get_queryset(self):
        try:
            user = self.request.user
            return App_User.objects.filter(email=user)
        except:
            return Response({'status':403,'message': 'Some error has occured'})

#To list and create professor pending profile (create or list ProfessorMore) 
class ProfessorDetailsLC(ListCreateAPIView):
    serializer_class = ProfessorDetailsSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
            try:
                user = self.request.user
                return ProfessorMore.objects.filter(user=user)
            except:
                return Response({'status':403,'message': 'Some error has occured'})
    
    def perform_create(self,serializer):
        try:
            user = self.request.user
            print(user)
            serializer.save(user=user)
            return Response(serializer.data)
        except:
            return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})

#To Update Professor pending profile (pk must be equal to self.request.user)
class ProfessorDetailsU(UpdateAPIView):
    serializer_class = ProfessorDetailsSerializer
    permission_classes=(IsAuthenticated,)
    def get_queryset(self):
        try:
            user = self.request.user
            return ProfessorMore.objects.filter(user=user)
        except:
            return Response({'status':403,'message': 'Some error has occured'})
