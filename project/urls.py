from django.urls import path
from . import views

urlpatterns = [
    path('',views.project,name="project"),
    path('single-project/<str:pk>/',views.singleProject,name="singleProject"),
    path('create-project/',views.createProject,name="create-project"),
    path('update-project/<str:pk>/',views.updateProject,name="update-project"),
    path('delete-project/<str:pk>/',views.deleteProject,name="delete-project"),
]