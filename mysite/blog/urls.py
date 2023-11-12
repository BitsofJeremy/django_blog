from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
   # All posts view from function
   path(
      '',
      views.post_list,
      name='post_list'
   ),

   # All posts view from class view
   # path('', views.PostListView.as_view(), name='post_list'),

   # Get all posts with tag
   path(
      'tag/<slug:tag_slug>/',
      views.post_list,
      name='post_list_by_tag'
   ),
   # Specific post based on year, month, day, and slug
   path(
      '<int:year>/<int:month>/<int:day>/<slug:post>/',
      views.post_detail,
      name='post_detail'
   ),
   # For sharing posts via email
   path(
      '<int:post_id>/share/',
      views.post_share,
      name='post_share'
   ),
   # Add a RSS feed
   path('rss/', LatestPostsFeed(), name='post_feed'),
   # Add Search page
   path('search/', views.post_search, name='post_search')
]
