from django.contrib.syndication.views import Feed
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe

from .models import Post

import markdown2

class LatestPosts(Feed):
    title = "KyleInProgress"
    link = "/"

    def items(self):
        return Post.objects.exclude(published_date__isnull=True).order_by('-published_date')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        extras = ["fenced-code-blocks", "footnotes"]
        content = mark_safe(markdown2.markdown(smart_text(item.text,encoding='utf-8'),
                                               extras = extras))
        return content
