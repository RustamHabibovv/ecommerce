from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser

def register_view(request):
    if request.method == 'POST':
        # Fetch the form data
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        role = request.POST.get('role', '')

        # Check for empty fields
        if not username or not email or not password1 or not password2 or not role:
            messages.error(request, 'All fields are required.')
            return render(request, 'register.html')

        # Validate the passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'register.html')

        # Check if username or email already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'register.html')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use.')
            return render(request, 'register.html')

        # Create the user
        user = CustomUser.objects.create_user(username=username, email=email, password=password1, role=role)
        user.save()

        # Success message and redirect
        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')

