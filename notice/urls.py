from django.urls import path
from .views import *

app_name = 'notice'

urlpatterns = [
    path('', NoticeListView.as_view()),
    path('<int:pk>/', NoticeDetailView.as_view()),
]
