import re
from django.core.exceptions import ValidationError
from taggit.forms import TagField




class MyTagField(TagField):

    def __init__(self, *args, **kwargs):
        super(MyTagField, self).__init__(*args, **kwargs)

        self.validators.append(self.check_for_dash)

    def clean(self, value):
        cleaned_value = super(MyTagField, self).clean(value)

        upper_cleaned_value = []
        for v in cleaned_value:
            upper_cleaned_value.append(v.lower())


        return  upper_cleaned_value


    def check_for_dash(self, values):
        #TODO with Django 1.7 use RegexValidator with inverse_match=True
        for value in values.split(','):
            #This regex disallow all the special characters except the dot.
            #To allows more special chars add a ^\<specialchar> inside the first []
            #To disallows other things to be added you have to add a regex on the right side of the | (like [_]
            if re.search(r'[^\w^\.]|[_]', value):
                raise ValidationError("Enter a valid 'tag' consisting of one single word with only letters and numbers.")