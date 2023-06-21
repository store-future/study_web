from django.shortcuts import render,redirect
from .models import Room
from .form import RoomForm
from django.db.models import Q   # Q is a djago inbuit class which allow us to use IF/ELSE python statement 


'''IMPORTANT for home function
1- request.GET.get('q') = GET is taking the value( we define value  in home template by topic name ) from ride side of equal  (?q = value) from the google search bar url  and saving it into varible q    
2- if/else = if it found value then it display room according to query but if value is not given/not found it diplay all the rooms
3- 
'''
# displaying all the rooms into home page
def home(request):
    q = request.GET.get('q')  if request.GET.get('q') != None else '' 
    rooms = Room.objects.filter(                                        # it is displaying all the room on home page,side bar
                Q(topic__topic__icontains=q) |
                Q(name__icontains=q)         |
                Q(description__icontains=q)                 
            ) 
    topic = Room.objects.all()
    room_count= rooms.count()     # count gives length of th equery sets  (so rooms obj is here a query set )
    context = {"rooms":rooms , "topics":topic , "room_count":room_count}
    return render(request,"study/home.html" ,context )


# displaying all the rooom description in each room section
def room(request,id):
    room=Room.objects.get(pk=id)
    context = {"room":room}
    return render(request,"study/room.html",context)


# creating new room
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
def updateroom(request,id):
    room = Room.objects.get(pk=id)   # here we are fetching data from particular room id to make instance of it so that we can paas this data into blank form to achieve auto filled room with existing value
    form = RoomForm(instance=room)   # here instance is used to fill form with already exist room data
    context = {"form":form}
    
    if request.method=="POST":
        form = RoomForm(request.POST , instance=room )   # it means New data which is in request,post  will replace the old data (Instance-room )
        if form.is_valid:
            form.save()
            return redirect('home')    
    return render(request , "study/room-form.html" , context)


# delete the room 
def deleteroom(request,id):
    room = Room.objects.get(pk=id)
    
    if request.method=="POST":
        room.delete()
        return redirect('home')
    return render(request,"study/delete-room.html" , {"room":room})