from django.contrib import admin
from django.urls import path
from Actors import views, auto_completion_actors

urlpatterns = [
    path("admin/", admin.site.urls),
    path('search/', views.search_movies, name='search_movies'),
    path('auto_complete/', auto_completion_actors.auto_completion, name='auto_complete'),
]
