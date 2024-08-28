from django.shortcuts import render, redirect, get_object_or_404
from .models import CarRequest, Vehicle, Staff, TransportOfficer
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings

from .forms import CarRequestForm, CreateVehicleForm
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.

def is_staff(user):
    return user.groups.filter(name='staff').exists()

def is_transport_officer(user):
    return user.groups.filter(name='transport_officer').exists()


def index(request):
    return render(request, 'requisition/index.html')

@login_required
@user_passes_test(is_staff, login_url='login')
def staff_dashboard(request):

    staff = request.user
    pending_vehicle_requests = CarRequest.objects.filter(staff=staff, status='Pending').count()
    approved_vehicle_requests = CarRequest.objects.filter(staff=staff, status='Approved').count()
    total_vehicle_requests = CarRequest.objects.filter(staff=staff).count()
    vehicle_requests = CarRequest.objects.filter(staff=staff).order_by('-id')
    
    if request.method == 'POST':
        form = CarRequestForm(request.POST)
        if form.is_valid():
            car_request = form.save(commit=False)
            car_request.staff = staff
            car_request.save()
            messages.success(request, "Request sent successfully")
            return redirect(reverse('requisition:staff_dashboard'))
        else:
            return render(request, 'requisition/staff-dashboard.html', {'form': form})
        
    form = CarRequestForm()

    context = {
        'staff': staff, 
        'form': form,
        'pending_vehicle_requests': pending_vehicle_requests, 
        'approved_vehicle_requests': approved_vehicle_requests, 
        'total_vehicle_requests': total_vehicle_requests, 
        'vehicle_requests': vehicle_requests}
        
    return render(request, 'requisition/staff-dashboard.html', context)


@login_required
@user_passes_test(is_staff, login_url='login')
def delete_request_view(request, request_id):
    car_request = CarRequest.objects.get(pk=request_id)
    car_request.delete()
    messages.error(request, 'Request deleted successfully!')
    return redirect('requisition:staff_dashboard')


@login_required
@user_passes_test(is_staff, login_url='login')
def edit_request_view(request, request_id):
    car_request = CarRequest.objects.get(pk=request_id)
    form = CarRequestForm(request.POST or None, instance=car_request)
    if form.is_valid():
        form.save()
        messages.success(request, 'Request updated successfully')
        return redirect('requisition:staff_dashboard')
    return render(request, 'requisition/edit.html', {'edit_form': form})

@login_required
@user_passes_test(is_transport_officer, login_url='login')
def transport_officer_dashboard(request):
    pending_vehicle_requests = CarRequest.objects.filter(status = 'Pending').count()
    approved_vehicle_requests = CarRequest.objects.filter(status = 'Approved').count()
    total_vehicle_requests = CarRequest.objects.all().count
    vehicle_requests = CarRequest.objects.all().order_by('-id')

    context = {
        'pending_vehicle_requests': pending_vehicle_requests,
        'approved_vehicle_requests': approved_vehicle_requests,
        'total_vehicle_requests': total_vehicle_requests,
        'vehicle_requests': vehicle_requests
    }
    return render(request, 'requisition/requests-dashboard.html', context)



@login_required
@user_passes_test(is_transport_officer, login_url='login')
def fleet_dashboard(request):
    available_vehicles = Vehicle.objects.filter(is_available = True).count()
    unavailable_vehicles = Vehicle.objects.filter(is_available = False).count()
    total_vehicles = Vehicle.objects.all().count()
    vehicles = Vehicle.objects.all()

    if request.method == 'POST':
        form = CreateVehicleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle Added successfully")
            return redirect(reverse('requisition:fleet_dashboard'))
        else:
            return render(request, 'requisition/fleet-dashboard.html', {'form': form})
        
    form = CreateVehicleForm()

    context = {
        'form': form,
        'available_vehicles': available_vehicles,
        'unavailable_vehicles': unavailable_vehicles,
        'total_vehicles': total_vehicles,
        'vehicles': vehicles
    }

    return render(request, 'requisition/fleet-dashboard.html', context)


def notify_staff(car_request, status):
    email_subject = f'Car Request {status}'
    email_body = f'Your car request ({car_request.vehicle}) to {car_request.destination} on {car_request.start_datetime} has been {status.lower()}.'
    send_mail(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [car_request.staff.email],
        fail_silently=False,
    )
    # import requests
    # client = requests.Session()
    # url = "https://sms.arkesel.com/sms/api?action=send-sms&api_key=&to=PhoneNumber&from=SenderID&sms=YourMessage"
    # params = {
    #     "action": "send-sms",
    #     "api_key": "WnlZVGJJc2pzVkNPV0lOa1FsT3I",
    #     "to": f"{car_request.staff.phone_number}",
    #     "from": "Requi",
    #     "sms": f"Your car request ({car_request.vehicle}) to {car_request.destination} on {car_request.start_datetime} has been {status.lower()}."
    # }

    # # Send HTTP GET request
    # try:
    #     response = client.get(url, params=params)
    #     response.raise_for_status()
    #     print(response.text)
    # except requests.exceptions.RequestException as e:
    #     print("An error occurred:", e)

@user_passes_test(is_transport_officer, login_url='login')
def change_status(request, request_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid_statuses = ['Approved', 'Declined', 'Returned']

        if new_status not in valid_statuses:
            messages.error(request, 'Invalid status.')
            return redirect('requisition:requests_dashboard')

        car_request = get_object_or_404(CarRequest, id=request_id)
        vehicle = car_request.vehicle

        # Update status
        car_request.status = new_status
        car_request.save()

        # Update vehicle availability if the request is approved
        if new_status == 'Approved':
            if vehicle:
                vehicle.is_available = False
                vehicle.save()
            notify_staff(car_request, new_status)
            messages.success(request, 'Request approved successfully. The staff has been notified.')
        elif new_status == 'Declined':
            if vehicle:
                vehicle.is_available = True
                vehicle.save()
            notify_staff(car_request, new_status)
            messages.success(request, 'Request declined successfully. The staff has been notified.')
        elif new_status == 'Returned':
            if vehicle:
                vehicle.is_available = True
                vehicle.save()
            messages.success(request, 'Vehicle returned successfully.')

        return redirect('requisition:requests_dashboard')
    


@login_required
@user_passes_test(is_transport_officer, login_url='login')
def edit_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = CreateVehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle updated successfully!')
            return redirect('requisition:fleet_dashboard')
    else:
        form = CreateVehicleForm(instance=vehicle)
    return render(request, 'requisition/edit-vehicle.html', {'form': form})


@login_required
@user_passes_test(is_transport_officer, login_url='login')
def delete_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    vehicle.delete()
    messages.error(request, 'Vehicle deleted successfully!')
    return redirect('requisition:fleet_dashboard')
    

# Add more views for approval, decline, and other functionalities as needed
