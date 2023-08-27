from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from django.http import JsonResponse
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .utils import cookieCart, cartData, guestOrder


class BaseTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        result = cartData(request=self.request)
        for i in result:
            context[i] = result[i]
        return context


class StoreView(BaseTemplateView):
    template_name = "store/store.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        context["products"] = products
        return context


class CartView(BaseTemplateView):
    template_name = "store/cart.html"


class CheckOutView(BaseTemplateView):
    template_name = "store/checkout.html"


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
    else:
        customer, order = guestOrder(request=request, data=data)

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

    return JsonResponse({"message": "Payment submitted.."})