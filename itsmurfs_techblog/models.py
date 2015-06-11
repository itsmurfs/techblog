import os
from django.db import models
from django.contrib.auth.models import User
from itsmurfs_techblog import settings

import uuid
import os

#TODO make this function more robust and global
def get_file_path(instance, filename):
    """
    this method renames image using a unique identifier
    thanks to http://stackoverflow.com/questions/2673647/enforce-unique-upload-file-names-using-django
    """
    name, ext = os.path.splitext(filename)
    filename = "{name}{uuid}{ext}".format(name=name,uuid=uuid.uuid4(), ext=ext)
    return os.path.join(settings.FILE_UPLOAD_DIRECTORY, 'profile_images', filename)


class Smurf(models.Model):

    #user = models.ForeignKey(User)
    user = models.OneToOneField(User)

    #What you do
    job_title = models.CharField(max_length=50)

    #Company name
    workplace = models.CharField(max_length=150)

    #Geografical zone
    workarea = models.CharField(max_length=60)

    #your job field
    field = models.CharField(max_length=100)

    profile_image = models.ImageField(upload_to=get_file_path)

    #The link to your presentation post (possibly inside techblog :) )
    presentation_post = models.URLField(blank=True)

    short_description = models.CharField(max_length=255)

    num_post = models.IntegerField(default=0)

    @property
    def full_name(self):
        return unicode("{} {}".format(self.user.first_name, self.user.last_name))

    def __unicode__(self):

        return unicode("{} profile".format(self.user.username))


class Mention(models.Model):

    description=models.CharField(max_length=200)

    smurf = models.ForeignKey('Smurf', related_name='mentions')


class ReferenceSite(models.Model):

    link = models.URLField()

    smurf = models.ForeignKey('Smurf', related_name='references')


