from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def getRoutes(request): # shows all the routes in the API
    routes = [
        'GET api/',
        'GET api/rooms/',
        'GET api/rooms/:id',
    ]
    return Response(routes) # safe = False allows us to return data structs other than dict

@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()
    serlializer = RoomSerializer(rooms, many=True) # create serializer object
    return Response(serlializer.data)

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serlializer = RoomSerializer(room, many=False) # for one Room object
    return Response(serlializer.data)