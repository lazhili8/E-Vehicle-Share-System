# myapp/serializers.py
from rest_framework import serializers
from .models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    address = serializers.CharField(source='location.address', read_only=True)

    class Meta:
        model = Vehicle
        fields = ['vehicleID', 'type', 'batteryStatus', 'isDefective', 'position_x', 'position_y', 'address']
