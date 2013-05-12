from datetime import datetime

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from images.models import Image
from diptych.settings import DIPTYCH_USERS

def index(request):
    return HttpResponse("index...")

def detail(request, year, month, day):
    images = []
    dt = datetime(int(year), int(month), int(day))
    users = User.objects.filter(username__in=DIPTYCH_USERS)

    # get the image-pair
    for user in users:
        try:
            img = Image.objects.filter(owner=user).filter(date=dt)[0]
        except:
            pass
        else:
            images.append(img)

    ### Custom SQL from dailyphoto.php

    # get count of total pairs
    s = "select imagedate from photo group by imagedate having count(*) = 2 ORDER BY imagedate"

    # get the date of the previous and next pairs
    nextquery = "select imagedate from (select imagedate from photo group by imagedate having count(*) = 2) as T where 
                  imagedate > '". $date ."' ORDER BY imagedate LIMIT 1"

    prevquery = "select imagedate from (select imagedate from photo group by imagedate having count(*) = 2) as T where 
                  imagedate < '". $date ."' ORDER BY imagedate DESC LIMIT 1"

    # get the date of the first and last pairs
    query = "select imagedate from photo group by imagedate having count(*) = 2 ORDER BY imagedate LIMIT 1;";
    lquery = "select imagedate from photo group by imagedate having count(*) = 2 ORDER BY imagedate DESC LIMIT 1;";

    # get the current day (index into all pairs)
    query = "select count(*) from (select imagedate from photo group by imagedate having count(*) = 2) as T where imagedate <= '". $date ."' ORDER BY imagedate"

    ### END Custom SQL

    if len(images) == 2:
        context = {'images': images, 'date': (year, month, day), 'current_day': 2,  }
        return render_to_response('images/diptych.html', context, context_instance=RequestContext(request))
    else:
        return HttpResponse("No image pair for %s-%s-%s." % (year, month, day))
