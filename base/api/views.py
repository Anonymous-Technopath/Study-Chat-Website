from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET']) # passed which http reqest are allowed to access this view, like PUT,GET,POST
def getRoutes(request):
    routes=[
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',

    ]
    return Response(routes)


@api_view(['GET'])
def getRooms(request):
    rooms =Room.objects.all()
    serializer = RoomSerializer(rooms,many=True) # many means are there gonna be multiple objects we need to serialize is there going to be one
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(request,pk):
    room =Room.objects.get(id=pk)
    serializer = RoomSerializer(room,many=False) 
    return Response(serializer.data)