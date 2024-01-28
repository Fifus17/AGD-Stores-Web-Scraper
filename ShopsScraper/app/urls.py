from django.urls import path
from .views import render_site

urlpatterns = [
    path('', render_site, name='render_site')
]
