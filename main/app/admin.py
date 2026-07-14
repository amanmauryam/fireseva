from django.urls import path
from django.contrib import admin
from .models import Blog, Blogcategory, State,Lead, Category, City, Business, ServiceCityPage,BlogView
from django.shortcuts import get_object_or_404, render,redirect
import openpyxl
from django.contrib import messages
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
    list_display = ("name", "user", "category_name", "state", "city", "phone")
    list_filter = ("state", "city", "category", "user")
    search_fields = ("name", "phone", "address")
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="Category")
    def category_name(self, obj):
        return obj.category.name
    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "import-excel/",
                self.admin_site.admin_view(self.import_excel),
                name="business_import_excel",
            ),
        ]

        return custom_urls + urls
    
    def import_excel(self, request):
        if request.method == "POST":
            success_count = 0
            errors = []
            state_id = request.POST.get("state")
            city_id = request.POST.get("city")
            category_id = request.POST.get("category")
            excel_file = request.FILES.get("excel")
            if not excel_file:
                messages.error(request, "Please select an Excel file.")
                return render(request, "admin/business_import.html", context)
            state = get_object_or_404(State, id=state_id)
            city = get_object_or_404(City, id=city_id)
            category = get_object_or_404(Category, id=category_id)
            workbook = openpyxl.load_workbook(excel_file)
            sheet = workbook.active
            for row_number, row in enumerate(sheet.iter_rows(min_row=2,values_only=True), start=2):
                name = row[0]
                phone = row[1]
                google_map_image = row[2]
                address = row[3]
                sub_category = row[4]
                if not name:
                    errors.append(f"Row {row_number}: Name is missing.")
                    continue
                if not phone:
                    errors.append(f"Row {row_number}: Phone is missing.")
                    continue
                
                Business.objects.create(
                    
                    name=name,
                    phone=phone,
                    google_map_image=google_map_image,
                    address=address,
                    state=state,
                    city=city,
                    category=category,
                    sub_category = sub_category
                )
                success_count= success_count+1
            messages.success(request,f"{success_count} businesses imported successfully.")
            for error in errors:
                messages.error(request, error)
            return redirect(request.path)    
        states = State.objects.all()
        category = Category.objects.all()
        cities = City.objects.all()
        context ={
            'states': states,
            'category': category,
            'cities': cities
        }

        return render(request, "admin/business_import.html", context)
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
