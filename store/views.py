from .models import *
from django.http import JsonResponse, HttpResponse
import json
import datetime
from .utils import cookieData, cartData, guestOrder
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from paytm.checksum import generateSignature,verifySignature
import razorpay
from django.shortcuts import HttpResponseRedirect, redirect, render

import logging
import sys
logger = logging.getLogger(__name__)



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
	if request.method == "GET":
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
	try:
		transaction_id = datetime.datetime.now().timestamp()
		data = json.loads(request.body.decode('utf-8'))

		if request.user.is_authenticated: 
			customer = request.user.customer
			order, ordercreated = Order.objects.get_or_create(customer=customer, complete =False)
		else:
			order, customer = guestOrder(request, data)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		logger.info("ProcessOrder If Check %s ==  %s",str(total), str(order.get_cart_total()))

		if str(total) == str(order.get_cart_total()):
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

			# razorpay getway
			client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))
			payment = client.order.create({
				'amount': int(order.get_cart_total()) * 100,
				'currency': 'INR',
				'payment_capture' : 1
				})
			
			payment['status'] = 'success'
			order.razorpay_order_id = payment['id']
			order.save()
			return JsonResponse(payment, safe=False)

		data = {}
		data['status'] = "fail"
		return JsonResponse(data,safe=False)

	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		logger.error("ProcessOrder Error %s at %s",str(e), str(exc_tb.tb_lineno))
		data = {}
		data['status'] = "fail"
		return JsonResponse(data,safe=False)
	

@csrf_exempt
def razorpaySuccess(request):
	razorpay_order_id = request.GET.get("razorpay_order_id","")
	if razorpay_order_id:
		order = Order.objects.get(razorpay_order_id=razorpay_order_id)
		order.complete = True
		order.save()
		context = {}
		return render(request, 'store/payment_success.html', context)
		return HttpResponse("Payment Success..")
		