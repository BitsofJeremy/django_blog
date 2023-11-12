from django.contrib import admin
from .models import Post, Comment


# Use the decorator to register Posts in admin site
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # List out the columns to view in admin site
    list_display = (
        'title',
        'slug',
        'author',
        'publish',
        'status'
    )
    # Right side admin site filter
    list_filter = (
        'status',
        'created',
        'publish',
        'author'
    )
    # Search field. What to search?
    search_fields = (
        'title',
        'body'
    )
    # This pre-populates the slug
    # auto-slugify in action
    prepopulated_fields = {
        'slug': ('title',)
    }
    # Set author to column primary key
    # eg admin == 1
    raw_id_fields = ('author',)
    # Sets the ability to sort by date by Year, Month, Day
    date_hierarchy = 'publish'
    # Sets the ability to column sort by status and date published
    ordering = (
        'status',
        'publish'
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # List out the columns to view in admin site
    list_display = ('name', 'email', 'post', 'created', 'active')
    # Filter by in admin
    list_filter = ('active', 'created', 'updated')
    # Search field. What to search?
    search_fields = ('name', 'email', 'body')
    # Sets the ability to sort by date by Year, Month, Day
    date_hierarchy = 'created'
    # Sets the ability to column sort by status and date published
    ordering = (
        'created',
    )