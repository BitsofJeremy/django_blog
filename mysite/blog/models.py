from django.db import models
# import the util to reverse a url
from django.urls import reverse
# import timezone helper
from django.utils import timezone
# Import taggit for tagging functionality
from taggit.managers import TaggableManager
# import the user model to fk to
from django.contrib.auth.models import User

import uuid


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    # Create a list of choices
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    # Add a nifty UUID to each post
    blog_uuid = models.CharField(max_length=36, default=uuid.uuid4)

    title = models.CharField(max_length=250)
    # Funky slug maker, makes unique based on date
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    # links to User table and removes posts if user is deleted
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    # Sets date to timezone.now
    publish = models.DateTimeField(default=timezone.now)
    # Auto fills in the date when created
    created = models.DateTimeField(auto_now_add=True)
    # Auto fills in the date when updated
    updated = models.DateTimeField(auto_now=True)
    # Created a dropdown based on  STATUS_CHOICES
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    tags = TaggableManager()

    # Original search by objects
    objects = models.Manager()
    # New custom search for published posts
    published = PublishedManager()

    class Meta:
        # Order posts by date descending
        ordering = ('-publish',)

    def __str__(self):
        # Set the return as the title
        return self.title

    def get_absolute_url(self):
        """ use the get_absolute_url() method in your templates to link to specific posts. """
        # We are getting the post and building a url based on the args
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )


class Comment(models.Model):
    # Post foreign key relates to comments in Post model
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
