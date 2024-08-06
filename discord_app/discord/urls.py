from django.urls import path
from discord.views import Home , nav , signup ,login , logout



urlpatterns = [
    path("" , Home , name = 'home'),
    path("nav/" , nav , name = 'nav'),
    path("signup/" , signup , name = 'signup'),
    path("login/" , login , name = 'login'),
    path("logout/" , logout , name = 'logout'),
    

]

