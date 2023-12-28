from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from .models import Room,Topic
from.forms import RoomForm

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else '' # here is all is selected thne q will be empty string so every topic has an empty string in it
    rooms=Room.objects.filter(topic__name__icontains=q) #it should atleast contain the given string in topic name, i with contains means not case sensitive

    topics = Topic.objects.all()


    return render(request,'base/home.html',{'rooms':rooms,'topics':topics})

def room(request,pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request,'base/room.html',context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save() # save in database
            return redirect('home') # redirect to home
    context ={'form':form}
    return render(request,'base/room_form.html',context)

def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)


    if request.method=='POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'base/room_form.html',context)

def deleteRoom(request,pk):
    room =Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})