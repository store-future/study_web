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



@api_view(['PUT'])
def updateTodo(request ,pk):
    try :
        todo = TodoModel.objects.get(pk=pk)
    except:
        return Response(status= status.HTTP_404_NOT_FOUND)
    
    if 'status' in request.data:
        # print(f"todo object {todo.__dict__} , api data {request.data}")
        todo.status = request.data['status']
        todo.save()
        serializer = TodoSerializer(todo)
        return Response(serializer.data)


@api_view(['PUT'])
def deleteTodo(request ,pk):
    try :
        todo = TodoModel.objects.get(pk=pk)
    except:
        return Response(status= status.HTTP_404_NOT_FOUND)
    
    if 'status' in request.data:
        # print(f"todo object {todo.__dict__} , api data {request.data}")
        todo.status = request.data['status']
        todo.save()
        serializer = TodoSerializer(todo)
        return Response(serializer.data)


@api_view(['DELETE'])
def deleteTodo(request ,pk):
    try :
        todo = TodoModel.objects.get(pk=pk)
    except:
        return Response(status= status.HTTP_404_NOT_FOUND)
    # print(f"todo object {todo.__dict__} , api data {request.data}")
    todo.delete()
    return Response(status.HTTP_204_NO_CONTENT)
