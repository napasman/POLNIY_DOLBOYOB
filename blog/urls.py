from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from blog.utils import handler404  # Import the handler404 function from the correct location
from django.views.generic import TemplateView
from django.contrib.staticfiles.views import serve as serve_static

admin.autodiscover()

handler404 = 'blog.utils.handler404'  # Update the handler404 variable to the correct location

urlpatterns = [
    path('ckeditor', include('ckeditor_uploader.urls')),
    path("sitemap.xml", sitemap, {"sitemaps": {"cmspages": CMSSitemap}}),
    path('admin/clearcache/', include('clearcache.urls')),
    path("admin/", admin.site.urls), 
    path("skote/", include("skote_admin.urls")),
    path("users/",include("authentication.urls")),
    path("users/",include("charts.urls")),
    path('', include(('posts.urls', 'posts'), namespace='posts')),
    path("", include("cms.urls")),
    path('', include('django.contrib.auth.urls')),
    
    
]


# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('robots.txt', serve_static, {'path': 'robots.txt'}),
]