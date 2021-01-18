from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('Home',views.index,name='Home'),
    path('show_books',views.show_books,name="show_books"),
    path('user_Profile',views.user_Profile,name="user_Profile"),
    path('user_books',views.user_books_,name="user_books"),
    path('user_profile',views.profile_,name="user_profile"),
    path('issue_books',views.issue_books,name="issue_books"),
    path('add/<int:book_id>',views.add,name="add"),
    path('add_books',views.issue_books,name="add_books"),
    path('return/<int:book_id>',views.return_book,name='return'),
    path('update_profile',views.update_profile,name='update_profile'),
    path('update',views.update,name='update'),
    path('category/<int:category_no>',views.categoryshow,name='category')
]