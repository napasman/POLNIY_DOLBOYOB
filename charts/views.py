from re import A
from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from posts.models import ApiUser
from ipware import get_client_ip
from .models import WordChart


# Create your views here.
@login_required
def charts(request):
    try:
        api_user = ApiUser.objects.get(user=request.user)
    except ApiUser.DoesNotExist:
        this_ip = get_client_ip(request)[0]
        api_user = ApiUser.objects.create(user=request.user, ip_address=this_ip)

    profiles = WordChart.objects.all()

    # Prepare data for the chart
    labels = ['May-22', 'Jun-22', 'Jul-22', 'Aug-22', 'Sep-22', 'Oct-22', 'Nov-22', 'Dec-22', 'Jan-23', 'Feb-23',
              'Mar-23', 'Apr-23']
    data = []
    for profile in profiles:
        data.append([
            profile.wordMention_May_22,
            profile.wordMention_Jun_22,
            profile.wordMention_Jul_22,
            profile.wordMention_Aug_22,
            profile.wordMention_Sep_22,
            profile.wordMention_Oct_22,
            profile.wordMention_Nov_22,
            profile.wordMention_Dec_22,
            profile.wordMention_Jan_23,
            profile.wordMention_Feb_23,
            profile.wordMention_Mar_23,
            profile.wordMention_Apr_23,
        ])

    context = {
        'labels': labels,
        'api_user': api_user,
        'profiles': profiles,
        'data': data,
    }

    return render(request, "charts.html", context=context)