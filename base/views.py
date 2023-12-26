from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from .models import Room
from.forms import RoomForm

def home(request):
    rooms = Room.objects.all()
    return render(request,'base/home.html',{'rooms':rooms})

def room(request,pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request,'base/room.html',context)

def createRoom(request):
    form = RoomForm()
    if request.method=='POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save() # save in database
            return redirect('home') # redirect to home
    context ={'form':form}
    return render(request,'base/room_form.html',context)

