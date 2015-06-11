"""
This is the module in which we code the additionals context processor in order to pass more constants to the templates
"""

from itsmurfs_techblog import settings


def facebook_context_processor(request):
    """
    This processor should be used to pass to the template the facebook's constants
    """

    return {
        'FB_APP_ID': settings.FACEBOOK_APP_ID
    }
