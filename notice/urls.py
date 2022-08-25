from django.urls import path
from .views import *

app_name = 'notice'

urlpatterns = [
    path('list/', NoticeListView.as_view())  # notices/list
]
