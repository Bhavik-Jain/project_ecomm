from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
import datetime
from .utils import cookieCart, cartData, guestOrder
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.db.models.query import QuerySet

@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			messages.success(request, 'Account was created for '+username)
			return redirect('login')

	context = {'form': form}
	return render(request, 'store/register.html', context)

@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(request, username = username, password = password)

		if user is not None:
			login(request, user)
			if user.is_superuser:
				return redirect('dashboard')
			else:
				return redirect('profile')
		else:
			messages.info(request, 'Username OR Password is incorrect')

	context = {}
	return render(request, 'store/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def profilePage(request):
	customer = request.user.customer
	form = ProfileForm(instance=customer)

	if request.method == 'POST':
		form = ProfileForm(request.POST, request.FILES, instance=customer) 
		if form.is_valid():
			form.save()
			
	context = {'form': form}
	return render(request, 'store/profile.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def store(request):
	data = cartData(request)
	cartItems = data['cartItems']

	products = Product.objects.all()

	context = {'products':products, 'cartItems': cartItems}
	return render(request, 'store/store.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def cart(request):
	data = cartData(request)
	cartItems = data['cartItems']
	items = data['items']
	order = data['order']

	context = {'items':items, 'order': order, 'cartItems': cartItems}
	return render(request, 'store/cart.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def checkout(request):
	data = cartData(request)
	cartItems = data['cartItems']
	items = data['items']
	order = data['order']

	# if request.user.is_authenticated:
	# 	customer = request.user.customer
	# 	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	# 	items = order.orderitem_set.all()
	# 	cartItems = order.get_cart_items

	context = {'items':items, 'order': order, 'cartItems': cartItems}
	return render(request, 'store/checkout.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def updateItem(request):
	data = json.loads(request.body)
	productID = data['productID']
	action = data['action']

	print('Action:', action)
	print('productID:', productID)

	customer = request.user.customer
	product = Product.objects.get(id=productID)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()


	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)

	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == float(order.get_cart_total):
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
	)

	return JsonResponse('Payment Complete!', safe=False)



from .decorators import admin_only

@login_required(login_url='login')
@admin_only
def dashboard(request):
	customers = Customer.objects.all()
	items = OrderItem.objects.all()

	context = {'customers': customers, 'items': items}

	return render(request, 'store/dashboard.html', context)

@login_required(login_url='login')
@admin_only
def products(request):
	products = Product.objects.all()
	return render(request, 'store/products.html', {'products': products})

@login_required(login_url='login')
@admin_only
def customer(request, pk):
	customer = Customer.objects.get(id=pk)
	orders = customer.orderitem_set.all()
	shippinginfo = customer.shippingaddress_set.all()

	total_order = orders.count()

	context = {'customer': customer, 'orders': orders, 'total_order':total_order, 'shippinginfo': shippinginfo}
	return render(request, 'store/customer.html', context)