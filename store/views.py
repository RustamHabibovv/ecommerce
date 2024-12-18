from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from .models import Product

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

def products_page(request):
    from .models import Product

    # Fetch all products
    products = Product.objects.all()

    # Fetch predefined category choices
    category_choices = Product.CATEGORY_CHOICES

    # Search functionality
    search_query = request.GET.get('search', '').strip()
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Filter by category
    selected_category = request.GET.get('category', '')
    if selected_category:
        products = products.filter(category=selected_category)

    # Filter by price range
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    context = {
        'products': products,
        'category_choices': category_choices,  # Send predefined categories to the template
        'selected_category': selected_category,  # For retaining selected filter
        'search_query': search_query,  # For retaining search query
        'min_price': min_price,  # For retaining min price
        'max_price': max_price,  # For retaining max price
    }
    return render(request, 'products_page.html', context)

def order_history(request):
    return render(request, 'order_history.html', {'message': 'Order History Placeholder'})

def liked_products(request):
    return render(request, 'liked_products.html', {'message': 'Liked Products Placeholder'})

def cart_page(request):
    return render(request, 'cart_page.html', {'message': 'Cart Page Placeholder'})
