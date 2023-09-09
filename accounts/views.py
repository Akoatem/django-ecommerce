from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *


# Reset password
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
#from django.utils.encoding import force_str
from django.utils.encoding import force_text
from django.conf import settings
from django.views import View
import threading



# create the register method

# https://docs.djangoproject.com/en/4.2/contents/


class EmailThread(threading.Thread):
     def __init__(self, email_message):
          self.email_message = email_message
          threading.Thread.__init__(self)
          
     def run(self):
          self.email_message.send()



def register(request):
     if request.method == 'POST':
          first_name = request.POST['first_name']
          last_name = request.POST['last_name']
          username = request.POST['username']
          email = request.POST['email']
          password1 = request.POST['password1']
          password2 = request.POST['password2']
          
          # varification of password
          if password1 == password2:
               if User.objects.filter(username=username).exists():
                    # print('Username taken')
                    messages.info(request, 'Username taken')
                    return redirect('register')
               elif User.objects.filter(email=email).exists():
                    # print('Email taken')
                    messages.info(request, 'Email taken')
                    return redirect('register')
               else:
                    user = User.objects.create_user(first_name=first_name,last_name=last_name,
                                                    username=username,email=email, password=password1)
                   
                    user.save();
                    print('User Created')
                    return redirect('login') 
               
               
          else:
              messages.info(request, 'Password Mismatch')
              return redirect('register')
          return redirect('/')         
     
          
     else:
          return render(request, 'register.html')
 
 


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
            
            
    else:
        return render(request, 'login.html' )
    
    
def logout(request):
        auth.logout(request)
        return redirect('/')
   






class RequestResetEmailView(View):
     def get(self, request):
          return render(request, 'request-reset-email.html')
     
     def post(self, request):
          email = request.POST['email']
          user = User.objects.filter(email=email)
          
          if user.exists():
               current_site = get_current_site(request)
               email_subject = '[Reset Your Password]'
               message = render_to_string('reset-user-password.html', {
                    'domain': '127.0.0.1:8000',
                    'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                    'token': PasswordResetTokenGenerator().make_token(user[0])
               })
               
               email_message = EmailMessage(email_subject,message,
                                            settings.EMAIL_HOST_USER,[email])
               EmailThread(email_message).start()
               
               messages.info(request, "WE HAVE SENT YOU AN EMAIL ON HOW TO RESET YOUR PASSWORD")
               return render(request, 'request-reset-email.html')


class SetNewPasswordView(View):
     def get(self, request, uidb64, token):
          context = {
               'uidb64': uidb64,
               'token': token
          }
           
          try:
             user_id = force_text(urlsafe_base64_decode(uidb64))
             user = User.objects.get(pk=user_id)
               
             if not PasswordResetTokenGenerator().check_token(user,token):
                  messages.warning(request, 'Password Reset Link is Invalid')
                  return render(request, 'request-reset-email.html')
          
          except DjangoUnicodeDecodeError as identifier:
               pass
          
          return render(request, 'set-new-password.html', context)
          
     def post(self, request, uidb64, token):
          context = {
               'uidb64': uidb64,
               'token': token
          }
          password1 = request.POST['password1']
          password2 = request.POST['password2']
       
          if password1 != password2:
               messages.warning(request, 'Password Mismatch')
               return render(request, 'set-new-password.html', context)
          
          try:
             user_id = force_text(urlsafe_base64_decode(uidb64))
             user = User.objects.get(pk=user_id)
             user.set_password(password1)
             user.save()
             messages.success(request, 'Password Reset Successfully, Please login')
             return redirect('login')
          
          except DjangoUnicodeDecodeError as identifier:
              messages.error(request, 'Something Went Wrong')
              return render(request, 'set-new-password.html', context)
         
          return render(request, 'set-new-password.html', context)
                    
      
      
     
               