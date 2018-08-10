
from django.urls import path, include, re_path
from .views import index, show_log
app_name="myspy"
urlpatterns = [
    path('', index ,name='index'),
    path('log', show_log ,name='log'),
]
