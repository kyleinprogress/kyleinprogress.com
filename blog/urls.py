from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap
from django.views.generic import ListView, DetailView

from blog.models import Post, Category, Tag
from blog.sitemap import PostSitemap, FlatpageSitemap
from blog.views import PostYearArchiveView, PostMonthArchiveView, CategoryListView, TagListView

from . import views, feeds

# Define sitemaps
sitemaps = {
    'posts': PostSitemap,
    'pages': FlatpageSitemap
}

urlpatterns = [
    # Index
    url(r'^$', views.index, name="index"),

    # Individual posts
    url(r'^archive/(?P<published_date__year>\d{4})/(?P<published_date__month>\d{2})/(?P<slug>[a-zA-Z0-9-]+)/?$', DetailView.as_view(
        model=Post,
        )),

    # Archive Views
    url(r'^archive/(?P<year>[0-9]{4})/$',PostYearArchiveView.as_view(),name="article_year_archive"),
    url(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',PostMonthArchiveView.as_view(month_format='%m'),name="archive_month_numeric"),

    # Categories
    url(r'^category/(?P<slug>[a-zA-Z0-9-]+)/?$', CategoryListView.as_view(
        model=Category,
        paginate_by=5,
        )),

    # Tags
    url(r'^tag/(?P<slug>[a-zA-Z0-9-]+)/?$', TagListView.as_view(
        paginate_by=5,
        model=Tag,
        )),

    # Post RSS feed
    url(r'^feed/$', feeds.LatestPosts()),

    # Sitemap
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
            name='django.contrib.sitemaps.views.sitemap'),
]
