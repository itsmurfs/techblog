from django.db import models

# Create your models here.

from taggit.managers import TaggableManager
from taggit.models import TagBase


class EntryTagsCrossDb(models.Model):

    id_entry = models.CharField(max_length=126, unique=True)

    @property
    def entry(self):
        from techblog.models import Entry

        return Entry.objects.get(pk=self.id_entry)

    tags = TaggableManager()

class MyTag(TagBase):
    pass