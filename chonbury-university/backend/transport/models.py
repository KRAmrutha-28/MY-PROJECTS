from django.db import models

class BusRoute(models.Model):
    route_number = models.CharField(max_length=20, unique=True)
    route_name = models.CharField(max_length=100)
    start_point = models.CharField(max_length=200)
    end_point = models.CharField(max_length=200)
    stops = models.TextField()
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"Route {self.route_number}: {self.route_name}"

class Bus(models.Model):
    BUS_STATUS = [
        ('ACTIVE', 'Active'),
        ('MAINTENANCE', 'Under Maintenance'),
        ('INACTIVE', 'Inactive'),
    ]
    
    bus_number = models.CharField(max_length=20, unique=True)
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE, related_name='buses')
    capacity = models.IntegerField()
    driver_name = models.CharField(max_length=100)
    driver_contact = models.CharField(max_length=15)
    morning_departure = models.TimeField()
    evening_departure = models.TimeField()
    status = models.CharField(max_length=11, choices=BUS_STATUS, default='ACTIVE')
    registration_number = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"Bus {self.bus_number} - {self.route.route_name}"