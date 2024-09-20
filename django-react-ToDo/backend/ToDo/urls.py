from django.urls import path
from .views import *


urlpatterns = [
    path("TodoList" , TodoList    ),
    path("TodoList/add" , AddTodo ),
    

]
