from __future__ import absolute_import
from celery import shared_task
from django.contrib.auth.models import User
from crossdb_utils.models import EntryTagsCrossDb
from techblog.models import Entry


@shared_task
def entry_OneToOne_entryTagsCrossDb_check():
    """
    It compares the total number of the "records" of both models.
    If it equals then the integrity check will success
    else there wil be an inconsistency.
    """
    entry_count = Entry.objects.count()
    entry_tag_cross_db_count = EntryTagsCrossDb.objects.count()

    if entry_count != entry_tag_cross_db_count:
        #TODO improve and test!!!!
        return "Error: entry count = {} while entry tag cross db count = {}".format(entry_count, entry_tag_cross_db_count)
    else:
        return "OK"

@shared_task
def author_ManyToMany_entry_check(): #Old it was OneToMany before adding multiple authors
    """
     It executes a full table scan to get all the user's id and a full collection scan to get the author_id of each entry
     then builds a set of both results.
     The check will success if every author_id is contained in the user id list.


    """
    import itertools
    entry_author_ids = itertools.chain(*Entry.objects.all().values_list('author_ids', flat=True))
    entry_author_ids_set = set(entry_author_ids)
    user_ids = set(User.objects.all().values_list('id',flat=True))

    author_id_not_in_user = entry_author_ids_set - user_ids

    if author_id_not_in_user:
        return ("Error: There are entries without a correct cross relation with user: {}"
                .format(",".join(str(s) for s in author_id_not_in_user)))
    else:
        return "OK"

