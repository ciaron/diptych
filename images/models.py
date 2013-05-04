import os
from datetime import datetime
from time import strptime, mktime
from django.db import models
from django.contrib.auth.models import User
from PIL import Image as PImage

class Image(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(max_length = 100, blank = True)
    caption = models.CharField(max_length = 250, blank = True)
    date = models.DateField(blank = True, default = datetime.now(), help_text="Dates entered here will be overwritten by the file's EXIF date. If you need to change the date, upload the file without EXIF")
    image = models.ImageField(upload_to ="photos/originals/%Y/%m/")

    def __unicode__(self):
        return self.image.name

    def save(self, *args, **kwargs):

        i = PImage.open(self.image)
        info = i._getexif()
        
        # TODO: we might be correcting the date, i.e. ignoring EXIF

        if info != None:
            if info.has_key(36867):
                # 36867 = Exif.DateTimeOriginal (http://www.awaresystems.be/imaging/tiff/tifftags/privateifd/exif/datetimeoriginal.html)
                dts = strptime(info[36867], "%Y:%m:%d %H:%M:%S")
                self.date = datetime.fromtimestamp(mktime(dts))
        
        super(Image, self).save(*args, **kwargs)

    ## delete is done with a custom Admin action - see admin.py
