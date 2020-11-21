from django import forms

from .models import MongoDB


class MongoDBCreateConnectionForm(forms.ModelForm):
    host = forms.CharField(label="Host : Port(Optional)", max_length=4096)
    #db_name = forms.CharField(label="Database name", max_length=256)
    #db_user = forms.CharField(label="Database User", max_length=256)
    #db_password = forms.CharField(label="Database Password", max_length=256)

    class Meta:
        model = MongoDB
        fields = ["db_name", "db_user", "db_password"]