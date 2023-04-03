from django.shortcuts import render
from rest_framework.permissions import *
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView,ListCreateAPIView
from django.core.exceptions import PermissionDenied

class InternshipList(APIView):
    def get(self, request):
        Contacts = Internship.objects.all()
        serializer = InternshipSerializer(Contacts, many=True)
        return Response(serializer.data)
    def post(self, request):
        pass

class InternshipDetail(APIView):
    def get(self, request, pk):
        Contacts = Internship.objects.get(id=pk)
        serializer = InternshipSerializer(Contacts, many=False)
        return Response(serializer.data)
    def post(self):
        pass

#To display Research Project Lists to all students
class Research_ProjectList(ListAPIView):
    serializer_class = Research_ProjectSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Research_Project

#If a Professor wants to add Research Projects
class Research_ProjectLC(ListCreateAPIView):
    serializer_class = Research_ProjectSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        if self.request.user is Professor:
            try:
                user = self.request.user
                return Research_Project.objects.filter(professor=user)
            except:
                return Response({'status':403,'message': 'Some error has occured'})
        else:
            raise PermissionDenied
        
    def perform_create(self,serializer):
        if self.request.user is Professor:
            try:
                user = self.request.user
                print(user)
                serializer.save(professor=user)
                return Response(serializer.data)
            except:
                return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})
        else:
            raise PermissionDenied

#If a Professor wants to update or delete a Research Project under him/her        
class Research_ProjectRUD(RetrieveUpdateDestroyAPIView):
    serializer_class = Research_ProjectSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        if self.request.user is Professor:
            try:
                user = self.request.user
                return Research_Project.objects.filter(professor=user)
            except:
                return Response({'status':403,'message': 'Some error has occured'})
        else:
            raise PermissionDenied        