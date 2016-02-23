from django.contrib.syndication.views import Feed
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe

from .models import Post

import markdown2

class LatestPosts(Feed):
    title = "KyleInProgress"
    link = "/"

    def items(self):
        # return Post.objects.order_by('-published_date')
        return Post.objects.exclude(published_date__isnull=True).order_by('-published_date')

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.get_absolute_url()

    def item_description(self, item):
        extras = ["fenced-code-blocks"]
        content = mark_safe(markdown2.markdown(force_unicode(item.text),
                                               extras = extras))
        return content
