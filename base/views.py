from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
from .models import Room,Topic,Message,User
from.forms import RoomForm,UserForm,MyUserCreationForm
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm

def loginPage(request):
    
    page='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method=='POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request,"Email does not exist.")

        user = authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else :
            messages.error(request,"Email or password does not exist")

    context={'page':page}
    return render(request,'base/login.html',context)

def registerPage(request):

    form= MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration.')

    context={'form':form}
    return render(request,'base/register.html',context)

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

    topics = Topic.objects.all()[:5]
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    return render(request,'base/home.html',{'rooms':rooms,'topics':topics,'room_messages':room_messages})

def room(request,pk):

    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created') # here we pick model Message and we get all the set of messages related to the specific room, class name will be small so name_set
    if request.method=='POST':
       message=Message.objects.create(
           user=request.user,
           room=room,
           body=request.POST.get('body')
       )
       room.participants.add(request.user)
       return redirect('room',pk=room.id)

    participants=room.participants.all()
    context = {'room':room,'room_messages':room_messages,'participants':participants}
    return render(request,'base/room.html',context)


@login_required(login_url='/login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        # form = RoomForm(request.POST)
        topic_name=request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host=request.user
        #     room.save()
        #     return redirect('home') # redirect to home

        Room.objects.create(
            host = request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')
    context ={'form':form,'topics':topics}
    return render(request,'base/room_form.html',context)


@login_required(login_url='/login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    
    if request.user!=room.host:
        return HttpResponse('You are not allowed to update this room!')

    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        form = RoomForm(request.POST,instance=room)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context={'form':form,'topics':topics,'room':room}
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


@login_required(login_url='/login')
def deleteMessage(request,pk):
    message =Message.objects.get(id=pk)

    if request.user!=message.user:
        return HttpResponse('You are not allowed to delete this room!')

    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':message})


def userProfile(request,pk):
    user =User.objects.get(id=pk)
    rooms= user.room_set.all()
    room_messages = user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST,request.FILES,instance=user)
        # print(request.POST)
        if form.is_valid() :
            form.save()
            return redirect("user-profile",pk=user.id)




    context={'form':form}
    return render(request,'base/update-user.html',context)


def viewTopics(request):
    
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    topics = Topic.objects.filter(name__icontains=q)

    context ={'topics':topics}
    return render(request,'base/topics.html',context)

def viewActivities(request):

    activity_messages=Message.objects.all()
    context={'activity_messages':activity_messages}

    return render(request,'base/activity.html',context)