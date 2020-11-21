from django import forms

from .models import MongoDB


class MongoDBCreateConnectionForm(forms.ModelForm):

    class Meta:
        model = MongoDB
        fields = ("connection_string", )
