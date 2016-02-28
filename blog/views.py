from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe
from django.views.generic import ListView, ArchiveIndexView, YearArchiveView, MonthArchiveView

from .models import Category, Post, Tag
import markdown2

def index(request):
    if request.user.is_staff:
        post_list = Post.objects.all().order_by('-published_date')
    else:
        post_list = Post.objects.published().order_by('-published_date')
    all_categories = Category.objects.all()
    context = {'post_list': post_list, 'all_categories': all_categories}
    return render(request, 'blog/index.html', context)

class PostYearArchiveView(YearArchiveView):
    queryset = Post.objects.exclude(published_date__isnull=True).order_by('-published_date')
    date_field = "published_date"
    make_object_list = True

class PostMonthArchiveView(MonthArchiveView):
    queryset = Post.objects.all()
    date_field = "published_date"
    make_object_list = True

class CategoryListView(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            category = Category.objects.get(slug=slug)
            post_list = Post.objects.filter(category=category)
            return post_list
        except Category.DoesNotExist:
            post_list = Post.objects.none()
            return post_list

class TagListView(ListView):
    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            tag = Tag.objects.get(slug=slug)
            return tag.post_set.all()
        except Tag.DoesNotExist:
            return Post.objects.none()
