from django import template
from django.db.models import Count
# Add markdown utils
from django.utils.safestring import mark_safe
import markdown

from ..models import Post

# Instantiate the register to create a
# custom jinja template tag
register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
	"""
	Adding Markdown tag
	This will render markdown correctly
	place on post.body|markdown
	"""
	return mark_safe(markdown.markdown(text))


@register.simple_tag
def total_posts():
	"""
	Register as a simple_tag that returns a string
	New tag = {{ total_posts }}
	Return the number of posts in DB
	"""
	return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
	"""
	Register a inclusion tag
	Get the latest posts from DB
	Order by the date published, descending
	Send to template as 'latest_posts'
	"""
	latest_posts = Post.published.order_by('-publish')[:count]
	return {'latest_posts': latest_posts}


# Register a simple tag
@register.simple_tag
def get_most_commented_posts(count=5):
	"""
	Only return the top 5 posts with highest comments
	Return the total number of comments for each post
	Stored as total_comments
	"""
	return Post.published.annotate(
		total_comments=Count('comments')
	).order_by('-total_comments')[:count]
