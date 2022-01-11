from .models import Profile,Skill
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


def paginateProfiles(request,profiles,results=0):
    page=request.GET.get('page')
    results=results
    paginator=Paginator(profiles,results)
    try:
        profiles = paginator.page(page)
    except:
        page=1
        profiles = paginator.page(1)
    leftIndex=(int(page)-4)
    if leftIndex<1:
        leftIndex=1
    rightIndex=(int(page)+5)
    if rightIndex>paginator.num_pages:
        rightIndex=paginator.num_pages+1
    custom_range=range(leftIndex,rightIndex)
    return custom_range,profiles

def searchProfiles(request):
    search_query=''
    if request.GET.get('search_query'):
        search_query=request.GET.get('search_query')
    skills=Skill.objects.filter(name__icontains=search_query)
    profiles=Profile.objects.distinct().filter(Q(name__icontains=search_query) | Q(short_intro__icontains=search_query) |
    Q(skill__in=skills))

    return profiles,search_query

class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp: int) -> str:
        return (text_type(user.id)+text_type(user.pk)+text_type(timestamp))

tokenGenerator=AppTokenGenerator()