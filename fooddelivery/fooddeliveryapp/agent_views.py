from django.shortcuts import render,redirect
from django.views.generic import TemplateView,View
from django.contrib.auth.models import User
from fooddeliveryapp.models import *
from django.http import HttpResponse

class Homeview(TemplateView):
    template_name = 'delivery agents/home.html'

class agentavailability(TemplateView):
    template_name='delivery agents/availability.html' 

    def post(self, request, *args, **kwargs):
        agent = agentsignup.objects.get(user_id=request.user.id)
        availability = request.POST.get('availability')
        agent.status = availability
        agent.save()
        return render(request, self.template_name, {'message': "Successfully updated"})  
    

class assignview(TemplateView):
    template_name = 'delivery agents/assigned_order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agent = agentsignup.objects.get(user_id=self.request.user.id)
        assign1=assigned_order.objects.filter(agent=agent,status='Assigned')
        context['assign1']=assign1
        return context
    
class Approveassignview(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        assign1 = assigned_order.objects.get(pk=id)
        assign1.status='approve'
        assign1.save()
        return redirect('assigned_order')
    
class Rejectassignview(View):
    def dispatch(self, request, *args, **kwargs):
        id = request.GET['id']
        assign1 = assigned_order.objects.get(pk=id)
        assign1.status='rejected'
        assign1.save()
        return redirect('assigned_order')
    
# class orderstatus(TemplateView):
#     template_name = 'delivery agents/order_status.html'

#     def get_context_data(self, **kwargs):
#         context = super(orderstatus, self).get_context_data(**kwargs)
#         agent = agentsignup.objects.get(user_id=self.request.user.id)
#         bookview = assigned_order.objects.filter(agent=agent,status='approve')
#         context['assign1'] = bookview
#         return context


from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from .models import assigned_order, agentsignup, agentWorks

class orderstatus(TemplateView):
    template_name = 'delivery agents/order_status.html'

    def get_context_data(self, **kwargs):
        context = super(orderstatus, self).get_context_data(**kwargs)
        try:
            agent = agentsignup.objects.get(user_id=self.request.user.id)
            status = assigned_order.objects.filter(agent=agent, status__in=['approve', 'pickup'])
            context['assign1'] = status
        except agentsignup.DoesNotExist:
            context['assign1'] = []
        return context

    def post(self, request, *args, **kwargs):
        agent = agentsignup.objects.get(user_id=request.user.id)
        status = request.POST.get('status')  # Get status from form
        order_id = request.POST.get('order_id')  # Get the selected order ID

        if status and order_id:
            order = get_object_or_404(assigned_order, id=order_id, agent=agent)

            order.status = status
            order.save()

            if status == "delivered":
                if not agentWorks.objects.filter(user=agent, work=order).exists():
                    agentWorks.objects.create(
                        user=agent,
                        work=order,
                        status="completed"
                    )

            return redirect('/agent')
        else:
            return HttpResponse("<script>alert('Please select a status.'); window.location='/agent'</script>", status=400)


class report(TemplateView):
    template_name = 'delivery agents/report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agent = agentsignup.objects.get(user_id=self.request.user.id)
        assign1=agentWorks.objects.filter(user=agent)
        context['work']=assign1
        return context