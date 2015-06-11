from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',

    url(r'^$', 'techblog.views.home', name='home'),
    url(r'tag/(?P<tag_slug>\w+)/$', 'techblog.views.home', name='home'),
    url(r'author/(?P<author_id>\d*)/(?P<username>\w*)$', 'techblog.views.home', name='home'),
    url(r'entry-detail/(?P<entry_id>\w*)/(?P<slug>\w*)', 'techblog.views.entry_detail', name='entry_detail'),
    url(r'draft-entry-detail/(?P<entry_id>\w*)', 'techblog.views.draft_entry_detail', name='draft_entry_detail'),

    url(r'authors/', 'techblog.views.authors', name='authors'),
    url(r'about/', 'techblog.views.about', name='about')




)

if settings.DEBUG:
    #this works only in debug mode to serve uploaded files in the development server.
    # https://docs.djangoproject.com/en/dev/howto/static-files/#serving-files-uploaded-by-a-user-during-development
    urlpatterns = urlpatterns +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)