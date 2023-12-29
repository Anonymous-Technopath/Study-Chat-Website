from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from .models import Room,Topic
from.forms import RoomForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def loginPage(request):
    
    page='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"Username does not exist.")

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else :
            messages.error(request,"Username or password does not exist")

    context={'page':page}
    return render(request,'base/login_register.html',context)

def registerPage(request):

    form= UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration.')

    context={'form':form}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else '' # here is all is selected thne q will be empty string so every topic has an empty string in it
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)

    ) #it should atleast contain the given string in topic name, i with contains means not case sensitive

    topics = Topic.objects.all()


    return render(request,'base/home.html',{'rooms':rooms,'topics':topics})

def room(request,pk):
    room = Room.objects.get(id=pk)
    context = {'room':room}
    return render(request,'base/room.html',context)


@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save() # save in database
            return redirect('home') # redirect to home
    context ={'form':form}
    return render(request,'base/room_form.html',context)


@login_required(login_url='/login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user!=room.host:
        return HttpResponse('You are not allowed to update this room!')

    if request.method=='POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'base/room_form.html',context)


@login_required(login_url='/login')
def deleteRoom(request,pk):
    room =Room.objects.get(id=pk)

    if request.user!=room.host:
        return HttpResponse('You are not allowed to delete this room!')

    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})