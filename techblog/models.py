# Create your models here.
from HTMLParser import HTMLParseError
from django.contrib.auth.models import User

from django.db import models


# Create your models here.
from djangotoolbox.fields import EmbeddedModelField, ListField
import shutil
from taggit.models import Tag

from crossdb_utils.models import EntryTagsCrossDb
from itsmurfs_techblog.settings import FILE_UPLOAD_DIRECTORY, MEDIA_ROOT, FILE_UPLOAD_TEMP_DIRECTORY, FRONT_IMAGE_SIZES, \
    MEDIA_URL, SITE_DOMAIN
from mongoadminforms.fields import SimpleListFormField

from techblog.html_utils import HtmlTool
from mongoadminforms.models import ListEmbeddedModelFieldWithForm, ListFieldWithForm, ListFieldWithSimpleForm

import PIL.Image
import os.path



class Entry(models.Model):

    PUBLISHED_STATUS = 'pub'
    DRAFT_STATUS = 'draft'

    STATUS_CHOICES = ((PUBLISHED_STATUS,'published'), (DRAFT_STATUS,'draft'))

    title = models.CharField(max_length=100, unique=True)  # inserted by: user

    meta_description = models.CharField(max_length=255, verbose_name="summary")  # inserted by: user

    content = models.TextField()  # inserted by: user

    creation_date = models.DateField(auto_now_add=True)  # automatic

    wordcount = models.IntegerField()  # automatic

    # this field contains thee cross database foreign keys to user table
    author_ids = ListField(null=True) # automatic

    # this field is the cross database foreign key to user table
    modified_by_id = models.IntegerField(null=True) # automatic

    modification_date = models.DateField(auto_now=True)  # automatic


    @property # thanks to http://stackoverflow.com/questions/6618002/python-property-versus-getters-and-setters
    def authors(self):
        #Cross db query
        usr_ids = [x for x in self.author_ids]
        return User.objects.filter(pk__in=usr_ids)

    @authors.setter
    def authors(self, value):

        #First of all initialize the author_ids list field:
        if not self.author_ids:
            self.author_ids = []

        if isinstance(value, list):
            for u in value:
                if isinstance(u, User):
                    self.author_ids.append(u.id)
                elif isinstance(u, int):
                    self.author_ids.append(u)
                else:
                    raise TypeError("Authors must be a list of User, found {}".format(type(u)))
        else:
            raise TypeError("Authors must be a list of User, found {}".format(type(value)))


    @property # thanks to http://stackoverflow.com/questions/6618002/python-property-versus-getters-and-setters
    def modified_by(self):
        #Cross db query
        return User.objects.get(pk=self.modified_by_id)

    @modified_by.setter
    def modified_by(self, value):
        if isinstance(value, User):
            self.modified_by_id = value.id
        elif isinstance(value, int):
            self.modified_by_id = value
        else:
            raise TypeError()


    @property
    def tags(self):
        #Cross db query with taggit
        #If a DoesNotExists will be raised then something wrong is happened during insertion.
        return EntryTagsCrossDb.objects.get(id_entry=self.id).tags

    @property
    def tags_list(self):
        """
        Convenient method to retrieve always a list of tags even when the entry is in drafted state.
        In this way it doesn't need to check the status of the entry outside the entry for retrieve the tags list
        """
        if self.status == Entry.PUBLISHED_STATUS:
            return self.tags.all()
        elif self.status == Entry.DRAFT_STATUS:
            return [Tag(name=t, slug=t) for t in self.drafted_tags]

    def similar_entries(self):
        #TODO Use dynamic query
        return [e.entry for e in self.tags.similar_objects()]

    @classmethod
    def get_tagged_entries(cls, tagged_items):

        p = None

        for count, e in enumerate(tagged_items.all()):
            if count==0:
                p = Q(id=e.content_object.id_entry)
            else:
                p = p | Q(id=e.content_object.id_entry)

        return Entry.objects.filter(p)

    #This fields is used to store temporarily the tags without creating the Taggit object
    #We have to do this in order to preserve the integrity and the security of the tag clouds
    #Indeed if we made the Taggit objects also for the drafted entries we would have incoherent data between the
    #entries displayed and the number of entry with a certain tags.
    drafted_tags = ListField()

    #Like tags but these will be only inserted inside meta-keywords head metatag. These should be a collection of
    #most probably searched keyword.
    seo_keywords = ListFieldWithSimpleForm(blank=True)

    slug = models.SlugField()  # automatic

    #This will be saved in mongo as a string containing the full path
    front_image = models.ImageField(upload_to=FILE_UPLOAD_TEMP_DIRECTORY, null=True)  # inserted by: user if not get the content's first image

    demo_attachment = models.URLField(blank=True, null=True)  # inserted by: user

    git_link = models.URLField(blank=True, null=True)  # inserted by: user

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT_STATUS)

    #parsed from content, show as readonly in admin form
    references = ListEmbeddedModelFieldWithForm(EmbeddedModelField('Reference'), blank=True, null=True)

    #parsed from content when the form is submitted
    code_snippets = ListEmbeddedModelFieldWithForm(EmbeddedModelField('CodeSnippet'), blank=True, null=True)

    #see https://docs.djangoproject.com/en/1.6/ref/models/instances/#django.db.models.Model.get_absolute_url
    def get_absolute_url(self):
        """
        this is the permalink
        """
        from django.core.urlresolvers import reverse
        if self.status == Entry.PUBLISHED_STATUS:
            return reverse('entry_detail', kwargs={'entry_id': self.id, 'slug':""})
        elif self.status == Entry.DRAFT_STATUS:
            return reverse('draft_entry_detail', kwargs={'entry_id': self.id})

    def _generate_front_image_sized_name(self, original_file_name, size):
        fileName, fileExtension = os.path.splitext(original_file_name)
        size_str = "{}x{}".format(size[0], size[1])
        new_file_name = "{filename}-{size}{ext}".format(filename=fileName,
                                                        size=size_str,
                                                        ext=fileExtension)
        return new_file_name

    def _generate_resized_front_image(self, img, new_directory, original_file_name):

        if FRONT_IMAGE_SIZES:
            for social, size in FRONT_IMAGE_SIZES:
                rimg = img.resize(size)
                new_file_name = self._generate_front_image_sized_name(original_file_name, size)

                rimg.save(os.path.join(new_directory, new_file_name))

    def _get_upload_path(self):
        return os.path.join(MEDIA_ROOT,FILE_UPLOAD_DIRECTORY, self.id)

    def _get_upload_url(self):
        return os.path.join(SITE_DOMAIN,MEDIA_URL[1:],FILE_UPLOAD_DIRECTORY, self.id)

    def get_front_images(self):
        if FRONT_IMAGE_SIZES and self.front_image:
            front_images = {}
            for social, size in FRONT_IMAGE_SIZES:
                original_file_name = os.path.basename(self.front_image.name)
                image_name = self._generate_front_image_sized_name(original_file_name, size)
                front_images[social] = os.path.join(self._get_upload_url(),'front_image', image_name)
            #add the original image
            front_images['original'] = unicode(self.front_image)
            return front_images
        else:
            return None

    def insert_front_image(self, in_memory_image):
        """
        This method provides the capability of saving the front image inserted by the user in different
        size. One for each social network or other content sharing provided. It uses pillow to resize the image.
        It stores the images resized as long as the original image in the personal directory of the entry.
        """

        img = PIL.Image.open(in_memory_image)
        new_directory = os.path.join(self._get_upload_path(), "front_image")
        original_file_name = "".join(os.path.basename(in_memory_image.name).split())
        new_path = os.path.join(new_directory, original_file_name)


        if not os.path.exists(new_directory):
            os.makedirs(new_directory)
        else:
            #https://docs.python.org/2/library/shutil.html#shutil.rmtree
            shutil.rmtree(new_directory)
            os.makedirs(new_directory)

        img.save(new_path)

        self.front_image = os.path.join(self._get_upload_url(), "front_image",original_file_name)

        self._generate_resized_front_image(img, new_directory, original_file_name)



    def has_references(self):

        return bool([ref.link for ref in self.references if ref.link!=''])


    def process_html(self):
        """
        This method elaborate the content of thi entry in order to apply pygments to each tag div with class code

        :return:
        """

        try:
            html_parser = HtmlTool(self.content)
        except HTMLParseError:
            return False


        #A list of couple (code_pyg_div, data_attrs_as_dict)
        codes_to_model = html_parser.apply_pygments_to_code_tags()

        #get the content parsed with the modification applied by apply_pygments_to_code_tags
        self.content = html_parser.get_html_parsed_as_string()

        return codes_to_model

    def save(self, *args, **kwargs):

        self.title = self.title.title()

        super(Entry, self).save(*args, **kwargs)


    def __unicode__(self):

        return self.title


