from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.http import request
from .models import Profile
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render,redirect
from django.views import View
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .utils import tokenGenerator


def profileDeleted(sender,instance,**kwargs):
    user=instance.user
    user.delete()

#@receiver(post_save,sender=Profile)
def profileUpdated(sender,instance,created,**kwargs):
    print("Profile Triggered")
    if created==True:
        user=instance
        profile=Profile.objects.create(user=user,username=user.username,email=user.email,name=user.first_name)
        subject="Welcome to our page"
        #send_mail(subject,
        #message,
        #settings.EMAIL_HOST_USER,
        #[profile.email],
        #fail_silently=False)
        uidb64=urlsafe_base64_encode(force_bytes(profile.pk))
        domain="127.0.0.1:8000/"
        link=reverse('activate',kwargs={'uidb64':uidb64,'token':tokenGenerator.make_token(profile)})
        activate_url="http://"+domain+link
        message="Welcome "+profile.username + \
            " Please use this link to activate\n"+activate_url
        

        email = EmailMessage(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [profile.email],

            )
        email.send(fail_silently=True)
        

def updateUser(sender,instance,created,**kwargs):
    profile=instance
    user=profile.user
    if created==False:
        user.first_name=profile.name
        user.username=profile.username
        user.email=profile.email
        user.save()

class verificationView(View):
    def get(self,request,uidb64,token):
        return redirect('login')
           


post_save.connect(updateUser,sender=Profile)
post_save.connect(profileUpdated,sender=User)
post_delete.connect(profileDeleted,sender=Profile)
