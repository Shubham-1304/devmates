from django.core import paginator
from django.shortcuts import render,redirect

from django.http import HttpResponse, request
from .models import Project,Tag
from .forms import ProjectForm,ReviewForm 
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .utils import searchProjects,paginateProjects
from django.core.paginator import Paginator
from django.contrib import messages
from django.shortcuts import render,redirect

lst=[{
    'id':"1",
    'title':'Free Guy',
    'rating':4.2
},
{
    'id':"2",
    'title':'Cruella',
    'rating':4.5
}]
def project(request):
    projects,search_query=searchProjects(request)
    custom_range,projects=paginateProjects(request,projects,3)
    
    context={'msg':"hello",'List':projects,'search_query':search_query,'paginator':paginator,'projects':projects,
    'custom_range':custom_range}
    return render(request,'project/project.html',context)

def singleProject(request,pk):
    #movie=None
    #for i in lst:
     #   if i['id']==pk:
      #      movie=i
    movie=Project.objects.get(id=pk)
    form=ReviewForm()
    if request.method=='POST':
        form=ReviewForm(request.POST)
        review=form.save(commit=False)
        review.project=movie
        review.owner=request.user.profile
        review.save()
        movie.getVoteCount
        messages.success(request,"Your review posted successfully")
        return redirect('singleProject',pk=movie.id)
    tags=movie.tag.all()
    return render(request,'project/single-project.html',{'movie':movie,'tags':tags,'form':form})

@login_required(login_url="login")
def createProject(request):
    form=ProjectForm()
    profile=request.user.profile
    if request.method =='POST':
        newtags=request.POST.get('newtags').replace(","," ").split()
        #print(request.POST)
        form=ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project=form.save(commit=False)
            project.owner=profile
            project.save()
            for tags in newtags:
                tags,created=Tag.objects.get_or_create(name=tags)
                project.tag.add(tags)
            return redirect('project')
    context={'form':form}
    return render(request,'project/project_form.html',context)

@login_required(login_url="login")
def updateProject(request,pk):
    profile=request.user.profile
    project=profile.project_set.get(id=pk)
    form=ProjectForm(instance=project)
    if request.method =='POST':
        newtags=request.POST.get('newtags').replace(","," ").split()
        #print(request.POST)
        form=ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            project=form.save()
            for tags in newtags:
                tags,created=Tag.objects.get_or_create(name=tags)
                project.tag.add(tags)

            return redirect('project')
    context={'form':form}
    return render(request,'project/project_form.html',context)

@login_required(login_url="login")
def deleteProject(request,pk):
    profile=request.user.profile
    project=profile.project_set.get(id=pk)
    if request.method =='POST':
        project.delete()
        return redirect('project')
    context={'object':project}
    return render(request,'delete_template.html',context)

# Create your views here.
