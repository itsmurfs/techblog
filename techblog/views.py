# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from taggit.models import Tag
from itsmurfs_techblog.models import Smurf
from techblog.models import Entry
from django.db.models import Min, Max, Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from taggit.models import Tag
from django.db.models import Q


 # https://docs.djangoproject.com/en/dev/topics/pagination/
def build_paginator(entries, request, entry_per_page):
    paginator = Paginator(entries, entry_per_page)
    page = request.GET.get('page')
    try:
        paginated_entries = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_entries = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        paginated_entries = paginator.page(paginator.num_pages)
    return paginated_entries



def home(request, tag_slug=None, author_id=None, **kwargs):

    if(tag_slug):
        #The tag page
        tag = get_object_or_404(Tag,slug=tag_slug)
        #We don't need to filter for entry.status because only the published entries have tags
        #entries = [ e.content_object.entry for e in tag.taggit_taggeditem_items.all()]
        entries = Entry.get_tagged_entries(tag.taggit_taggeditem_items)

        authors = User.objects.exclude(smurf__isnull=True)
    elif author_id:
        entries = Entry.objects.filter(author_ids=int(author_id)).filter(status=Entry.PUBLISHED_STATUS)
        authors = [User.objects.get(pk=author_id)] #the home accepts a list of author
    else:
        #The home
        entries = Entry.objects.filter(status=Entry.PUBLISHED_STATUS)
        authors = User.objects.exclude(smurf__isnull=True)

    entries = entries.order_by('-creation_date')

    paginated_entries = build_paginator(entries, request, 5)

    tag_cloud = build_tag_cloud()



    return render(request, 'techblog/home.html', {'paginated_entries':paginated_entries,
                                                  'authors':authors,
                                                   'tag_cloud': tag_cloud})


def build_tag_cloud():

    min=1 #font min size class
    max=5 #font max size class

    #Comput max and min number of items tagged by a tag and store it inside a dict
    #the keys are num_items__min and num_items__max
    annotated_tags=Tag.objects.annotate(num_items=Count('taggit_taggeditem_items')).filter(num_items__gt=0)
    min_max_items_tagged = annotated_tags.aggregate(Max('num_items'),Min('num_items'))

    tag_cloud = []
    for tag in annotated_tags:
        cloud_item = {}
        cloud_item['name'] = tag.name
        cloud_item['num_items'] = tag.num_items
        cloud_item['slug'] = tag.slug

        if tag.num_items == min_max_items_tagged['num_items__min']:
            cloud_item['size_class'] = tag.num_items
        else:
            size_class =(tag.num_items/min_max_items_tagged['num_items__max']) * (max - min) + min
            cloud_item['size_class']=size_class

        tag_cloud.append(cloud_item)

    return tag_cloud



def entry_detail(request, entry_id, slug):
    entry = get_object_or_404(Entry, pk=entry_id)
    if not entry.status == Entry.PUBLISHED_STATUS:
        raise Http404

    tag_cloud = build_tag_cloud()
    latest_entries = Entry.objects.filter(status=Entry.PUBLISHED_STATUS).order_by('-creation_date')
    front_images = entry.get_front_images()
    return render(request, 'techblog/entry_detail.html', {'entry':entry,
                                                          'latest_entries': latest_entries,
                                                          'tag_cloud': tag_cloud,
                                                          'front_images': front_images})


def draft_entry_detail(request, entry_id):

    if not request.user.is_authenticated():
        raise PermissionDenied

    entry = get_object_or_404(Entry, pk=entry_id)

    tag_cloud = build_tag_cloud()
    latest_entries = Entry.objects.filter(status=Entry.PUBLISHED_STATUS).order_by('creation_date')
    return render(request, 'techblog/entry_detail.html', {'entry':entry,
                                                          'latest_entries': latest_entries,
                                                          'tag_cloud': tag_cloud})


def about(request):
    return render(request, 'techblog/about.html')


def authors(request):

    authors_list = Smurf.objects.all()

    return render(request, 'techblog/authors.html', {'authors': authors_list})


