from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from .views import person_list, CustomAuthToken, FileTokenView, sample_api, upload_book

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('authors', views.show, name="public_users"),
    # path('upload/', views.upload_book, name='upload_book'),
    path('book', views.view_books, name="book"),
    path('persons/', views.person_list, name='person-list'),
    path('file_token/<int:file_id>/', FileTokenView.as_view(), name='file_token'),
    path('token-auth/', CustomAuthToken.as_view()),
    path('api/sampleapi', views.sample_api),
    path('upload/', upload_book.as_view(), name='file_upload_api'),
    path('file/<int:file_id>/', upload_book.as_view(), name='file_access_api'),
    # path('overview', views.overview, name="overview"),  # type: ignore
]