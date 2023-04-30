from rest_framework import serializers
from .models import Internship,Research_Project

class InternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = '__all__'

class Research_ProjectSerializer(serializers.ModelSerializer):
    professor = serializers.ReadOnlyField(source='professor.email')
    class Meta:
        model = Research_Project
        fields = '__all__'