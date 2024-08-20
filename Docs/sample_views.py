from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import CarRequest, Vehicle
from .forms import VehicleForm

@login_required
def create_car_request(request):
    if request.method == 'POST':
        form = CarRequestForm(request.POST)
        if form.is_valid():
            car_request = form.save(commit=False)
            car_request.user = request.user
            car_request.save()

            # Notify transport officers via messaging framework
            messages.success(request, 'Car request created successfully. Transport officers have been notified.')

            # Optional: Send an email notification
            send_mail(
                'New Car Request Created',
                f'A new car request has been created by {request.user.username}.',
                settings.DEFAULT_FROM_EMAIL,
                ['transport_officer@example.com'],  # Replace with the transport officer's email
                fail_silently=False,
            )
            return redirect('some_view')
    else:
        form = CarRequestForm()
    return render(request, 'create_car_request.html', {'form': form})

@login_required
def view_all_requests(request):
    requests = CarRequest.objects.all()
    return render(request, 'view_all_requests.html', {'requests': requests})

@login_required
def approve_request(request, pk):
    car_request = get_object_or_404(CarRequest, pk=pk)
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle_id')
        if vehicle_id:
            vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
            if vehicle.is_available:
                car_request.vehicle = vehicle
                car_request.status = 'Approved'
                vehicle.is_available = False
                vehicle.save()
                car_request.save()

                # Notify the staff
                messages.success(request, 'Request approved successfully. The staff has been notified.')
                send_mail(
                    'Car Request Approved',
                    f'Your car request to {car_request.destination} has been approved.',
                    settings.DEFAULT_FROM_EMAIL,
                    [car_request.user.email],
                    fail_silently=False,
                )
            else:
                messages.error(request, 'Selected vehicle is not available.')
        else:
            car_request.status = 'Declined'
            car_request.save()

            # Notify the staff
            messages.success(request, 'Request declined successfully. The staff has been notified.')
            send_mail(
                'Car Request Declined',
                f'Your car request to {car_request.destination} has been declined.',
                settings.DEFAULT_FROM_EMAIL,
                [car_request.user.email],
                fail_silently=False,
            )
        return redirect('view_all_requests')
    vehicles = Vehicle.objects.filter(is_available=True)
    return render(request, 'approve_request.html', {'car_request': car_request, 'vehicles': vehicles})

@login_required
def decline_request(request, pk):
    car_request = get_object_or_404(CarRequest, pk=pk)
    if request.method == 'POST':
        car_request.status = 'Declined'
        car_request.save()

        # Notify the staff
        messages.success(request, 'Request declined successfully. The staff has been notified.')
        send_mail(
            'Car Request Declined',
            f'Your car request to {car_request.destination} has been declined.',
            settings.DEFAULT_FROM_EMAIL,
            [car_request.user.email],
            fail_silently=False,
        )
        return redirect('view_all_requests')
    return render(request, 'decline_request.html', {'car_request': car_request})

@login_required
def fleet_dashboard(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'fleet_dashboard.html', {'vehicles': vehicles})

@login_required
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fleet_dashboard')
    else:
        form = VehicleForm()
    return render(request, 'add_vehicle.html', {'form': form})

@login_required
def delete_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('fleet_dashboard')
    return render(request, 'delete_vehicle.html', {'vehicle': vehicle})

@login_required
def edit_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('fleet_dashboard')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'edit_vehicle.html', {'form': form})
