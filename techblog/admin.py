import json
import re
import repr
from __builtin__ import object
from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.exceptions import PermissionDenied
from django.forms import widgets, CharField, TextInput, FileField, ImageField
from django.utils.encoding import force_text
from django.utils.text import slugify
from django.forms import ModelForm, CharField
from taggit.models import Tag
from taggit.utils import edit_string_for_tags
from techblog import forms

from techblog.models import Entry, CodeSnippet


class EntryForm(ModelForm):

    front_image_upload = ImageField(label="Front image")
    tags = forms.MyTagField()
    other_authors = CharField(label="Other author(s)",
                              required=False,
                              help_text="specify a comma-separated list of usernames",
                              widget=TextInput(attrs={'style':'width:100%'}))

    class Meta:
        model = Entry
        exclude = ('author_ids','slug','permalink', 'code_snippets','drafted_tags', 'modified_by_id', 'front_image')
        widgets = {
            'meta_description': widgets.Textarea(),
            'wordcount': widgets.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):

        super(EntryForm, self).__init__(*args, **kwargs)

        if 'instance' in kwargs:
            #Update mode
            obj = kwargs['instance']
        else: #Creation mode
            obj = None

        if obj:
            if obj.status == Entry.PUBLISHED_STATUS:
                initial_tags = edit_string_for_tags(obj.tags_list)
            else:
                initial_tags = ','.join(obj.drafted_tags)

            initial_other_authors = [user.username for user in obj.authors]
            self.fields['other_authors'].label = "Author(s)"
            if obj.front_image:
                initial_image = type('ImgTemp', (object,),
                                     { "url": force_text(obj.front_image),
                                       '__unicode__': lambda self : unicode(self.url)})()
                self.fields['front_image_upload'].initial = initial_image
        else:
            initial_tags = None
            initial_other_authors = []


        self.fields['tags'].initial=initial_tags
        #Get all available tags and set it inside the form field. These will be used by tag-it plugin to perform
        #the autocomplet on the widget
        self.fields['tags'].available_tags = json.dumps([ tag.name for tag in Tag.objects.all()])

        self.fields['other_authors'].initial = ", ".join(initial_other_authors)

    def save(self, commit=True, user=None):

        if not user:
            raise PermissionDenied("No user provided")

        instance = super(EntryForm, self).save(commit=False)

        #Automatic fields:
        instance.slug = slugify(instance.title)

        #Main authors (the logged user)
        if not instance.pk:
            #Creation mode
            instance.authors = [user]
        else:
            #Update mode
            instance.modified_by = user
            #Clean the old authors if any
            instance.author_ids = None

        #Other authors (All the authors if in update mode)
        if self.cleaned_data['other_authors']:
            authors = [x.strip() for x in self.cleaned_data['other_authors'].split(',')]
            authors_id = [ user.id for user in User.objects.filter(username__in=authors)]
            instance.authors = authors_id


        code_to_model = instance.process_html()

        if code_to_model:
            #If there are new code inserted let's rebuild the entire list
            instance.code_snippets = []

        for (code,attrs) in code_to_model:
            code_snippet = CodeSnippet()
            code_snippet.code = code
            code_snippet.description = unicode(attrs['data-description'])
            code_snippet.language = unicode(attrs['data-language'])
            code_snippet.file_name = unicode(attrs['data-file_name'])
            instance.code_snippets.append(code_snippet)

        instance.save()

        if 'front_image_upload' in self.changed_data:
            instance.insert_front_image(self.cleaned_data['front_image_upload'])

        #after saving the entry we can fill the tags with the ones provided by the user
        #we add them as taggit-tags only if the status of the entry is set to published
        if instance.status == Entry.PUBLISHED_STATUS:
            instance.tags.set(*self.cleaned_data['tags'])
            instance.drafted_tags = []
        else:
            #We store the tags as a list of strings
            instance.drafted_tags = self.cleaned_data['tags']
            instance.tags.clear()

        return instance


class EntryAdminForm(admin.ModelAdmin):

    form = EntryForm

    list_display = ('title', 'display_authors', 'creation_date','modified_by', 'modification_date', 'status', 'display_tags')
    list_filter = ('status',)
    search_fields = ('title',)
    save_on_top = True

    def display_tags(self, obj):
        return ", ".join([t.name for t in obj.tags_list])
    display_tags.short_description = 'Tags'

    def display_authors(self, obj):
        return ", ".join([u.username for u in obj.authors])
    display_authors.short_description = 'Author(s)'

    # def get_queryset(self, request):
    #     """
    #     https://docs.djangoproject.com/en/1.6/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_queryset
    #     In this case we show only the user's entries. If the user is a superuser we show all entries.
    #     """
    #     qs = super(EntryAdminForm, self).get_queryset(request)
    #     if request.user.is_superuser:
    #         return qs
    #
    #     return qs.filter(author_id=request.user.id)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(EntryAdminForm, self).get_search_results(request, queryset, search_term)
        #Search the term inside the tags and retrieve all the entry with that tag
        try:
            tag = Tag.objects.get(name__iexact=search_term)
            if tag:
                entries_queryset = Entry.get_tagged_entries(tag.taggit_taggeditem_items)
                queryset |= entries_queryset
        except Tag.DoesNotExist:
            #If tag does not exists simply return the normal query
            pass

        return queryset, use_distinct

    def save_form(self, request, form, change):
        """
        Given a ModelForm return an unsaved instance. ``change`` is True if
        the object is being changed, and False if it's being added.

        override and shadowing of super(EntryAdminForm, self).save_form
        in order to pass the logged user to the form
        """

        return form.save(commit=False, user=request.user)

admin.site.register(Entry, EntryAdminForm)