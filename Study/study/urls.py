from django.urls import path
from .views import *


urlpatterns=[
    path(   ""                     , home          , name="home"),
    
    path("room/<int:id>/"          , room          , name="room"),              # display inside room and deal with specific message    
    path("delete-message/<str:id>/", deletemessage , name="delete-message"),
    path("user-profile/<str:id>/"  ,  userprofile  , name="user-profile" ),
    
    path("create-room/"            , createroom    , name="create-room"),
    path("update-room/<str:id>"    , updateroom    , name="update-room"),
    path("delete-room/<str:id>"    , deleteroom    , name="delete-room"),
     
    path("login/"                  ,loginuser      , name="login"),
    path("logout/"                 ,logoutuser     , name="logout"),
    path("register/"               ,registeruser   , name="register")
    
]
 