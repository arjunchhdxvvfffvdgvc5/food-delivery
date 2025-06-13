from django.urls import path
from fooddeliveryapp.agent_views import *

urlpatterns = [
    path('',Homeview.as_view(), name='home'),
    path('agentavailability',agentavailability.as_view(), name='home'),
    path('assignview',assignview.as_view(),name="assigned_order"),
    path('Approveassignview',Approveassignview.as_view()),
    path('Rejectassignview',Rejectassignview.as_view()),
    path('orderstatus',orderstatus.as_view()),
    path('report',report.as_view()),
]