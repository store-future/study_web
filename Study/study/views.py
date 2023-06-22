from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Room
from .form import RoomForm
from django.db.models import Q   # Q is a djago inbuit class which allow us to use IF/ELSE python statement 
from django.contrib.auth.models import User       #django builtin user model
from django.contrib.auth import  authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required      # it restrict some pages access ,to access these pages user have to login
from django.contrib.auth.forms import UserCreationForm         # inbuilt django user form





#login user
def loginuser(request):
    
    page='login'
    
    
    if request.user.is_authenticated:     # if user is already loggin in then thi condition  stops him to re-login
        return redirect('home')
    
    if request.method=="POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        
        try :                  # it is just checking whether user exist or not in our databse
            user = User.objects.get(username=username)
        except:
            messages.error(request,"User does not exist")
        
        
        user = authenticate(username=username , password=password)   #it will cross-check user detail and return none or not none 
        
        if user is not None:
            login(request,user)     #don't use capital u i user otherwie it will say an error abstract baseuser is missing one positional argument
            return redirect ("home")
        else:
            messages.error(request,"username or password does not exist")
        
    context = {"page":page}
    
    
    return render(request,"study/login_register.html" , context) 



# logout user
def logoutuser(request):
    
    logout(request)
    return redirect('home')



def registeruser(request):
    page='register'
    
    form = UserCreationForm()
    
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)        # it is freezing at the moment means not saving user immediatelt
            user.username =user.username.lower() 
            user.save()
            login(request,user)
            return redirect('login')
        else:
            messages.error(request,"An error occured during registration")
            
        
    context={"form":form}   
    return render(request,"study/login_register.html" , context)   
       
    







'''IMPORTANT for home function
1- request.GET.get('q') = GET is taking the value( we define value  in home template by topic name ) from ride side of equal  (?q = value) from the google search bar url  and saving it into varible q    
2- if/else = if it found value then it display room according to query but if value is not given/not found it diplay all the rooms
3- 
'''
# displaying all the rooms into home page
def home(request):
    q = request.GET.get('q')  if request.GET.get('q') != None else ''   # taking value from key-value pair , here q is key and it's value is room's topic
    rooms = Room.objects.filter(                                        # it is displaying all the room on home page,side bar
                Q(topic__topic__icontains=q) |
                Q(name__icontains=q)         |
                Q(description__icontains=q)                 
            ) 
    topic = Room.objects.all()
    room_count= rooms.count()     # count gives length of th query sets  (so room models is here a query set )
    context = { 
                "rooms":rooms ,
                "topics":topic , 
                "room_count":room_count
            }
    return render(request,"study/home.html" ,context )


# displaying all the rooom description in each room section
def room(request,id):
    room=Room.objects.get(pk=id)
    context = {"room":room}
    return render(request,"study/room.html",context)


# creating new room
@login_required(login_url=('login'))         #  decorator that restrict below function for  unlogged in user and try to send them on login page,login is required to acces that page
def createroom(request):
    form = RoomForm()           # it is get blank form
    context = {"form":form}     # then used to display form into template
    
    if request.method=="POST":
        form=RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')
    return render(request , "study/room-form.html",context)



# editing room with new value
@login_required(login_url=('login'))
def updateroom(request,id):
        
    room = Room.objects.get(pk=id)   # here we are fetching data from particular room id to make instance of it so that we can paas this data into blank form to achieve auto filled room with existing value
    form = RoomForm(instance=room)   # here instance is used to fill form with already exist room data
    context = {"form":form}
    
    
    if request.user != room.host:       # this condition restrict delete and editing functionlity those user who won't create that room 
       return HttpResponse("you are not authorised person")
    
    if request.method=="POST":
        form = RoomForm(request.POST , instance=room )   # it means New data which is in request,post  will replace the old data (Instance-room )
        if form.is_valid:
            form.save()
            return redirect('home')    
    return render(request , "study/room-form.html" , context)


# delete the room 
@login_required(login_url=('login'))
def deleteroom(request,id):

    room = Room.objects.get(pk=id)
    
   
    if request.user != room.host:       # this condition restrict delete and editing functionlity those user who won't create that room 
       return HttpResponse("you are not authorised person")
    
    
    if request.method=="POST":
        room.delete()
        return redirect('home')
    return render(request,"study/delete-room.html" , {"room":room})


