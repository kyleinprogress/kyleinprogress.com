from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe
from django.views.generic import DetailView, ListView, ArchiveIndexView, YearArchiveView, MonthArchiveView, TemplateView

from .models import Category, Post
import markdown2

def Index(request):
    if request.user.is_staff:
        post_list = Post.objects.all().order_by('-published_date')
    else:
        post_list = Post.objects.published().order_by('-published_date')
    all_categories = Category.objects.all()
    context = {'post_list': post_list, 'all_categories': all_categories}
    return render(request, 'blog/_main.html', context)


class PostViewMixin(object):
    date_field = 'published_date'
    paginate_by = 10

    def get_allow_future(self):
        return self.request.user.is_staff

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.all()
        else:
            return Post.objects.published()

class PostAllView(PostViewMixin, ArchiveIndexView):
    pass

class PostYearArchiveView(PostViewMixin, YearArchiveView):
    make_object_list = True
    allow_empty = True

class PostMonthArchiveView(PostViewMixin, MonthArchiveView):
    make_object_list = True
    allow_empty = True

class CategoryListView(ListView):
    template_name = 'blog/category_list.html'

    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            category = Category.objects.get(slug=slug)
            post_list = Post.objects.filter(category=category)
            return post_list
        except Category.DoesNotExist:
            post_list = Post.objects.none()
            return post_list

    def get_context_data(self, **kwargs):
        slug = self.kwargs['slug']
        context = super(CategoryListView, self).get_context_data(**kwargs)
        try:
            context['category'] = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            context['category'] = Category.objects.none()
        return context
