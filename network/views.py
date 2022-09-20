from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator  #importing paginator class

from .models import *
from django import forms 


#django form for commenting
class post_form(forms.Form):
    post = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 70px', 'class': 'form-control', 'id':'new_post_body'}), label="New Post:")

# #django form for post editing
# class edit_form(forms.Form):
#     post = forms.CharField(widget=forms.Textarea(attrs={'style': 'height: 40px', 'class': 'form-control', 'id':'edited_post_body'}), label="")

def index(request):
    return render(request, "network/index.html", {
        "post_form": post_form(),
    })


@csrf_exempt
def new_post(request):
    # new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # create object related to the post
    data = json.loads(request.body)     #parse a JSON string and convert it into a Python Dictionary
    body = data.get("body", "")         #get the content
    Post.objects.create(
        user = Profile.objects.get(user=request.user),
        body = body,
        likes = 0
    )
    return JsonResponse({"message": "Posted successfully."}, status=201)


def show_posts(request):
    posts = Post.objects.all().order_by("-timestamp")
    return JsonResponse([post.serialize(request.user) for post in posts], safe=False)



def pagination(request):
    posts = Post.objects.all().order_by("-timestamp")
    post_paginator = Paginator(posts, 10)   #paginate 'posts' list with 10 posts for each page
    page_num = request.GET.get('all_posts/page')    #given url for each page based on page number
    page = post_paginator.get_page(page_num)      #get page



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# displaying posts for each profile
def profile_posts(request, user_name):
    user_account = User.objects.get(username=user_name)
    user_profile = Profile.objects.get(user=user_account)
    posts = Post.objects.filter(user=user_profile).order_by("-timestamp")
    return JsonResponse([post.serialize(request.user) for post in posts], safe=False )

# displaying profile details
def profile(request, user_name):
    user_account = User.objects.get(username=user_name)
    user_profile = Profile.objects.get(user=user_account)
    return JsonResponse(user_profile.serialize(request.user), safe=False )  # serialize takes argument for req_user in models

# display following posts
def following_posts(request):
    following_users = Profile.objects.get(user=request.user).following.all()
    following_users_profiles = Profile.objects.filter(user__in=following_users)     # filtering by a query list -> gives a query list of all profile objects belongs to all objects in the following_users qusery list
    posts = Post.objects.filter(user__in=following_users_profiles).all()         # filtering by a query list -> gives a query list of all posts objects belongs to all objects in the following_users_profile qusery list
    return JsonResponse([post.serialize(request.user) for post in posts], safe=False )      

# follow button
def new_follower(request, user_name):
    new_follower = User.objects.get(username=user_name)
    following_list = Profile.objects.get(user=request.user).following.all()
    if new_follower in following_list:
        new_status = False
        Profile.objects.get(user=request.user).following.remove(new_follower)
    else:
        new_status = True
        Profile.objects.get(user=request.user).following.add(new_follower)
    return JsonResponse({"new_status":new_status, "followers_count":new_follower.followed_by.count()}, status=200)

@csrf_exempt
def post_edit(request):
    data = json.loads(request.body)     #parse a JSON string and convert it into a Python Dictionary
    new_content = data.get("body", "")         #get the content
    post_id = int(data.get("post_id", ""))
    post = Post.objects.get(id=post_id)
    post.body = new_content
    post.save()
    return JsonResponse(post.serialize(request.user), safe=False)
    # return JsonResponse({"new_content":new_content, "post_id":post_id}, status=200)
    # return JsonResponse({"message": "Posted successfully."}, status=200)

def like_post(request, post_id):
    liked_post = Post.objects.get(id=post_id)
    liked_post_list = Profile.objects.get(user=request.user).liked_posts.all()
    if liked_post in liked_post_list:
        new_status = False
        Profile.objects.get(user=request.user).liked_posts.remove(liked_post)
    else:
        new_status = True
        Profile.objects.get(user=request.user).liked_posts.add(liked_post)
    return JsonResponse({"new_status":new_status, "likes_count":liked_post.likes.count()}, status=200)