from django.contrib.auth.models import User
from django.http import request
from django.core.mail import EmailMessage
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from .forms import customUserCreation,ProfileForm,SkillForm,MessageForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Profile
from .models import Profile,Skill,Message
from .utils import searchProfiles,paginateProfiles
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def loginUser(request):
    page='login'
    context={'page':page}
    if request.user.is_authenticated:
            return redirect('profiles')

    if request.method=='POST':
        username=request.POST['username'].lower()
        password=request.POST['password']
    
        try:
            user=User.objects.get(username=username)
        except:
            print("Username doesn't exist")
            messages.error(request,'Username doesn not exist')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            print("Incorrect username or password")
            messages.error(request,'Incorrect username or password')
        
        

    return render(request,'users/login_register.html',context)

def logoutUser(request):
    logout(request)
    messages.info(request,'You Logged Out')
    return redirect('login')

@csrf_exempt
def registerUser(request):
    page='register'
    form=customUserCreation()
    if request.method == 'POST':
        form=customUserCreation(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            #profile=Profile.objects.create(user=user,username=user.username,email=user.email,name=user.first_name)
            subject="Your acccount got activated"
            email_body="welcome to the Page"
            
            messages.success(request,"Account successfully created")
            login(request,user)
            return redirect('login')
        else:
            messages.error(request,"An error occurred")

    context={'page':page,'form':form}
    return render(request,'users/login_register.html',context)

def profiles(request):
    profiles,search_query=searchProfiles(request)
    custom_range,profiles=paginateProfiles(request,profiles,3)
    context={'profiles':profiles,'search_query':search_query,'custom_range':custom_range}
    return render(request,'users/profiles.html',context)

def userProfile(request,pk):
    profile=Profile.objects.get(id=pk)
    topskills=profile.skill_set.exclude(description__exact="")
    otherskills=profile.skill_set.filter(description__exact="")
    context={"profile":profile,"topskills":topskills,"otherskills":otherskills}
    return render(request,'users/user-profile.html',context)

@login_required(login_url="login")
def userAccount(request):
    profile=request.user.profile
    topskills=profile.skill_set.exclude(description__exact="")
    otherskills=profile.skill_set.filter(description__exact="")
    context={'profile':profile,'topskills':topskills,'otherskills':otherskills}
    return render(request,'users/account.html',context)

@login_required(login_url="login")
def editAccount(request):
    profile=request.user.profile
    form=ProfileForm(instance=profile)  #instance=profile set form with previous answers 
    if request.method == 'POST':
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context={'form':form}
    return render(request,'users/profile_form.html',context)

@login_required(login_url="login")
def createSkill(request):
    profile=request.user.profile
    form=SkillForm()
    if request.method == "POST":
        form=SkillForm(request.POST)
        if form.is_valid():
            skill=form.save(commit=False)
            skill.owner=profile
            skill.save()
            messages.success(request,"Skill successfully added")
            return redirect('account')

    context={'form':form}
    return render(request,'users/skill_form.html',context)


@login_required(login_url="login")
def updateSkill(request,pk):
    profile=request.user.profile
    skill=profile.skill_set.get(id=pk)
    form=SkillForm(instance=skill)
    if request.method == "POST":
        form=SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,"Skill successfully updated")
            return redirect('account')

    context={'form':form}
    return render(request,'users/skill_form.html',context)

@login_required(login_url="login")
def deleteSkill(request,pk):
    profile=request.user.profile
    skill=profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request,"Skill successfully deleted")
        return redirect('account')
    context={'object':skill}
    return render(request,'delete_template.html',context)


@login_required(login_url="login")
def inbox(request):
    profile=request.user.profile
    messageRequests=profile.messages.all()
    unreadCount=messageRequests.filter(is_read=False).count()
    context={'messageRequests':messageRequests,'unreadCount':unreadCount}
    return render(request,'users\inbox.html',context)

@login_required(login_url="login")
def viewMessage(request,pk):
    profile=request.user.profile
    message=profile.messages.get(id=pk)
    if message.is_read==False:
        message.is_read=True
        message.save()
    context={'message':message}
    return render(request,'users\message.html',context)

def createMessage(request,pk):
    recepient=Profile.objects.get(id=pk)
    form=MessageForm()
    try:
        sender=request.user.profile
    except:
        sender=None
    if request.method == 'POST':
        form=MessageForm(request.POST)
        if form.is_valid():
            message=form.save(commit=False)
            message.sender=sender
            message.recepient=recepient

            if sender:
                message.name=sender.name
                message.email=sender.email
            message.save()
            messages.success(request,"Your message was successfully sent")
            return redirect('user-profile',pk=recepient.id)

    context={'recepient':recepient,'form':form}
    return render(request,'users\message_form.html',context)
