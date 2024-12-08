from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import AmazonProduct, DarazProduct


@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('register')

        User.objects.create_user(username=username, password=password)
        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials!")
            return redirect('login')

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')



# Daraz product selection
def select_daraz_product(request):
    products = DarazProduct.objects.all()

    if request.method == 'POST':
        selected_product_id = request.POST['daraz_product']
        request.session['selected_daraz_product'] = selected_product_id
        return redirect('select_amazon_product')

    return render(request, 'select_daraz.html', {'products': products})

# Amazon product selection
def select_amazon_product(request):
    products = AmazonProduct.objects.all()

    if request.method == 'POST':
        amazon_id = request.POST['amazon_product']
        daraz_id = request.session.get('selected_daraz_product')

        if daraz_id:  # Ensure the daraz product ID is in the session
            return redirect('compare_products', daraz_id=daraz_id, amazon_id=amazon_id)

    return render(request, 'select_amazon.html', {'products': products})


# Compare selected products
def compare_products(request, daraz_id, amazon_id):
    from .models import DarazProduct, AmazonProduct

    daraz_product = DarazProduct.objects.get(id=daraz_id)
    amazon_product = AmazonProduct.objects.get(id=amazon_id)

    # Calculate price difference and percentage
    price_difference = abs(daraz_product.price - amazon_product.price)
    percentage_difference = (price_difference / max(daraz_product.price, amazon_product.price)) * 100

    context = {
        'daraz_product': daraz_product,
        'amazon_product': amazon_product,
        'price_difference': price_difference,
        'percentage_difference': round(percentage_difference, 2),
    }
    return render(request, 'compare.html', context)



# # Test view
# from celery import shared_task
# from .models import AmazonProduct, AmazonPriceHistory, DarazProduct, DarazPriceHistory
# from datetime import datetime

# @shared_task
# def update_product_prices():
#     # Example for Amazon
#     for product in AmazonProduct.objects.all():
#         # Scrape the current price (use your scraping function here)
#         current_price = scrape_amazon_price(product.name)  # Replace with your scraping logic

#         if product.current_price != current_price:
#             # Update current price
#             product.current_price = current_price
#             product.last_updated = datetime.now()
#             product.save()

#             # Add entry to price history
#             AmazonPriceHistory.objects.create(product=product, price=current_price)