class CodeSnippet(models.Model):
    code = models.TextField()  # inserted by: user

    # inserted by: user with a listbox whose values must be compatible with pygments
    language = models.CharField(max_length=255)

    description = models.CharField(max_length=255)  # inserted by: user

    file_name = models.CharField(max_length=50, null=True)  # inserted by: user


class Reference(models.Model):
    title = models.CharField(max_length=250)  # inserted by: user

    link = models.URLField()  # inserted by: user

    description = models.CharField(max_length=255, blank=True)  # meta-content, inserted by: user




###################################################################################################################
#
#                                                  SIGNALS
#
#################################################################################################################




from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.signals import post_delete, post_save


##################################################################
#
#           Author_referential_constraint
#
##################################################################


def author_referential_constraint(sender, instance, **kwargs):
    """
    This method will reassign the author_id of the deleted user to the admin user id
    :param sender: User class
    :param instance: user deleted
    """
    potentials_users = User.objects.filter(Q(is_active=True)|Q(is_superuser=True)|Q(is_staff=False))
    if potentials_users:
        default = potentials_users[0]
    else:
        default = -1

    entries_with_author_deleted = Entry.objects.filter(author_id=instance.id)
    for entry in entries_with_author_deleted:
        entry.author = default
        entry.save()

post_delete.connect(author_referential_constraint, sender=User)

