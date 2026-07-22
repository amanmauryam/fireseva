
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from app.sitemaps import sitemaps
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('app.urls')),
    path('dashboard/',include('dashboard.urls')),
    path('chaining/', include('smart_selects.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path("sitemap.xml",sitemap,{"sitemaps": sitemaps},name="django.contrib.sitemaps.views.sitemap",),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)