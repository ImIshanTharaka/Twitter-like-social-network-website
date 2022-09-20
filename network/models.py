from urllib import request
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, blank=True, related_name="followed_by")

    def serialize(self,req_user):
        return {
            "id": self.id,
            "user": self.user.username,
            "following": self.following.count(),
            "followers": self.user.followed_by.count(),
            "following_status": not req_user.is_anonymous and self.user in Profile.objects.get(user=req_user).following.all(),
            "follow_availability": not req_user.is_anonymous and self.user != req_user      # users cannot follow themselves
        }

    def __str__(self):
        return f"{self.user} - ID:{self.id}" 

class Post(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(Profile, blank=True, related_name="liked_posts")
        # Post.likes - The Profiles that liked the Post
        # Profile.liked_posts - The Posts that liked by the Profile

    def serialize(self,req_user):
        return {
            "id": self.id,
            "user": self.user.user.username,
            "body": self.body,
            "likes": self.likes.count(),
            "liked_status": not req_user.is_anonymous and self in Profile.objects.get(user=req_user).liked_posts.all(),
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "edit_status": not req_user.is_anonymous and self.user.user == req_user,

        }