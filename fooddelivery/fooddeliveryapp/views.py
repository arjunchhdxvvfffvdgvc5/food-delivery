from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from fooddeliveryapp.models import userType,Customersignup,restaurentsignup,agentsignup
from django.contrib.auth import login,authenticate
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import login, authenticate
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse

class ForgotPassword(TemplateView):
    template_name = 'forgot_password.html'

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            protocol = 'http'
            domain = request.META['HTTP_HOST']
            reset_url = reverse('password_reset', kwargs={'uidb64': uid, 'token': token})
            reset_url = f"{protocol}://{domain}{reset_url}"
            context = {
                'user': user,
                'protocol': protocol,
                'domain': domain,
                'uid': uid,
                'token': token,
                'reset_url': reset_url,
            }
            message = render_to_string('password_reset_email.html', context)
            send_mail(
                'Password Reset',
                message,
                'your_email@example.com',
                [user.email],
                fail_silently=False,
            )
            return render(request, 'forgot_password_sent.html')
        except User.DoesNotExist:
            return render(request, 'forgot_password.html', {'message': 'Invalid email address'})


class PasswordReset(TemplateView):
    template_name = 'password_reset.html'

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            # Decode the uidb64 to get the user's ID
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)  # Retrieve user by ID
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            # Get the new passwords from the POST request
            new_password = request.POST.get('new_password1')
            new_password_confirmation = request.POST.get('new_password2')

            # Initialize an error message variable
            error_message = None

            # Validations
            if not new_password or not new_password_confirmation:
                error_message = "Both password fields are required."
            elif new_password != new_password_confirmation:
                error_message = "Passwords do not match."
            elif len(new_password) < 8:
                error_message = "Your password must contain at least 8 characters."
            elif new_password.isdigit():
                error_message = "Your password can't be entirely numeric."
            elif new_password.lower() in ['password', '12345678', 'qwerty', 'letmein']:
                error_message = "Your password can't be a commonly used password."
            # You can add more checks here as needed

            if error_message:
                # If there are validation errors, render the template with the error message
                return render(request, 'password_reset.html', {
                    'error': error_message,
                    'uidb64': uidb64,
                    'token': token,
                })

            # If all validations pass, set the new password
            user.set_password(new_password)
            user.save()  # Save the user with the new password
            update_session_auth_hash(request, user)  # Keep the user logged in if needed

            return redirect('success')  # Redirect to success page
        else:
            # Token is invalid or expired
            return render(request, 'password_reset_invalid.html')
        

class SuccessView(TemplateView):
    template_name = 'success.html'

# Create your views here.
class homeview(TemplateView):
    template_name='index.html'


class loginview(TemplateView):
    template_name='login.html'


    def post(self,request,*arg,**kwargs):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)
        if user is not None:

            login(request,user)
            if user.last_name == '1':

                if user.is_superuser:
                    return redirect('/admin')
                elif userType.objects.get(user_id=user.id).type == "customer":
                    return redirect('/customer')
                elif userType.objects.get(user_id=user.id).type == "restaurent":
                    return redirect('/restaurent')
                elif userType.objects.get(user_id=user.id).type == "agent":
                    return redirect('/agent')
            
            else:
                return render(request,'login.html',{'message':"User account Not Authenticated"})
        else:
    
            return render(request,'login.html',{'message':"invalid Username or Password"})
            
class restaurentview(TemplateView):
    template_name='restaurent.html'

    def post(self,request,*args,**kwargs):

        name= request.POST['name']
        username= request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        mobileno=request.POST['phone']
        address=request.POST['address']
        image= request.FILES['image']
        if User.objects.filter(email=email,username=username):
            print ('pass')
            return render(request,'restaurent.html',{'message':"already added the username or email"})

        else:
            user = User.objects.create_user(username=username,password=password,email=email,first_name=name,last_name='0')
            user.save()
            se = restaurentsignup()
            se.user = user
            se.mobile = mobileno 
            se.address = address
            se.image = image
            se.save()
            usertype=userType()
            usertype.user=user
            usertype.type ='restaurent'
            usertype.save()
            return render(request,'restaurent.html',{'message':"successfully added"})



class registerview(TemplateView):
    template_name='register.html'

    def post(self,request,*args,**kwargs):
        # Safely retrieve and validate form data
        name = request.POST.get('name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        mobileno = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        # Check for missing fields
        if not all([name, username, email, password, mobileno, address]):
            return render(request, 'register.html', {'message': 'All fields are required'})

        # Prevent duplicate accounts
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'message': 'Username or email already exists'})

        # Create new user
        user = User.objects.create_user(username=username, password=password, email=email, first_name=name, last_name='0')
        user.save()
        se = Customersignup()
        se.user = user
        se.mobile = mobileno 
        se.address = address
        se.save()
        usertype=userType()
        usertype.user=user
        usertype.type ='customer'
        usertype.save()
        return render(request,'login.html',{'message':"successfully added"})
        
class agentview(TemplateView):
    template_name='agent.html'

    def post(self,request,*args,**kwargs):
        name= request.POST['name']
        username= request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        mobileno=request.POST['phone']
        address=request.POST['address']
        if User.objects.filter(email=email,username=username):
            print ('pass')
            return render(request,'agent.html',{'message':"already added the username or email"})

        else:
            user = User.objects.create_user(username=username,password=password,email=email,first_name=name,last_name='0')
            user.save()
            se = agentsignup()
            se.user = user
            se.mobile = mobileno 
            se.address = address
            se.save()
            usertype=userType()
            usertype.user=user
            usertype.type ='agent'
            usertype.save()
            return render(request,'login.html',{'message':"successfully added"})
