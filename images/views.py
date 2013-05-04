from datetime import datetime
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from images.models import Image
from diptych.settings import DIPTYCH_USERS

def index(request):
    return HttpResponse("index...")

def detail(request, year, month, day):
    images = []
    dt = datetime(int(year), int(month), int(day))
    users = User.objects.filter(username__in=DIPTYCH_USERS)

    for user in users:
        try:
            img = Image.objects.filter(owner=user).filter(date=dt)[0]
        except:
            pass
        else:
            images.append(img)

    if len(images) == 2:
        context = {'images': images, 'date': (year, month, day)}
        return render_to_response('images/diptych.html', context, context_instance=RequestContext(request))
    else:
        return HttpResponse("No image pair for %s-%s-%s." % (year, month, day))
