from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
import os
from PIL import Image

#http://javiergodinez.blogspot.fi/2008/03/square-thumbnail-with-python-image.html
def _thumbnail(img, size):
    width, height = img.size
    
    if width > height:
        delta = width - height
        left = int(delta/2)
        upper = 0
        right = height + left
        lower = height
    else:
        delta = height - width
        left = 0
        upper = int(delta/2)
        right = width
        lower = width + upper
    
    img = img.crop((left, upper, right, lower))
    img.thumbnail(size, Image.ANTIALIAS)
    return img

class Room(models.Model):
    name = models.CharField(max_length=32)
    createdBy = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name


class Message(models.Model):
    content = models.TextField(max_length=1000)
    responseTo = models.ForeignKey('Message', blank=True, null=True, related_name='responses')
    room = models.ForeignKey(Room)
    writer = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.content[:30]

class UserExtra(models.Model):
    user = models.OneToOneField(User)
    img = models.ImageField(upload_to='images', verbose_name="Select Your Profile Image", blank=True, null=True)
    thumbnail = models.ImageField(upload_to='images', blank=True, null=True)
    
    def save(self):
        try:
            this = UserExtra.objects.get(user = self.user)
            self.id = this.id #force update instead of insert
            if self.img and this.img != self.img:
                os.remove(this.img.path)
                if this.thumbnail:
                    os.remove(this.thumbnail.path)
        except:
            pass
        if self.img:
            super(UserExtra, self).save()
            tsize = 35,35
            isize = 700,700
            fname, ext = os.path.splitext(self.img.name)
            outfilepath = os.path.splitext(self.img.path)[0] + ".thumbnail" + ext
            outfilefield = fname + ".thumbnail" + ext
            im = Image.open(self.img.path)
            im = _thumbnail(im, tsize)
            im.save(self.img.path, im.format)
            im.thumbnail(isize, Image.ANTIALIAS)
            im.save(outfilepath, im.format)
            self.thumbnail = outfilefield
        super(UserExtra, self).save()

    def __unicode__(self):
        return self.user.username


admin.site.register(Room)
admin.site.register(Message)
admin.site.register(UserExtra)
