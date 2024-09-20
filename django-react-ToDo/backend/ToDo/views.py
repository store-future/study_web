from django.shortcuts import render 
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status

from .models import TodoModel
from .serializers import TodoSerializer


@api_view(['GET'])
def TodoList(request):
    Todo = TodoModel.objects.all() 
    serializer = TodoSerializer(Todo , many = True)
    return Response(serializer.data)


@api_view(['POST'])
def AddTodo(request):
    serializer = TodoSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data , status.HTTP_201_CREATED)
    return Response(serializer.data , status = status.HTTP_400_BAD_REQUEST)


