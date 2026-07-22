from django.contrib import admin
from .models import Blog, Blogcategory, State,Lead, Category, City, Business, ServiceCityPage,BlogView

# ---------------------------------------------------------------------------
# Inline helpers
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# State / Category / City  (basic)
# ---------------------------------------------------------------------------
admin.site.register(State)
admin.site.register(Category)
admin.site.register(City)

# ---------------------------------------------------------------------------
# Business
# ---------------------------------------------------------------------------
@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    change_list_template = "admin/business_change_list.html"
    list_display = ("name", "user", "state", "city", "phone")
    list_filter = ("state", "city", "category", "user")
    search_fields = ("name", "phone", "address")

# ---------------------------------------------------------------------------
# Lead
# ---------------------------------------------------------------------------
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    pass

# ---------------------------------------------------------------------------
# MachineCityPage


@admin.register(ServiceCityPage)
class ServiceCityPageAdmin(admin.ModelAdmin):
    list_filter = (
        "service",
        "city",
    )

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
     list_display = (
        "title",
        "category",
        "view_count",
        "created_at",
    )

     def view_count(self, obj):
        return obj.views.count()

     view_count.short_description = "Views"

@admin.register(Blogcategory)
class BlogcategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(BlogView)
class BlogViewAdmin(admin.ModelAdmin):
    list_display = (
        "blog",
        "created_at",
    )
