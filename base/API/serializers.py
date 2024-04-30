from rest_framework.serializers import ModelSerializer
from base.models import Room


class RoomSerializer(ModelSerializer): # to turn a room object in to json serializable format
    class Meta:
        model = Room
        fields = '__all__'