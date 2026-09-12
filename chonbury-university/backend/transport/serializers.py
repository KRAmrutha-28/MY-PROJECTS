from rest_framework import serializers
from .models import BusRoute, Bus

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'

class BusRouteSerializer(serializers.ModelSerializer):
    buses = BusSerializer(many=True, read_only=True)
    total_buses = serializers.IntegerField(source='buses.count', read_only=True)
    active_buses = serializers.SerializerMethodField()
    
    def get_active_buses(self, obj):
        return obj.buses.filter(status='ACTIVE').count()
    
    class Meta:
        model = BusRoute
        fields = '__all__'