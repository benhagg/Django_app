from django.shortcuts import render, redirect
from django.contrib import messages # flash messages
from django.http import HttpResponse
from django.db.models import Q # for search queries
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm

# Create your views here.
# function based views -- Class based views are also possible

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get('email').lower()  # get the username from the form
        password = request.POST.get('password')  # get the password from the form
        # Attempt to retrieve the user; handle case where user does not exist
        try:
            user = User.objects.get(email=email)
            # Authenticate the user
            user = authenticate(request, email=email, password=password)
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
    # page = 'register' delete if this works
    form = MyUserCreationForm() # create a form object

    if request.method == "POST":
        form = MyUserCreationForm(request.POST) # get the form data
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
    topics = Topic.objects.all()[0:5] # get the first 5 topics
    room_messages = Message.objects.all() # get all messages
    room_count = rooms.count() # get the count of rooms
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))

    context = {'rooms': rooms,  'topics': topics, 'room_count' : room_count, 'room_messages': room_messages} # create a context dictionary for the passed data
    return render(request, 'base/home.html', context) # third arg expected as a dictionary {'rooms': rooms}

def room(request, pk):
    q = request.GET.get('q') # get the query from the url
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all() #.order_by('-created'): another option we ordered the whole messages class instead
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

def userProfile(request, pk):
    user = User.objects.get(id = pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url= 'login') # check if user is logged in and redirect to login page if not
def createRoom (request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name) # if the topic does not exist, create it

        Room.objects.create(
            host = request.user,
            topic = topic, 
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )

        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url= 'login') # check if user is logged in and redirect to login page if not
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room) # the form will be pre filled with the room data
    topics = Topic.objects.all()

    if request.user != room.host: # check if the user is the owner of the room
        return HttpResponse('You are not the owner of this room')

    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get('name') # update functionality
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    context = {'form': form, 'topics': topics, 'room': room}
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
        return redirect('home') # pk = message.room.id) # redirect to the room page
    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url = 'login')
def updateUser(request):
    user = request.user
    form = UserForm(instance = user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'base/edit-user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' # inline if else to get query from URL (search)
    topics = Topic.objects.filter(name__icontains = q)
    return render(request, 'base/topics.html', {'topics': topics})

def activityPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' # inline if else to get query from URL (search)
    room_messages = Message.objects.filter(body__icontains = q)
    return render(request, 'base/activity.html', {'room_messages': room_messages})