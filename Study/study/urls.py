from django.urls import path
from .views import *


urlpatterns=[
    path(   ""                   , home        , name="home"),
    path("room/<int:id>/"        , room        , name="room"),
    path("create-room/"          , createroom  , name="create-room"),
    path("update-room/<str:id>"  , updateroom  , name="update-room"),
    path("delete-room/<str:id>"  , deleteroom  , name="delete-room"),
    
]
 