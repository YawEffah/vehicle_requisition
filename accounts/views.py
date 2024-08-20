
from django.shortcuts import render, redirect
from .forms import *
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone



# Create your views here.





def is_staff(user):
    return user.groups.filter(name='staff').exists()

def is_transport_officer(user):
    return user.groups.filter(name='transport_officer').exists()


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Signed in successfully')
                if is_staff(user):
                    return redirect(reverse('requisition:staff_dashboard'))
                elif is_transport_officer(user):
                    return redirect(reverse('requisition:requests_dashboard'))
                else:
                    return redirect(reverse('index'))
            else:
                return render(request, 'login.html', {
                    'form': form, 
                    'errors': 'Invalid credentials'
                })
    return render(request, 'login.html', {'form': LoginForm()})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect(reverse('login'))
