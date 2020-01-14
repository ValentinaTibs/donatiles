from django.shortcuts import render
from django.http import HttpResponse

from .models import Post

import requests

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})



def blog(request):

    #filter just the ones that have publish date bigger than today
    posts = Post.objects.all()

    return render(request, "blog.html", {"posts": posts})