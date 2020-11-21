from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from .models import MongoDB
from .forms import MongoDBCreateConnectionForm


class MongoDBCreateConnectionView(CreateView):
    template_name = "mongodb/create.html"
    form_class = MongoDBCreateConnectionForm
    model = MongoDB
    success_url = reverse_lazy("mongodb:list_connection")

    def post(self, request, *args, **kwargs):
        connection_string = request.POST.get("connection_string")
        print(connection_string)
        # check connection
        try:
            client = MongoClient(connection_string, serverSelectionTimeoutMS=3000)
            _ = client.server_info()
        except ServerSelectionTimeoutError:
            messages.add_message(
                request,
                messages.ERROR,
                "Connection Error: Please enter a valid connection string!"
            )
            self.object = None
            return self.render_to_response(self.get_context_data())
        
        return super().post(request, *args, **kwargs)


class MongoDBListView(ListView):
    template_name = "mongodb/list.html"
    model = MongoDB
