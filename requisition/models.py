from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)

    def __str__(self):
        return self.user.first_name
    

class TransportOfficer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.first_name


class Vehicle(models.Model):
    picture = models.ImageField(upload_to='vehicle_pictures/')
    license_plate = models.CharField(max_length=20)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.make} {self.model} ({self.license_plate})'

class CarRequest(models.Model):
    PURPOSE_CHOICES = [
        ('Business', 'Business'),
        ('Personal', 'Personal'),
    ]
    
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    description = models.TextField(max_length=500)
    destination = models.CharField(max_length=100)
    start_datetime = models.DateTimeField()
    return_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Declined', 'Declined'),
        ('Returned', 'Returned'),
    ], default=('Pending'))
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.purpose} to {self.destination}'
