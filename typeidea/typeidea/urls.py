"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from django.conf import settings
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.contrib.sitemaps import views as sitemap_views
from django.views.decorators.cache import cache_page
from django.views.static import serve
from blog.apis import PostViewSet,CategoryViewSet
from blog.views import (
    IndexView,CategoryView,TagView,
    PostDetailView,aurl,
    SearchView,AuthorView,
    login,register,newblog,
    Favoritelist,quit,
    ChangeFavorite,addpost,
)
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from config.views import LinkListView
from comment.views import CommentView
from .autocomplete import CategoryAutocomplete,TagAutocomplete
from django.contrib import admin
# from blog.views import post_list,post_detail
# from blog.apis import post_list,PostList

router = DefaultRouter()
router.register(r'post',PostViewSet,base_name='api-post')
router.register(r'category',CategoryViewSet,base_name='api-category')

urlpatterns = [
    url(r'^$', IndexView.as_view(),name='index'),
    # url(r'^$', loginstatus,name='loginstatus'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(),name='category-list'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(),name='tag-list'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'^comment/$', CommentView.as_view(), name='comment'),
    url(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),
    url(r'^post/(?P<post_id>\d+).html$', PostDetailView.as_view(),name='post-detail'),
    url(r'^links/$', LinkListView.as_view(),name='links'),
    url(r'^admin/', xadmin.site.urls, name='xadmin'),
    # url(r'^super_admin/', admin.site.urls,name='super-admin'),
    url(r'^rss|feed/', LatestPostFeed(), name='rss'),
    url(r'^sitemap\.xml$', cache_page(60 * 20, key_prefix='sitemap_cache_')(sitemap_views.sitemap),
                      {'sitemaps': {'posts': PostSitemap}}),
    url(r'^category-autocomplete/$', CategoryAutocomplete.as_view(), name='category-autocomplete'),
    url(r'^tag-autocomplete/$', TagAutocomplete.as_view(), name='tag-autocomplete'),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^api/docs/', include_docs_urls(title='typeidea apis')),
    url(r'^aurl/', aurl,name='aurl'),
    url(r'^login/',login,name='login'),
    url(r'^register/',register,name='register'),
    url(r'^newblog/',newblog,name='newblog'),
    url(r'^favoritelist/$',Favoritelist,name='favoritelist'),
    # url(r'^changefavorite/(\d+).html$',changefavorite,name='changefavorite'),
    url(r'^changefavorite/(?P<post_id>\d+).html$',ChangeFavorite.as_view(),name='change-favorite'),
    url(r'^quit/$',quit,name='quit'),
    url(r'^addpost/$',addpost,name='addpost'),
    url(r'^media/(?P<path>.*)',serve,{'document_root':settings.MEDIA_ROOT}),
    # url(r'^sitemap\.xml$', sitemap_views.sitemap,{'sitemaps':{'posts':PostSitemap}}),
    # url(r'^api/post/',PostList.as_view(),name='post-list'),
    # url(r'^api/post/',post_list,name='post-list'),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/',include(debug_toolbar.urls)),
    ] + urlpatterns
    # urlpatterns += [url(r'^silk/',include('silk.urls',namespace='silk'))]