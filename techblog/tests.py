"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.contrib.auth.models import User

from django.test import TestCase
from django.test.runner import DiscoverRunner
from itsmurfs_techblog.models import Smurf

from techblog.models import Entry, EntryTagsCrossDb
from django.conf import settings


class TechblogRunner(DiscoverRunner):

    def __init__(self, *args, **kwargs):
        super(TechblogRunner, self).__init__(*args, **kwargs)

        self.mongodb_name = 'test_%s' % (settings.MONGO_DATABASE_NAME, )

    def setup_databases(self, **kwargs):
        from mongoengine.connection import connect, disconnect
        disconnect()
        connect(self.mongodb_name)
        print 'Creating mongo test database ' + self.mongodb_name
        return super(TechblogRunner, self).setup_databases(**kwargs)

    def teardown_databases(self, old_config, **kwargs):
        from mongoengine.connection import get_connection, disconnect
        connection = get_connection()
        connection.drop_database(self.mongodb_name)
        print 'Dropping mongo test database: ' + self.mongodb_name
        disconnect()
        super(TechblogRunner, self).teardown_databases(old_config, **kwargs)


def fill_entry_db(entries_number, **kwargs):
    """
    This is an utility method to fill the db with a entry_numer of entries.
    This is useful for test purpose.
    :param entries_number:
    :param kwargs: it must contains (field_name, field_value) pairs. If it is passed then the new created entries will be
     modified with these information
    """

    import copy

    entries = Entry.objects.all()

    if not entries:
        raise Exception("At least one entry must be present")

    entry_sample = entries[0]

    for i in range(entries_number):
        new_entry = copy.deepcopy(entry_sample)
        new_entry.id=None
        new_entry.title = "{} {}".format(entry_sample.title, i)

        if kwargs:
            for (k,v) in kwargs.iteritems():
                setattr(new_entry, k,v)

        new_entry.save()


def revert_entry_db():

    for count, entry in enumerate(Entry.objects.all()):
        if count!=0:
            entry.delete()


