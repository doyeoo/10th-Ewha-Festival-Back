from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('', ProfileView.as_view()),
    path('likes/', LikedListView.as_view()),
]
