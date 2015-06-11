from django.contrib import admin
from itsmurfs_techblog.models import Smurf, Mention, ReferenceSite



class MentionInline(admin.StackedInline):
    model = Mention

class ReferenceSiteInline(admin.StackedInline):
    model = ReferenceSite

class SmurfAdmin(admin.ModelAdmin):
    inlines = [
        MentionInline, ReferenceSiteInline
    ]


admin.site.register(Smurf, SmurfAdmin)