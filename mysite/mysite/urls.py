from django.urls import path, include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap

sitemaps = {
       'posts': PostSitemap,
}

urlpatterns = [
    # admin url
    path('admin/', admin.site.urls),
    # blog url
    path('blog/', include('blog.urls', namespace='blog')),
    # Add a sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap')
]