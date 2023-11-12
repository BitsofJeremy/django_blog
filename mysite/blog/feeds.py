from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post


class LatestPostsFeed(Feed):
    """
    Build a nice RSS feed for readers
    """
    title = 'My blog'
    link = reverse_lazy('blog:post_list')
    description = 'New posts of my blog.'

    def items(self):
        """
        Get the last 5 published posts
        """
        return Post.published.all()[:5]

    def item_title(self, item):
        """
        Get the title from the post and
        set it as title
        """
        return item.title

    def item_description(self, item):
        """
        Truncate the post body by 30 characters
        """
        return truncatewords(item.body, 30)
