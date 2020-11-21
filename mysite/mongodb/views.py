from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from .models import MongoDB, Host
from .forms import MongoDBCreateConnectionForm


class MongoDBCreateConnectionView(CreateView):
    template_name = "mongodb/create.html"
    form_class = MongoDBCreateConnectionForm
    model = MongoDB
    success_url = reverse_lazy("mongodb:list_connection")

    def post(self, request, *args, **kwargs):
        host = request.POST.get("host").split(",")
        data = {
            "host": host,
            "srv": len(host)==1,
            "db_name": request.POST.get("db_name"),
            "db_user": request.POST.get("db_user"),
            "db_password": request.POST.get("db_password")
        }
        connection_string = MongoDB.generate_connection_string(**data)
        # check connection
        self.object = None
        try:
            client = MongoClient(connection_string, serverSelectionTimeoutMS=3000)
            _ = client.server_info()
        except ServerSelectionTimeoutError:
            messages.add_message(
                request,
                messages.ERROR,
                "Connection Error: Please enter a valid connection string!"
            )
            return self.render_to_response(self.get_context_data())
        
        data.pop("srv")
        print(data)
        form = self.form_class(data=data)
        print(form)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        hosts = (form["host"].data)[-1].split(",")
        data = {
            "db_name": form["db_name"].data,
            "db_user": form["db_user"].data,
            "db_password": form["db_password"].data,
            "srv": len(hosts) == 1
        }
        mg = self.model.objects.create(**data)
        
        for host in hosts:
            temp = host.split(":")
            host_name = temp[0]
            port = temp[1] if len(temp) == 2 else None
            host = Host.objects.create(host_name=host_name, port=port, db=mg)
        return redirect(self.success_url)
        

class MongoDBListView(ListView):
    template_name = "mongodb/list.html"
    model = MongoDB
