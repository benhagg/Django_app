from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

# Create your views here.

# function based veiws -- Class based views are also possible
def home(request):
    rooms = Room.objects.all() # get all the rooms from the Room model (modelname.modelobjectsattribute.method())
    context = {'rooms': rooms} # create a context dictionary for the passed data
    return render(request, 'base/home.html', context) # third arg expected as a dictionary {'rooms': rooms}

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom (request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save() # saves to db
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room) # the form will be pre filled with the room data

    if request.method == "POST":
        form = RoomForm(request.POST, instance = room) # new POST data will replace the room object data in the room variable
        if form.is_valid: # checks if form is valid
            form.save() # saves to db
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete() # delete this object from the db
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})