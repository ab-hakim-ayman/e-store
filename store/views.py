from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q
from django.utils import timezone
from .models import *
from .serializers import *


class CategoryView(APIView):
    def get(self, request):
        context = {
            'request':request
        }
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context= context)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)