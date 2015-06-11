# from django.contrib.auth.models import User
# from django.db.models import Q
# from django.db.models.signals import post_delete
# from django.dispatch import receiver
# from techblog.models import Entry
#
#
# def author_referential_constraint(sender, instance, **kwargs):
#     """
#     This method will reassign the author_id of the deleted user to the admin user id
#     :param sender: User class
#     :param instance: user deleted
#     """
#     potentials_users = User.objects.filter(Q(is_active=True)|Q(is_superuser=True)|Q(is_staff=False))
#     if potentials_users:
#         default = potentials_users[0]
#     else:
#         default = -1
#
#     entries_with_author_deleted = Entry.objects.filter(author_id=instance.id)
#     for entry in entries_with_author_deleted:
#         entry.author = default
#         entry.save()
#
#
#
# post_delete.connect(author_referential_constraint, sender=User )