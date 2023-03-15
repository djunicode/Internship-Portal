from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Internship
from .serializers import InternshipSerializer

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