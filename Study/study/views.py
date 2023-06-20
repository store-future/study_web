from django.shortcuts import render,redirect
from .models import Room
from.form import RoomForm




def home(request):
    rooms=Room.objects.all()
    context = {"rooms":rooms}
    return render(request,"study/home.html" ,context )


def room(request,id):
    room=Room.objects.get(pk=id)
    context = {"room":room}
    return render(request,"study/room.html",context)


def createroom(request):
    form = RoomForm()           # it is get blank form
    context = {"form":form}     # then used to display form into template
    
    if request.method=="POST":
        form=RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')
    return render(request , "study/room-form.html",context)


def updateroom(request,id):
    room = Room.objects.get(pk=id)
    form = RoomForm(instance=room)   # here instance is used to fill form with already exist room data
    context = {"form":form}
    
    if request.method=="POST":
        form = RoomForm(request.POST , instance=room )   # it means New data which is in request,post  will replace the old data (Instance-room )
        if form.is_valid:
            form.save()
            return redirect('home')    
    return render(request , "study/room-form.html" , context)



def deleteroom(request,id):
    room = Room.objects.get(pk=id)
    
    if request.method=="POST":
        room.delete()
        return redirect('home')
    return render(request,"study/delete-room.html" , {"room":room})