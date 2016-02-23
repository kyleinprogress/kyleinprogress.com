from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.flatpages import views

from django.views.static import serve


urlpatterns = [
    # Blog URLs
    url(r'', include('blog.urls')),

    # Admin URLS
    url(r'^admin/', admin.site.urls),

    # Flatpage URLS
    url(r'^(?P<url>.*/)$', views.flatpage),
    # url(r'^about/$', views.flatpage, {'url': '/about/'}, name='about'),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
