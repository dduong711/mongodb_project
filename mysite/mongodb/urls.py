from django.urls import path

from . import views

app_name = "mongodb"
urlpatterns = [
    path("create/", views.MongoDBCreateConnectionView.as_view(), name="create_connection"),
    path("", views.MongoDBListView.as_view(), name="list_connection")
]