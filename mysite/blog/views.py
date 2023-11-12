from django.shortcuts import render, get_object_or_404

# Import the send_mail function to send email
from django.core.mail import send_mail

# for pagination on function based views [way 1]
from django.core.paginator import Paginator, \
    EmptyPage, PageNotAnInteger

# Setting up search
# using the django postgres utils
# https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/search/
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

# Adding trigram similarity search
# This searches for 3 letters close together
# https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/search/#trigramsimilarity
# CREATE EXTENSION pg_trgm;  <-- run SQL command on blog DB
from django.contrib.postgres.search import TrigramSimilarity

# Use the ListView class to create a class based view [way 2]
from django.views.generic import ListView

# Working with tags
from taggit.models import Tag

# import our email form, our Comment form, and the SearchForm
from .forms import EmailPostForm, CommentForm, SearchForm

# Import the Count functionality
from django.db.models import Count

# import the Post and Comment models for DB
from .models import Post, Comment


# Way 1, function view
def post_list(request, tag_slug=None):
    """ How to define a view with a function """
    # Get all the posts in the DB
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        # Many-to-many relationships
        # Get the tag object matching tag_slug
        tag = get_object_or_404(Tag, slug=tag_slug)
        # Filter all posts based on tag object from tag_slug _in posts list
        object_list = object_list.filter(tags__in=[tag])
    # Set 3 posts in each page
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'blog/post/list.html',
        {
            'page': page,
            'posts': posts,
            'tag': tag
        }
    )

# Way 2, Class based view
# class PostListView(ListView):
#     """ Same as way 1, but done as a class
#     • Use a specific QuerySet instead of retrieving all objects.
#         Instead of defining a queryset attribute, you could have specified model = Post
#         and Django would have built the generic Post.objects.all() QuerySet for you.
#     • Use the context variable posts for the query results.
#         The default variable is object_list if you don't specify any context_object_name.
#     • Paginate the result, displaying three objects per page.
#     • Use a custom template to render the page. If you don't set a default template,
#         ListView will use blog/post_list.html.
#     """
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    # this searches for a specific post, then renders it
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None
    if request.method == 'POST':
        # A comment was POSTed
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    # List of similar posts
    # Get the list of post tags as IDs in DB
    post_tags_ids = post.tags.values_list('id', flat=True)
    # Get all posts with the same tag IDs, exclude the current post
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # Get 4 posts with the same tag
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
            'similar_posts': similar_posts
        }
    )


def post_share(request, post_id):
    # Retrieve post by id and is published, or 404s
    post = get_object_or_404(Post, id=post_id, status='published')
    # Make sure sent is false
    sent = False

    if request.method == 'POST':
        # Form was submitted via POST
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # Data is dictionary of form fields and their values
            # Send the email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read: {post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            # the actual send function:
            send_mail(subject, message, 'admin@myblog.com',
                      [cd['to']])
            sent = True
    else:
        # Show a empty form on GET request
        form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        }
    )


def post_search(request):
    """
    Takes the query from the GET and does a search
    Using the SearchVector
    Returns the search page
    """
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # Setup the SearchVector for title and body

            # basic search vector
            # search_vector = SearchVector('title', 'body')
            # weighted search vector
            # The default weights are D, C, B, and A,
            # and they refer to the numbers 0.1, 0.2, 0.4, and 1.0, respectively.
            search_vector = SearchVector('title', weight='A') + \
                            SearchVector('body', weight='B')
            # Setup the postgres query,
            # Order by descending rank
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                similarity=TrigramSimilarity(
                    'title', query
                    # Get the similarity over 0.1
                ),).filter(similarity__gt=0.1).order_by('-similarity')
    return render(
        request,
        'blog/post/search.html',
        {
            'form': form,
            'query': query,
            'results': results
        }
    )
