from django.urls import path
from fooddeliveryapp.restaurent_views import *
urlpatterns = [
    path('',Homeview.as_view(), name='home'),
    path('agentverification',agentverification.as_view()),
    path('agent_approve',agent_approve.as_view()),
    path('agent_reject',agent_reject.as_view()),
    path('agentview',agentview.as_view()),
    path('menuview',menuview.as_view()),
    path('itemsview',itemsview.as_view()),
    path('UpdateProduct',UpdateProduct.as_view()),
    path('product_delete',product_delete.as_view()),
    path('ApprovebookingView',ApprovebookingView.as_view()),
    path('RejectbookingView',RejectbookingView.as_view()),
    path('Viewbooking',Viewbooking.as_view(),name="viewbooking"),
    path('bookview',bookview.as_view(),name="verify_orders"),
    path('view_feedback',view_feedback.as_view()),
]