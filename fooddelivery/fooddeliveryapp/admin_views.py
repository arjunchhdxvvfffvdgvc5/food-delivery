from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View
from fooddeliveryapp.models import *
from django.http import HttpResponse

class Homeview(TemplateView):
    template_name = 'admin/home.html'

class customerverification(TemplateView):
    template_name = 'admin/verify customer.html'

    def get_context_data(self, **kwargs):
        context = super(customerverification,self).get_context_data(**kwargs)
        customer = Customersignup.objects.filter(user__last_name='0',user__is_staff='0',user__is_active='1')
        context['customer'] = customer
        return context
    
class customer_approve(View):
    def dispatch(self, request,*args, **kwargs):
        id = request. GET['id']
        user = User.objects.get(pk=id)
        user.last_name ='1'
        user.save()
        return HttpResponse(f"<script>alert('account accepted');window.location='/admin/customerview' </script>")
    
class customer_reject(View):
    def dispatch(self, request,*args, **kwargs):
          id = request. GET['id']
          user = User.objects.get(pk=id)
          user.last_name ='1'
          user.is_active ='0'
          user.save()
          return HttpResponse(f"<script>alert('account rejected');window.location='/admin/customerview' </script>")


class restaurentverification(TemplateView):
    template_name = 'admin/verify restaurent.html'

    def get_context_data(self, **kwargs):
        context = super(restaurentverification,self).get_context_data(**kwargs)
        restaurent = restaurentsignup.objects.filter(user__last_name='0',user__is_staff='0',user__is_active='1')
        context['restaurent'] = restaurent
        return context
    
class restaurent_approve(View):
    def dispatch(self, request,*args, **kwargs):
        id = request. GET['id']
        user = User.objects.get(pk=id)
        user.last_name ='1'
        user.save()
        return HttpResponse(f"<script>alert('account accepted');window.location='/admin/restaurentview' </script>")
    
class restaurent_reject(View):
    def dispatch(self, request,*args, **kwargs):
          id = request. GET['id']
          user = User.objects.get(pk=id)
          user.last_name ='1'
          user.is_active ='0'
          user.save()
          return HttpResponse(f"<script>alert('account rejected');window.location='/admin/restaurentview' </script>")

class agentview(TemplateView):
    template_name = 'admin/agents.html'
    
    def get_context_data(self, **kwargs):
        context = super(agentview,self).get_context_data(**kwargs)
        agents = agentsignup.objects.filter(user__last_name='1',user__is_staff='0',user__is_active='1')
        context['agent'] = agents
        return context

class restaurentview(TemplateView):
    template_name = 'admin/restaurents.html'

    def get_context_data(self, **kwargs):
        context = super(restaurentview,self).get_context_data(**kwargs)
        restaurent = restaurentsignup.objects.filter(user__last_name='1',user__is_staff='0',user__is_active='1')
        context['restaurent'] = restaurent
        return context
    
class customerview(TemplateView):
    template_name = 'admin/customers.html'

    def get_context_data(self, **kwargs):
        context = super(customerview,self).get_context_data(**kwargs)
        customer = Customersignup.objects.filter(user__last_name='1',user__is_staff='0',user__is_active='1')
        context['customer'] = customer
        return context

class Viewbooking(TemplateView):
    template_name = 'admin/view_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookview=product_cart.objects.filter(status='approve')
        context['bookview']=bookview
        return context
    
class view_feedback(TemplateView):
    template_name='admin/feedback.html'

    def get_context_data(self, **kwargs):
        context = super(view_feedback,self).get_context_data(**kwargs)
        title = feedback.objects.all()
        context['title'] = title
        return context