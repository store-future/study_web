from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .form import RoomForm
from django.db.models import Q   # Q is a djago inbuit class which allow us to use IF/ELSE python statement 
from django.contrib.auth.models import User       #django builtin user model
from django.contrib.auth import  authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required      # it restrict some pages access ,to access these pages user have to login
from django.contrib.auth.forms import UserCreationForm         # inbuilt django user form



# --------------------------------------------------------Start of login logout --------------------------------------------------------------------------------------------------------


#login user
def loginuser(request):
    
    page='login'
    
    
    if request.user.is_authenticated:     # if user is already logged in then thi condition  stops him to re-login
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
       
    



# --------------------------------------------------------End of login logout --------------------------------------------------------------------------------------------------------





# --------------------------------------------------------Start of Home ,  --------------------------------------------------------------------------------------------------------

'''IMPORTANT for home function
1- request.GET.get('q') = GET is taking the value( we define value  in home template by topic name ) from ride side of equal  (?q = value) from the google search bar url  and saving it into varible q    
2- if/else = if it found value then it display room according to query but if value is not given/not found it diplay all the rooms
3- 
'''
# displaying all three section - topic , rooms , recent activity
def home(request):
    
    
   # 1- it is displaying all the topics on the home page
    topic = Room.objects.all()
   
   
    # 2- displaying all the rooms (both type - topic  wise and  all) according to query and also helpful in search bar
    q = request.GET.get('q')  if request.GET.get('q') != None else ''   # taking value from key-value pair , here q is key and it's value is room's topic
    rooms = Room.objects.filter(                                        # it is displaying all the room on home page,side bar
                Q(topic__topic__icontains=q) |
                Q(name__icontains=q)         |
                Q(description__icontains=q)                 
            ) 
    
    
    room_count= rooms.count()     # count gives length of th query sets  (so room models is here a query set )
    
    
    # 3-it is displaying all the recent activity section into home 
    room_message = Message.objects.filter(Q(room__topic__topic__icontains=q))  # if it receives q value then show message accoding to that otherwise show all the messages in new first order

    
    
    context = { 
                "rooms":rooms ,
                "topics":topic , 
                "room_count":room_count,
                "room_messages":room_message,
            }
    return render(request,"study/home.html" ,context )





# displaying all the information inside of a specific  rooom 
def room(request,id):
    room=Room.objects.get(pk=id)                                    
    room_message = room.message_set.all().order_by('-created')      # sytax = parentmodel.childmodel_set.all()  it is giving us a set of all messagemodel that are related to that specific room (note- here we write Message model in lower case with underscore set)
   
   
    # we use create instead of save because it is  creating  actual message model with defined field (user,room,body) 
    if request.method=="POST":
        
        message = Message.objects.create(
                    user = request.user,
                    room =room,
                    body =request.POST.get('body')
                )
        return redirect('room' , id=room.pk)     # here id is sent to our room redirection
       
   
    context = {"room":room , "room_messages":room_message}
    return render(request,"study/room.html",context)




def userprofile(request,id):
    
    # displaying all the rooms releted to specific user
    user = User.objects.get(pk=id)
    rooms = host.room_set.all()
    return render(request,"study/profile.html")











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


# view  for deleting comments/message
@login_required(login_url=('login'))
def deletemessage(request,id):

    message = Message.objects.get(pk=id)
    
   
    if request.user != message.user:       # this condition restrict delete and editing functionlity those user who won't create that room 
       return HttpResponse("you are not authorised person")
    
    
    if request.method=="POST":
        message.delete()
        return redirect('home')
    
    return render(request,"study/delete-room.html" , {"room":room})


