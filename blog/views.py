from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

import datetime as dt

from blog.models import Post

def blog(request, the_filter = None):

	all_post = Post.objects.filter(publication__publish_date__lte= dt.datetime.now(), deleted = False)
	return render(request, "blog.html",{ 	
		"all_post":all_post,	
		})


def post(request, post_slug):

	try: 
	    post = Post.objects.get(publication__publish_date__lte= dt.datetime.now(), deleted = False, publication__slug  = post_slug )
	except ObjectDoesNotExist:
	    return render(request, "404.html",{"message":"The post you asked to view is not existing",}) 

	return render(request, "post.html",{ 	
		"post":post,	
		})