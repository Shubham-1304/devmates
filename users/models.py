from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey


# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200, blank=True,null=True)
    email=models.EmailField(max_length=500,blank=True,null=True)
    username=models.CharField(max_length=200, blank=True,null=True)
    location=models.CharField(max_length=200, blank=True,null=True)
    short_intro=models.CharField(max_length=200,blank=True,null=True)
    bio=models.TextField(blank=True,null=True)
    profile_image=models.ImageField(blank=True,null=True,upload_to='profiles/',default="profiles/rabbit1.jpg")
    social_github=models.CharField(max_length=200,blank=True,null=True)
    social_linkedin=models.CharField(max_length=200,blank=True,null=True)
    social_website=models.CharField(max_length=200,blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)


    def __str__(self) -> str:
        return str(self.user.username)

class Skill(models.Model):
    owner=models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,null=True)
    name=models.CharField(max_length=200, blank=True,null=True)
    description=models.TextField(blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self) -> str:
        return self.name


class Message(models.Model):
    sender=models.ForeignKey(Profile,on_delete=models.SET_NULL,blank=True,null=True)
    recepient=models.ForeignKey(Profile,on_delete=models.SET_NULL,blank=True,null=True,related_name="messages")
    name=models.CharField(max_length=200, blank=True,null=True)
    email=models.EmailField(max_length=200, blank=True,null=True)
    subject=models.CharField(max_length=200, blank=True,null=True)
    body=models.TextField()
    is_read=models.BooleanField(default=False,null=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)


    def __str__(self) -> str:
        return self.subject

    class Meta:
        ordering=['is_read','-created']


