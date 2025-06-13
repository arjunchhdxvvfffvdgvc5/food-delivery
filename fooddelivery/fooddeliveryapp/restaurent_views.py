from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View
from django.contrib.auth.models import User
from fooddeliveryapp.models import *
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse


class Homeview(TemplateView):
    template_name = 'restaurants/home.html'

class agentverification(TemplateView):
    template_name = 'restaurants/verify_agent.html'

    def get_context_data(self, **kwargs):
        context = super(agentverification,self).get_context_data(**kwargs)
        agent = agentsignup.objects.filter(user__last_name='0',user__is_staff='0',user__is_active='1')
        context['agent'] = agent
        return context
    
class agent_approve(View):
    def dispatch(self, request,*args, **kwargs):
        id = request. GET['id']
        user = User.objects.get(pk=id)
        user.last_name ='1'
        user.save()
        return HttpResponse(f"<script>alert('account accepted');window.location='/restaurent' </script>")
    
class agent_reject(View):
    def dispatch(self, request,*args, **kwargs):
          id = request. GET['id']
          user = User.objects.get(pk=id)
          user.last_name ='1'
          user.is_active ='0'
          user.save()
          return HttpResponse(f"<script>alert('account rejected');window.location='/restaurent' </script>")

class agentview(TemplateView):
    template_name = 'restaurants/agents.html'
    
    def get_context_data(self, **kwargs):
        context = super(agentview,self).get_context_data(**kwargs)
        agents = agentsignup.objects.filter(user__last_name='1',user__is_staff='0',user__is_active='1')
        context['agent'] = agents
        return context
        
class menuview(TemplateView):
    template_name = 'restaurants/add items.html'

    def post(self,request,*args,**kwargs):
        restaurent=restaurentsignup.objects.get(user_id=self.request.user.id)
        name = request.POST['foodName']
        Description = request.POST['foodDescription']
        Price = request.POST['foodPrice']
        quantity = request.POST['product_quantity']
        Image = request.FILES['foodImage']

        se=addmenu()
        se.user=restaurent
        se.FoodName=name
        se.description=Description
        se.price=Price
        se.quantity=quantity
        se.image=Image
        se.save()
        return render(request,'restaurants/home.html',{'message':"successfully added"})
    
class itemsview(TemplateView):
    template_name = 'restaurants/items.html'

    def get_context_data(self, **kwargs):
        context=super(itemsview,self).get_context_data(**kwargs)
        com=restaurentsignup.objects.get(user_id=self.request.user.id)
        menu=addmenu.objects.filter(user_id=com.id)
        context['menu']=menu
        return context
    
class UpdateProduct(TemplateView):
    template_name = 'restaurants/update.html'
    def get_context_data(self, **kwargs):
        id = self.request.GET['id']
        context = super(UpdateProduct,self).get_context_data(**kwargs)
        product = addmenu.objects.filter(id=id)

        context['product'] = product
        return context
    
    def post(self,request,*args,**kwargs):
        id = request.GET['id'] 
        image = request.FILES['foodImage']
        fii = FileSystemStorage()
        filesss = fii.save(image.name, image)
        
        product =addmenu.objects.get(id=id)
        product.FoodName = request.POST['foodName']
        product.price = request.POST['foodPrice']
        product.description = request.POST['foodDescription']
        product.quantity = request.POST['product_quantity']
        product.image = filesss
        product.save()
        return render(request,'restaurants/home.html', {'message':"updated Successfully "})

class product_delete(View):
    def dispatch(self,request,*args,**kwargs):
        id = request.GET['id']
        addmenu.objects.get(id=id).delete()
        return redirect('/restaurent')
    
class bookview(TemplateView):
    template_name = 'restaurants/verify_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookview=product_cart.objects.filter(status='paid')
        context['bookview']=bookview
        return context

class ApprovebookingView(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        bookview = product_cart.objects.get(pk=id)
        bookview.status='approve'
        bookview.save()
        return redirect('verify_orders')
    
class RejectbookingView(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        bookview = product_cart.objects.get(pk=id)
        bookview.status='rejected'
        bookview.save()
        return redirect('verify_orders')
    


class Viewbooking(TemplateView):
    template_name = 'restaurants/view_orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dis = agentsignup.objects.filter(user__last_name='1', user__is_staff='0', user__is_active='1',status="available")
        bookview = product_cart.objects.filter(status='approve')
        context['dis'] = dis
        context['bookview'] = bookview
        return context

    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('assign_order')
        
        if order_id:
            try:
                order = product_cart.objects.get(id=order_id)
                agent_name = request.POST.get(f'agent_name_{order_id}')
                agent = agentsignup.objects.get(user__first_name=agent_name)

                user = order.user
                assigned = assigned_order(
                    agent=agent,
                    user=order,
                    price=order.total,
                    quantity=order.quantity,
                    status='Assigned'
                )
                assigned.save()

                order.status = 'Assigned'
                order.save()

                return redirect('viewbooking')

            except product_cart.DoesNotExist:
                return HttpResponse("Order not found.", status=404)
            except agentsignup.DoesNotExist:
                return HttpResponse("Agent not found.", status=404)
        
        return redirect('viewbooking')
    
class view_feedback(TemplateView):
    template_name='restaurants/feedback.html'

    def get_context_data(self, **kwargs):
        context = super(view_feedback,self).get_context_data(**kwargs)
        title = feedback.objects.all()
        context['title'] = title
        return context
