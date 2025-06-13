from django.urls import path
from fooddeliveryapp.customer_views import *

urlpatterns = [
    path('',Homeview.as_view(), name='home'),
    path('restaurentview',restaurentview.as_view()),
    path('view_datails',view_datails.as_view()),
    path('product_details_view',product_details_view.as_view()),
    path('cart_view',cart_view.as_view(),name="cart_view"),
    path('RejectcartView',RejectcartView.as_view()),
    path('checkout',checkout.as_view()),
    path('payment',payment.as_view()),
    path('product_orders',product_orders.as_view()),
    path('cancel_product_order',cancel_product_order.as_view()),
    path('Add_feedback',Add_feedback.as_view()),

]