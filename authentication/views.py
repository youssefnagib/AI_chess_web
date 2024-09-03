from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from AI_chess_web import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from django.template.loader import render_to_string


def home(request):
    return render(request, 'authentication/index.html')

def register(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST['username']
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        Cpassword = request.POST['confirm_password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')
        
        if len(username) > 10:
            messages.error(request, 'Username should not exceed 10 characters')
            return redirect('register')
        
        if password != Cpassword:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        
        if not username.isalnum():
            messages.error(request, 'Username should only contain alphanumeric characters')
            return redirect('register')
        
        # Create the user but don't activate yet
        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        
        messages.success(request, "Your account was successfully created! We have sent a confirmation email.")
        
        # Send welcome email
        subject = "Welcome to AI Chess - Confirm Your Email"
        message = f"Welcome {myuser.first_name} to AI Chess!\nPlease confirm your email address."
        send_mail(subject, message, settings.EMAIL_HOST_USER, [myuser.email], fail_silently=False)

        # Email address confirmation
        current_site = get_current_site(request)
        email_subject = 'Confirm your email @ AI Chess website'
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        email = EmailMessage(email_subject, message2, settings.EMAIL_HOST_USER, [myuser.email])
        email.send(fail_silently=False)
            
        return redirect('login')
        
    return render(request, 'authentication/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            messages.success(request, 'Your account has successfully logged in')
            return render(request, 'authentication/index.html', {'fname': fname})
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request, 'authentication/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out")
    return redirect('home')

def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        myuser = User.objects.get(pk=uid)
    
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
        
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, 'Your email has been confirmed')
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')
