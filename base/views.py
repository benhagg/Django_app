from django.shortcuts import render

# Create your views here.
# function based veiws
rooms = [
    {'id':1, 'name':'Room 1'},
    {'id':2, 'name':'Room 2'},
    {'id':3, 'name':'Room 3'},
]

def home(request):
    context = {'rooms': rooms} # create a context dictionary for the passed data
    return render(request, 'base/home.html', context) # third arg expected as a dictionary {'rooms': rooms}

def room(request, pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    context = {'room': room}
    return render(request, 'base/room.html', context)