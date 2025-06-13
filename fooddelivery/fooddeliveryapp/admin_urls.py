from django.urls import path
from fooddeliveryapp.admin_views import *

urlpatterns = [
    path('',Homeview.as_view(), name='home'),
    path('customerverification',customerverification.as_view()),
    path('customer_approve',customer_approve.as_view()),
    path('customer_reject',customer_reject.as_view()),
    path('restaurentverification',restaurentverification.as_view()),
    path('restaurent_approve',restaurent_approve.as_view()),
    path('restaurent_reject',restaurent_reject.as_view()),
    path('agentview',agentview.as_view()),
    path('restaurentview',restaurentview.as_view()),
    path('customerview',customerview.as_view()),
    path('Viewbooking',Viewbooking.as_view()),
    path('view_feedback',view_feedback.as_view()),
]
