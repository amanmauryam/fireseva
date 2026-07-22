from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Blog, Business, ServiceCityPage


class StaticSitemap(Sitemap):
    priority = 1.0
    changefreq = "weekly"

    def items(self):
        return [
            "home",
            "about",
            "contact",
            "all_service",
            "blog",
            "find_contractors",
        ]

    def location(self, item):
        return reverse(item)

class ServiceCityPageSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return ServiceCityPage.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

class BusinessSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Business.objects.all()

    def lastmod(self, obj):
        return obj.created_at

class BlogSitemap(Sitemap):
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

sitemaps = {
    "static": StaticSitemap,
    "machine_city": ServiceCityPageSitemap,
    "business": BusinessSitemap,
    "blog": BlogSitemap,
}