def create_sample_entry(author_id):

    entry_sample = Entry()
    entry_sample.author_ids = [author_id]
    entry_sample.title = 'First entry'
    entry_sample.subtitle = 'This is our first entry'
    entry_sample.meta_description = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam sit amet volutpat
                                    lacus. Curabitur ultrices sed turpis et ullamcorper.
                                    Quisque aliquet ipsum ut massa porta viverra."""
    entry_sample.content = """<h1><span style="font-family: 'arial black', 'avant garde'; font-size: 18pt;">Title 1</span></h1>
    <p style="padding-left: 30px;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam sit amet volutpat lacus. Curabitur ultrices sed turpis et ullamcorper. Quisque aliquet ipsum ut massa porta viverra. Aenean eleifend justo sed justo pellentesque, eu convallis neque tempus. Curabitur ac ultricies eros, id pretium magna. Sed eu quam et lacus feugiat elementum. Nullam egestas nunc vitae massa bibendum, vehicula molestie est bibendum. Vivamus vitae luctus nibh, in egestas orci. Sed nibh orci, interdum a ultricies eget, gravida accumsan mauris. Nullam porttitor velit sem, a tempus eros condimentum euismod.</p>
    <p>&nbsp;</p>
    <table class="code highlighttable highlighted" data-description="Python models" data-file_name="models.py" data-language="Python">
    <tbody>
    <tr>
    <td class="linenos">
    <div class="linenodiv">
    <pre><a href="#-1">1</a>
    <a href="#-2">2</a>
    <a href="#-3">3</a>
    <a href="#-4">4</a>
    <a href="#-5">5</a>
    <a href="#-6">6</a></pre>
    </div>
    </td>
    <td class="code">
    <div class="highlight">
    <pre><span id="line-1"><span class="kn">from</span> <span class="nn">django.db</span> <span class="kn">import</span> <span class="n">models</span>
    </span><span id="line-2">
    </span><span id="line-3"><span class="k">class</span> <span class="nc">Author</span><span class="p">(</span><span class="n">models</span><span class="o">.</span><span class="n">Model</span><span class="p">):</span>
    </span><span id="line-4">    <span class="n">name</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">100</span><span class="p">)</span>
    </span><span id="line-5">    <span class="n">title</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">CharField</span><span class="p">(</span><span class="n">max_length</span><span class="o">=</span><span class="mi">3</span><span class="p">)</span>
    </span><span id="line-6">    <span class="n">birth_date</span> <span class="o">=</span> <span class="n">models</span><span class="o">.</span><span class="n">DateField</span><span class="p">(</span><span class="n">blank</span><span class="o">=</span><span class="bp">True</span><span class="p">,</span> <span class="n">null</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span>
    </span></pre>
    </div>
    </td>
    </tr>
    </tbody>
    </table>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
    <p>Sed sed ornare urna, eu blandit velit. Etiam consequat et nibh eu eleifend. Sed justo erat, accumsan ac ligula nec, molestie laoreet nulla. Phasellus hendrerit felis nec sem mollis, vitae convallis risus ornare. Ut lacinia, metus id pretium facilisis, leo arcu ultrices sem, vel auctor felis est sed nisi. Morbi malesuada eu nulla sit amet vulputate. <span style="text-decoration: underline;"><em><strong>Pellentesque accumsan ipsum vitae ligula molestie laoreet. Nunc dapibus ante urna, vitae laoreet mauris sagittis vel. Mauris vestibulum nisi eget iaculis pulvinar. In justo urna, molestie non tortor non, iaculis auctor augue.</strong></em></span> Cras eget odio non ligula commodo pulvinar vel ut ligula. Fusce ullamcorper lacus eu magna ornare, vitae sagittis metus venenatis. Fusce ornare libero non viverra lacinia. Donec id pellentesque eros. Phasellus et sapien lectus.</p>
    <p style="text-align: center;">Cras aliquet nunc a sapien posuere pulvinar ut eu libero. Sed nec erat velit. Praesent ligula nisl, vulputate vel tellus vitae, auctor tincidunt arcu. Vivamus et congue mauris, id tincidunt sapien. Sed tincidunt aliquet enim id ullamcorper. <span style="text-decoration: line-through;">Nulla quam mauris, ultricies nec massa vel, accumsan congue sem. Ut eu vestibulum massa, ac ornare dolor. Phasellus accumsan enim non viverra laoreet. Cras gravida, risus sit amet pretium condimentum, enim nisi vehicula arcu, eu placerat odio eros at lectus</span>. Donec rutrum orci id nulla consequat pellentesque. Proin et orci venenatis, convallis turpis nec, interdum quam. Mauris viverra, erat sit amet fermentum blandit, sem lacus scelerisque ligula, et congue massa sem vel neque. Integer at lacus dictum leo adipiscing faucibus a et augue. Vestibulum vel nunc gravida, vulputate lectus sit amet, tincidunt nisl. Sed lacus turpis, consequat at malesuada et, luctus a tellus.</p>
    <h2 style="text-align: left;">Title 2</h2>
    <p>Sed gravida dui in diam laoreet, condimentum pulvinar ipsum tempus. Maecenas accumsan erat non nulla dignissim semper. In nulla turpis, bibendum sit amet bibendum vel, egestas sed felis. Sed ultricies sed libero suscipit fermentum. Donec ante lorem, elementum sit amet vehicula at, sollicitudin sit amet enim. In laoreet mattis dui, in molestie leo lobortis vel. Sed id fringilla dolor, at semper urna. Morbi ut mollis erat. Nulla mollis tortor sit amet placerat lobortis. Maecenas ultricies dictum consequat.</p>
    <p>Sed pharetra, nisi ac sodales gravida, metus erat blandit nisl, ut fringilla justo neque at urna. Donec ornare porttitor arcu eu dapibus. Nullam nec dui sem. Phasellus a ipsum urna. Vivamus velit erat, ultrices adipiscing massa eget, aliquam convallis metus. Sed et quam molestie, pretium turpis eget, sagittis odio. Etiam mollis dapibus nulla eu aliquam. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Phasellus ligula sem, rutrum ac egestas vitae, tempus quis velit.</p>
    <p>&nbsp;</p>
    <table class="code highlighttable highlighted" data-description="Html code" data-file_name="" data-language="HTML">
    <tbody>
    <tr>
    <td class="linenos">
    <div class="linenodiv">
    <pre><a href="#-1">1</a>
    <a href="#-2">2</a>
    <a href="#-3">3</a>
    <a href="#-4">4</a>
    <a href="#-5">5</a>
    <a href="#-6">6</a>
    <a href="#-7">7</a></pre>
    </div>
    </td>
    <td class="code">
    <div class="highlight">
    <pre><span id="line-1"><span class="nt">&lt;pre&gt;</span>
    </span><span id="line-2">Text in a pre element
    </span><span id="line-3">is displayed in a fixed-width
    </span><span id="line-4">font, and it preserves
    </span><span id="line-5">both      spaces and
    </span><span id="line-6">line breaks
    </span><span id="line-7"><span class="nt">&lt;/pre&gt;</span>
    </span></pre>
    </div>
    </td>
    </tr>
    </tbody>
    </table>
    <p>&nbsp;</p>
    <p>&nbsp;</p>
    <table class="code highlighttable highlighted" data-description="linux source" data-file_name="" data-language="Debian Sourcelist">
    <tbody>
    <tr>
    <td class="linenos">
    <div class="linenodiv">
    <pre><a href="#-1">1</a>
    <a href="#-2">2</a></pre>
    </div>
    </td>
    <td class="code">
    <div class="highlight">
    <pre><span id="line-1"><span class="k">deb</span> <span class="s">http://site.example.com/debian</span> <span class="kp">distribuzione</span> <span class="kp">elemento1</span> <span class="kp">elemento2</span> <span class="kp">elemento3</span>
    </span><span id="line-2"><span class="k">deb-src</span> <span class="s">http://site.example.com/debian</span> <span class="kp">distribuzione</span> <span class="kp">elemento1</span> <span class="kp">elemento2</span> <span class="kp">elemento3</span></span></pre>
    </div>
    </td>
    </tr>
    </tbody>
    </table>"""

    entry_sample.wordcount = 561
    entry_sample.front_image = 'http://www.schoolmate.it/j/images/stories/puffi/GrandePuffo.jpg'
    entry_sample.status = Entry.PUBLISHED_STATUS
    entry_sample.save()

def create_smurfs(username, is_superuser=False):

    if is_superuser:
        user = User.objects.create_superuser(username, 'admin@admin.it', 'admin')
    else:
        user = User.objects.create_user(username,)

    smurf = Smurf()
    smurf.user = user
    smurf.job_title = "test job"
    smurf.field = "test filed"
    smurf.short_description ="test short desc"
    smurf.workarea = "test workarea"
    smurf.workplace ="test workplace"

    smurf.save()

    return user



class CrossDbOneToManyRelationsTest(TestCase):

    entries_number = 10

    def setUp(self):
        create_smurfs('admin', is_superuser=True)
        self.user = create_smurfs('pippo')
        create_sample_entry(self.user.id)
        #entries number - 1 because we have just created the sample entry
        fill_entry_db(self.entries_number-1, **{'author': self.user})


    def test_signal_add_tags_referential_constraint(self):

        self.assertEqual(EntryTagsCrossDb.objects.all().count(),self.entries_number)

    def test_signal_post_delete_author(self):

        #Delete the user in order to send the signal
        self.user.delete()

        self.assertEqual(Entry.objects.filter(author_id__isnull=True).count(),0)






