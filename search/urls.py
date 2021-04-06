
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.query_search, name="query_search"),
    path('readMore/', views.watchTrailer, name = "readMore"),
    path('download/', views.download, name = "download"),
]

