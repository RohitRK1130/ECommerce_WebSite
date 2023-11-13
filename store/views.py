from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieData, cartData, guestOrder
from django.views.decorators.csrf import csrf_exempt

def index(request):
	data = cartData(request)
	cartItems = data['cartItems']

	products = Product.objects.all()
	load_more = False
	if products.count() > 12:
		load_more = True
	context = {"products":products, "load_more": load_more,"cartItems":cartItems}
	return render(request, 'store/index.html', context)

def cart(request):
	data = cartData(request)
	items = data['items']
	order = data['order']
	cartItems = data['cartItems']

	context = {"items":items,"order":order,"cartItems":cartItems}
	return render(request, 'store/cart.html', context)

def about(request):
	data = cartData(request)
	cartItems = data['cartItems']

	context = {"cartItems":cartItems}
	return render(request, 'store/about.html', context)

def testimonial(request):
	data = cartData(request)
	cartItems = data['cartItems']

	context = {"cartItems":cartItems}
	return render(request, 'store/testimonial.html', context)

def product(request):
	data = cartData(request)
	cartItems = data['cartItems']

	products = Product.objects.all()
	load_more = False
	if products.count() > 12:
		load_more = True
	context = {"products":products, "load_more": load_more,"cartItems":cartItems}
	return render(request, 'store/product.html', context)

def blog(request):
	data = cartData(request)
	cartItems = data['cartItems']

	context = {"cartItems":cartItems}
	return render(request, 'store/blog_list.html', context)

def contact(request):
	data = cartData(request)
	cartItems = data['cartItems']

	context = {"cartItems":cartItems}
	return render(request, 'store/contact.html', context)

@csrf_exempt
def checkout(request):
	data = cartData(request)
	items = data['items']
	order = data['order']
	cartItems = data['cartItems']

	context = {"items":items,"order":order,"cartItems":cartItems}
	return render(request, 'store/checkout.html', context)

@csrf_exempt
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, ordercreated = Order.objects.get_or_create(customer=customer, complete =False)
	orderItem, orderItemcreated = OrderItem.objects.get_or_create(order=order,product=product)

	if action == 'allremove':
		orderItem.delete()
	else:
		if action == 'add':
			orderItem.quantity = (orderItem.quantity + 1) 
		elif action == 'remove':
			orderItem.quantity = (orderItem.quantity - 1) 
		orderItem.save()
		if orderItem.quantity <= 0:
			orderItem.delete()

	return JsonResponse('Item was updated', safe=False)

@csrf_exempt
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated: 
		customer = request.user.customer
		order, ordercreated = Order.objects.get_or_create(customer=customer, complete =False)
	else:
		order, customer = guestOrder(request, data)
	total = float(data['form']['total'])
	order.transaction_id = transaction_id
	if total == order.get_cart_total():
		order.complete = True
	order.save()

	if order.shipping() == True:
		ShippingAddress.objects.create(
			customer=customer,
			order=order,
			name=customer.name,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zip'],
		)

	return JsonResponse("Payment Subbmitted..", safe=False)