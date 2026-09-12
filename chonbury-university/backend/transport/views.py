from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import BusRoute, Bus
from .serializers import BusRouteSerializer, BusSerializer

class BusRouteViewSet(viewsets.ModelViewSet):
    queryset = BusRoute.objects.all()
    serializer_class = BusRouteSerializer

class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

@api_view(['GET'])
def get_transport_details(request):
    routes = BusRoute.objects.all()
    data = []
    for route in routes:
        buses = route.buses.filter(status='ACTIVE')
        data.append({
            'route_number': route.route_number,
            'route_name': route.route_name,
            'total_buses': route.buses.count(),
            'active_buses': buses.count(),
            'buses': BusSerializer(buses, many=True).data,
            'stops': route.stops,
            'start_point': route.start_point,
            'end_point': route.end_point
        })
    return Response(data)

@api_view(['GET'])
def get_buses_by_route(request, route_number):
    try:
        route = BusRoute.objects.get(route_number=route_number)
        buses = route.buses.all()
        serializer = BusSerializer(buses, many=True)
        return Response(serializer.data)
    except BusRoute.DoesNotExist:
        return Response({'error': 'Route not found'}, status=404)