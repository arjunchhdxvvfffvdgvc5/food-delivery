from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View
from fooddeliveryapp.models import *
from django.http import HttpResponse

class Homeview(TemplateView):
    template_name = 'customer/home.html'

class restaurentview(TemplateView):
    template_name = 'customer/restaurents.html'

    def get_context_data(self, **kwargs):
        context = super(restaurentview,self).get_context_data(**kwargs)
        restaurent = restaurentsignup.objects.filter(user__last_name='1',user__is_staff='0',user__is_active='1')
        context['restaurent'] = restaurent
        return context
    
    

    
class view_datails(TemplateView):
    template_name = 'customer/view_items.html'

    def get_context_data(self, **kwargs):
        context = super(view_datails,self).get_context_data(**kwargs)
        items = addmenu.objects.all()

        context['items'] = items
        return context
    

    
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import addmenu

class product_details_view(TemplateView):
    template_name = 'customer/view_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.request.GET.get('id')

        try:
            product = addmenu.objects.get(id=id)  # Fetch a single product
            context['product'] = product
        except addmenu.DoesNotExist:
            context['product'] = None
            context['message'] = "Product not found"

        return context

    def post(self, request, *args, **kwargs):
        user = Customersignup.objects.get(user_id=self.request.user.id)
        id = self.request.GET.get('id')

        try:
            pr = addmenu.objects.get(id=id)  # Get the product
        except addmenu.DoesNotExist:
            return render(request, 'customer/home.html', {'message': "Product not found"})

        # Validate quantity input
        try:
            quantity = int(request.POST['quantity'])  # Convert to integer
            if quantity <= 0:
                return render(request, 'customer/view_details.html', {
                    'message': "Quantity must be at least 1",
                    'product': pr
                })
        except ValueError:
            return render(request, 'customer/view_details.html', {
                'message': "Invalid quantity entered",
                'product': pr
            })

        # Convert `pr.quantity` and `pr.price` to integers
        available_stock = int(pr.quantity)
        price = int(pr.price)

        # Ensure the requested quantity does not exceed available stock
        if quantity > available_stock:
            return render(request, 'customer/view_details.html', {
                'message': f"Only {available_stock} items available in stock",
                'product': pr
            })

        total_price = quantity * price  # Correct price calculation
        pr.quantity = available_stock - quantity  # Update stock
        pr.save()

        # Add product to cart
        product_cart.objects.create(
            user_id=user.id,
            product_id=pr.id,
            quantity=quantity,
            status='added',
            total=total_price
        )

        return render(request, 'customer/home.html', {'message': f"Successfully added to cart. Total: ${total_price}"})

class cart_view(TemplateView):
    template_name = 'customer/view_cart.html'
    
    def get_context_data(self, **kwargs):
        context = super(cart_view, self).get_context_data(**kwargs)
        user=Customersignup.objects.get(user_id=self.request.user.id)
        ct = product_cart.objects.filter(status='added', user_id=user.id)

        total = 0
        for i in ct:
            total = total + int(i.total)
        context['ct'] = ct
        context['asz'] = total

        return context
    
class RejectcartView(View):
    def dispatch(self,request,*args,**kwargs):
        id = request.GET['id']
        product_cart.objects.get(id=id).delete()
        return redirect('cart_view')
    

class checkout(TemplateView):
    template_name = 'customer/payment.html'
    def get_context_data(self, **kwargs):
        context = super(checkout, self).get_context_data(**kwargs)
        user=Customersignup.objects.get(user_id=self.request.user.id)
        ct = product_cart.objects.filter(status='added', user_id=user.id)

        total = 0
        for i in ct:
            total = total + int(i.total)

        context['ct'] = ct
        context['asz'] = total

        return context
    
class payment(TemplateView):
    template_name= 'customer/payment.html'
    def dispatch(self,request,*args,**kwargs):

        user=Customersignup.objects.get(user_id=self.request.user.id)


        ch = product_cart.objects.filter(user_id=user.id,status='added')


        print(ch)
        for i in ch:
            i.status='paid'
            i.save()

        return HttpResponse(f"<script>alert('payment successfull..'); window.location='/customer'; </script>")
    
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Customersignup, product_cart, assigned_order

class product_orders(TemplateView):
    template_name = 'customer/my_order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = Customersignup.objects.get(user_id=self.request.user.id)
        
        pr = product_cart.objects.filter(user_id=user.id, status__in=['paid', 'approve', 'rejected', 'Assigned'])
        
        ps = assigned_order.objects.filter(user__in=pr, status__in=['pickup', 'delivered'])
        
        context['pr'] = pr
        context['ps'] = ps
        return context

class cancel_product_order(View):
    def dispatch(self,request,*args,**kwargs):
        id = request.GET['id']
        product_cart.objects.get(id=id).delete()
        return redirect(request.META['HTTP_REFERER'])
    
class Add_feedback(TemplateView):
     template_name = 'customer/feedback.html'
    
     def post(self, request, *args, **kwargs):
        user = Customersignup.objects.get(user_id=self.request.user.id)
        title = request.POST ['title']
        description = request.POST ['description']
        rating = request.POST ['rating']
        se =feedback()
        se.user=user
        se.title=title
        se.description=description
        se.rating=rating
        se.save()
        return render(request,'customer/home.html')