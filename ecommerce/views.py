from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from django.http import JsonResponse
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .utils import cookieCart

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request=request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']
    products = Product.objects.all()
    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "products": products,
    }
    return render(request=request, template_name="store/store.html", context=context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request=request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request=request, template_name="store/cart.html", context=context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request=request)
        items = cookieData['items']
        order = cookieData['order']
        cartItems = cookieData['cartItems']
    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request=request, template_name="store/checkout.html", context=context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse({"message": "Item was added"})


@csrf_exempt
def proccessOrder(request):
    transanction_id = datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data["form"]["total"])
        order.transanction_id = transanction_id

        if total == order.get_cart_total:
            order.complete = True

        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                state=data["shipping"]["state"],
                address=data["shipping"]["address"],
                city=data["shipping"]["city"],
                zipcode=data["shipping"]["zipcode"],
            )

    else:
        print("Not logget in...")

    return JsonResponse({"message": "Payment submitted.."})
