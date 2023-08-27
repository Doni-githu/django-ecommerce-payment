from . import views
from django.urls import path
urlpatterns = [
    path('', views.StoreView.as_view(), name="store"),
    path('cart/', views.CartView.as_view(), name="cart"),
    path("checkout/", views.CheckOutView.as_view(), name="checkout"),
    
    path('update_item/', views.updateItem, name="update"),
    path('proccess_order/', views.proccessOrder, name="proccessOrder"),
]
