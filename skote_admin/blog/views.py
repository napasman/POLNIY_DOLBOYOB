from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class BlogListView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Blog List"
        greeting['pageview'] = "Blog"
        return render (request,'blog/bloglist.html',greeting)

class BlogGridView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Blog Grid"
        greeting['pageview'] = "Blog"
        return render (request,'blog/bloggrid.html',greeting)    

class BlogDetailsView(View):
    def get(self , request):
        greeting = {}
        greeting['heading'] = "Blog Details"
        greeting['pageview'] = "Blog"
        return render (request,'blog/blogdetails.html',greeting)             