from django.urls import path
from .views import *


urlpatterns = [
    path("TodoList" , TodoList    ),
    path("TodoList/add" , AddTodo ),
    path("TodoList/<int:pk>/update" , updateTodo ),
    path("TodoList/<int:pk>/delete" , deleteTodo)
]
