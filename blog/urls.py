from django.conf.urls import include, url
from django.contrib.sitemaps.views import sitemap
from django.views.generic import ListView, DetailView, ArchiveIndexView

from blog.models import Post, Category
from blog.sitemap import PostSitemap, FlatpageSitemap
from blog.views import PostAllView, PostYearArchiveView, PostMonthArchiveView, CategoryListView

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
    url(r'^archives/(?P<published_date__year>\d{4})/(?P<published_date__month>\d{2})/(?P<slug>[a-zA-Z0-9-]+)/?$', DetailView.as_view(model=Post,)),

    # Comments
    #url(r'^comments/', include('fluent_comments.urls')),

    # Archive Views
    url(r'^archives/$', PostAllView.as_view(), name="post_all_archive"),
    url(r'^archives/(?P<year>[0-9]{4})/$', PostYearArchiveView.as_view(), name="post_year_archive"),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$', PostMonthArchiveView.as_view(month_format='%m'), name="post_month_archive"),

    # Categories
    url(r'^category/(?P<slug>[a-zA-Z0-9-]+)/?$', CategoryListView.as_view(model=Category,paginate_by=10,)),

    # Post RSS feed
    url(r'^feed/$', feeds.LatestPosts()),

    # Sitemap
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
            name='django.contrib.sitemaps.views.sitemap'),
]
