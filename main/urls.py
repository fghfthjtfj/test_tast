from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('', LayoutRender.as_view(), name='layout_url'),
    path('main_screen', HomePge.as_view(), name='home_url'),
]
