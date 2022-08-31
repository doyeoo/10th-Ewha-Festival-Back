from django.urls import path
from .views import *

app_name = 'booth'

urlpatterns = [
    path('', BoothListView.as_view()),
    path('search/', SearchView.as_view()),
    path('<int:pk>/', BoothDetailView.as_view()),
    path('<int:pk>/images/', BoothImageView.as_view()),
    path('<int:pk>/thumnail/', BoothThumnailView.as_view()),
    path('<int:pk>/menus/', MenuListView.as_view()),
    path('<int:pk>/menus/<int:menu_pk>/', MenuDetailView.as_view()),
    path('<int:pk>/likes/', LikeView.as_view()),
    path('<int:pk>/comments/', CommentView.as_view()),
    path('<int:pk>/comments/<int:comment_pk>/', CommentDetailView.as_view()),
]
