from django.shortcuts import render, redirect
from django.contrib import messages # flash messages
from django.http import HttpResponse
from django.db.models import Q # for search queries
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm

# Create your views here.
# function based views -- Class based views are also possible

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()  # get the username from the form
        password = request.POST.get('password')  # get the password from the form
        # Attempt to retrieve the user; handle case where user does not exist
        try:
            user = User.objects.get(username=username)
            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # creates a session in the db and browser
                return redirect('home')  # redirect to the home page
            else:
                messages.error(request, 'Username or Password is incorrect')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')  # flash message if user is not found

    context = {'page': page}
    return render(request, 'base/login_register.html', context)  # Make sure to complete the template name correctly

def LogoutUser(request):
    logout(request) # deletes the token and user session
    return redirect('home')

def registerUser(request):
    page = 'register'
    form = UserCreationForm() # create a form object

    if request.method == "POST":
        form = UserCreationForm(request.POST) # get the form data
        if form.is_valid():
            user = form.save(commit=False) # does not immediately save to db
            # clean the form input data
            user.username = user.username.lower() # convert username to lowercase
            user.save()
            login(request, user) # login the user just created
            return redirect('home')
        else:
            messages.error(request, 'Error during registration')

    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' # inline if else to get query from URL (search)
    rooms = Room.objects.filter(Q(topic__name__icontains = q) | # search by topic or name or description
                                Q(topic__name__icontains = q) |
                                Q(description__icontains = q)) # makes sure the topic name contains the query
    topics = Topic.objects.all()
    room_count = rooms.count() # get the count of rooms
    context = {'rooms': rooms,  'topics': topics, 'room_count' : room_count} # create a context dictionary for the passed data
    return render(request, 'base/home.html', context) # third arg expected as a dictionary {'rooms': rooms}

def room(request, pk):
    q = request.GET.get('q') # get the query from the url
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    # query all messages from the room, also order by created date desc

    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room, 
            body = request.POST.get('body') # the form's name = 'body'
        )
        room.participants.add(request.user) # add the user to the room
        return redirect('room', pk = room.id) # reload the page
    
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

@login_required(login_url= 'login') # check if user is logged in and redirect to login page if not
def createRoom (request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save() # saves to db
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url= 'login') # check if user is logged in and redirect to login page if not
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room) # the form will be pre filled with the room data

    if request.user != room.host: # check if the user is the owner of the room
        return HttpResponse('You are not the owner of this room')

    if request.method == "POST":
        form = RoomForm(request.POST, instance = room) # new POST data will replace the room object data in the room variable
        if form.is_valid: # checks if form is valid
            form.save() # saves to db
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url= 'login') # check if user is logged in and redirect to login page if not
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host: # check if the user is the owner of the room
        return HttpResponse('You are not the owner of this room')
    if request.method == "POST":
        room.delete() # delete this object from the db
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url= 'login') # check if user is logged in and redirect to login page if not
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    # if request.user != Message.user: # check if the user is the owner of the message
    #     return HttpResponse('This is not your message')
    if request.method == "POST":
        message.delete() # delete this object from the db
        return redirect('room', pk = message.room.id) # redirect to the room page
    return render(request, 'base/delete.html', {'obj':message})