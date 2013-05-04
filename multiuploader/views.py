from django.shortcuts import get_object_or_404, render_to_response
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
#importing json parser to generate jQuery plugin friendly json response
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

import logging
from sorl.thumbnail import get_thumbnail

from images.models import Image

log = logging

@login_required(login_url='/login/')
def upload(request):
    return render_to_response('multiuploader/upload.html', {'STATIC_URL': settings.STATIC_URL})

@csrf_exempt
def multiuploader_delete(request, pk):
    """
    View for deleting photos with multiuploader AJAX plugin.
    made from api on:
    https://github.com/blueimp/jQuery-File-Upload
    """
#    if request.method == 'POST':
#        log.info('Called delete image. image id='+str(pk))
#        image = get_object_or_404(MultiuploaderImage, pk=pk)
#        image.delete()
#        log.info('DONE. Deleted photo id='+str(pk))
#        return HttpResponse(str(pk))
#    else:
#        log.info('Received not POST request to delete image view')
#        return HttpResponseBadRequest('Only POST accepted')
    return HttpResponseBadRequest('Not implemented yet')

@csrf_exempt
def multiuploader(request):
    """
    Main Multiuploader module.
    Parses data from jQuery plugin and makes database changes.
    """

    """ 
    CL
    Instead of using MultiuploaderImage as the model, need to use our own
    Image model.
    """

    user = User.objects.filter(username=request.user)[0]

    if request.method == 'POST':
        log.info('received POST to main multiuploader view')
        if request.FILES == None:
            return HttpResponseBadRequest('Must have files attached!')

        #getting file data for farther manipulations
        file = request.FILES[u'files[]']
        wrapped_file = UploadedFile(file)
        filename = wrapped_file.name
        file_size = wrapped_file.file.size
        log.info ('Got file: "%s"' % str(filename))
        log.info('Content type: "$s" % file.content_type')

        image = Image()
        image.filename = str(filename)
        image.image = file
        image.title = "" 
        image.caption = "" 
        image.owner = user
        image.save()

        log.info('File saving done')

        #getting thumbnail url using sorl-thumbnail
        if 'image' in file.content_type.lower():
            im = get_thumbnail(image, "80x80", quality=50)
            thumb_url = im.url
        else:
            thumb_url = ''

        #settings imports
        try:
            file_delete_url = settings.MULTI_FILE_DELETE_URL+'/'
            file_url = settings.MULTI_IMAGE_URL+'/'
        except AttributeError:
            file_delete_url = 'multi_delete/'
            file_url = 'multi_image/'

#        file_url='image/1/edit' # becomes /upload/image/1/edit
        file_url = '/account/image/' + str(image.id) + '/edit'

        #generating json response array
        result = []
        result.append({"name":filename, 
                       "size":file_size, 
                       "url":file_url, 
                       "thumbnail_url":thumb_url,
                       "delete_url":file_delete_url+str(image.pk)+'/', 
                       "delete_type":"POST",})
        response_data = simplejson.dumps(result)
        
        #checking for json data type
        #big thanks to Guy Shapiro
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)
    else: #GET
        return HttpResponse('Only POST accepted')

def multi_show_uploaded(request, key):
    """Simple file view helper.
    Used to show uploaded file directly"""
    image = get_object_or_404(Image, key_data=key)
    url = settings.MEDIA_URL+image.image.name
    return render_to_response('multiuploader/one_image.html', {"multi_single_url":url,})
