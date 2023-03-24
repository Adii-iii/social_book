from rest_framework import serializers
from .models import Book

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'file', 'created_at')