##################################################################
#
#           Tags_referential_constraint
#
##################################################################

def add_tags_referential_constraint(sender, instance, **kwargs):

    #created is a flag which means that the object is in creation or, when false, it is in update
    if 'created' in kwargs and kwargs['created']:

        tagsCross = EntryTagsCrossDb.objects.create()
        tagsCross.id_entry = instance.id
        tagsCross.save()


def delete_tags_referential_constraint(sender, instance, **kwargs):
    try:
        entry_tag = EntryTagsCrossDb.objects.get(id_entry=instance.id)
        entry_tag.delete()
    except EntryTagsCrossDb.DoesNotExist:
        pass


post_save.connect(add_tags_referential_constraint, sender=Entry)

post_delete.connect(delete_tags_referential_constraint, sender=Entry)


##################################################################
#
#               Num_post Count
#
##################################################################

def recount_num_post(sender, instance, **kwargs):
    #Recount num published post for the authors of this entry
    for author in instance.authors:
        num_post = Entry.objects.filter(status=Entry.PUBLISHED_STATUS).filter(author_ids=author.id).count()
        author.smurf.num_post = num_post
        author.smurf.save()


post_save.connect(recount_num_post, sender=Entry)

post_delete.connect(recount_num_post, sender=Entry)


##################################################################
#
#               Delete upload directory of deleted entry
#
##################################################################

def delete_upload_dir(sender, instance, **kwargs):

    new_directory = instance._get_upload_path()
    if os.path.exists(new_directory):
        shutil.rmtree(new_directory)


post_delete.connect(delete_upload_dir, sender=Entry)