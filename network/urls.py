
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    #API routes
    path("new_post", views.new_post, name="new_post"),
    path("show_posts", views.show_posts, name="show_posts"),
    path("posts/<str:user_name>", views.profile_posts, name="profile_posts"),
    path("profile/<str:user_name>", views.profile, name="profile"),
    path("following_posts", views.following_posts, name="following_posts"),
    path("new_follower/<str:user_name>", views.new_follower, name="new_follower"),
    path("post_edit", views.post_edit, name="post_edit"),
    path("like_post/<int:post_id>", views.like_post, name="like_post"),
]
