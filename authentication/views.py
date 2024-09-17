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
    """
    This function renders the home page of the AI Chess web application.

    Parameters:
    request (HttpRequest): The request object containing information about the client's request.

    Returns:
    HttpResponse: The rendered home page template.
    """
    return render(request, 'authentication/index.html')

def register(request):
    # Check if the request is a POST request (form submission)
    if request.method == 'POST':
        # Get form data
        username = request.POST['username']
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        Cpassword = request.POST['confirm_password']
        
        # Check if the username already exists in the database
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        
        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')
        
        # Ensure the username is no longer than 10 characters
        if len(username) > 10:
            messages.error(request, 'Username should not exceed 10 characters')
            return redirect('register')
        
        # Ensure the passwords match
        if password != Cpassword:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
        
         # Ensure the username is alphanumeric
        if not username.isalnum():
            messages.error(request, 'Username should only contain alphanumeric characters')
            return redirect('register')
        
        # Create the user but don't activate yet
        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        
        # Display a success message after account creation
        messages.success(request, "Your account was successfully created! We have sent a confirmation email.")
        
         # Send a welcome email to the user with a confirmation link
        subject = "Welcome to AI Chess - Confirm Your Email"
        message = "Welcome " + myuser.first_name + "to AI Chess!\nPlease confirm your email address."
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        
        # Send the welcome email
        send_mail(subject, message, from_email, to_list, fail_silently=False)

        # Generate email confirmation details
        current_site = get_current_site(request)
        email_subject = 'Confirm your email @ AI Chess website'
        uid = urlsafe_base64_encode(force_bytes(myuser.pk))
        token = generate_token.make_token(myuser)
        
         # Create the body of the confirmation email
        email_body = (
        f"Hi {myuser.first_name},\n\n"
        "Please confirm your email by clicking the link below:\n"
        f"http://{current_site.domain}/activate/{uid}/{token}\n\n"
        "Thank you for joining AI Chess!"
        )
        
         # Send the confirmation email
        email = EmailMessage(
        email_subject,
        email_body,
        settings.EMAIL_HOST_USER,  # Sender email
        [myuser.email]  # Recipient email
        )

        email.send(fail_silently=False)  # Send the email, raise errors if they occur
        
        # Redirect the user to the login page after successful registration
        return redirect('login')
        
     # If it's a GET request, render the registration form template
    return render(request, 'authentication/register.html')

def user_login(request):
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Retrieve username and password from the submitted form
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user with the provided credentials
        user = authenticate(username=username, password=password)
        
        # If authentication is successful (user exists and credentials are correct)
        if user is not None:
            # Log the user in by attaching the user object to the request session
            login(request, user)
            # Display a success message after successful login
            messages.success(request, 'Your account has successfully logged in')
            # Redirect to the home page after login
            return redirect('home')
        else:
            # If authentication fails, show an error message
            messages.error(request, 'Invalid username or password')
            # Redirect back to the login page
            return redirect('login')
        
    # If the request method is GET, render the login form page
    return render(request, 'authentication/login.html')

def user_logout(request):
    # Log the user out by clearing their session data
    logout(request)

    # Display a success message after logging out
    messages.success(request, "You have successfully logged out")

    # Redirect the user to the home page after logging out
    return redirect('home')

def activate(request, uid64, token):
    try:
        # Decode the user ID (uid) from the base64-encoded string
        uid = force_str(urlsafe_base64_decode(uid64))
        # Get the user object corresponding to the decoded user ID
        myuser = User.objects.get(pk=uid)
    
    # Catch any exceptions during decoding or user retrieval
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        # If an error occurs, set myuser to None
        myuser = None
    
    # If the user object exists and the token is valid, activate the user
    if myuser is not None and generate_token.check_token(myuser, token):
        # Activate the user's account
        myuser.is_active = True
        myuser.save() # Save the changes to the user model (activation)
        
        # Log the user in after activation
        login(request, myuser)
        # Display a success message upon successful activation
        messages.success(request, 'Your email has been confirmed')
        
        # Redirect the user to the home page after successful activation

        return redirect('home')

    # If the user object does not exist or the token is invalid, render the failed activation template
    else:
        # If activation fails, show an error message
        messages.error(request, 'Activation link is invalid!')

        # Render the activation failed template
        return render(request, 'activation_failed.html')
