from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from smart_selects.db_fields import ChainedForeignKey
from django.core.validators import FileExtensionValidator
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field
from django.urls import reverse


def convert_image_to_webp(instance, field_name):
    image_field = getattr(instance, field_name)

    if not image_field:
        return False

    try:
        img = Image.open(image_field.path)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Resize
        img.thumbnail((1200, 1200))

        buffer = BytesIO()
        img.save(
            buffer,
            format="WEBP",
            quality=80,
            optimize=True,
        )

        filename = os.path.splitext(
            os.path.basename(image_field.name)
        )[0] + ".webp"

        if os.path.exists(image_field.path):
            os.remove(image_field.path)

        image_field.save(
            filename,
            ContentFile(buffer.getvalue()),
            save=False,
        )

        return True

    except Exception:
        return False    



class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(
        upload_to="category_image/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "webp"]
            )
        ],
        blank=True,
        null=True,
    )
    one_line = models.CharField(max_length=50,blank=True)
    description = models.TextField(blank=True)
    use_cases = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

        # Only process if an image is actually present
        if self.image and hasattr(self.image, "path"):
            img = Image.open(self.image.path)

            # Convert to RGB if needed
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Resize (optional)
            img.thumbnail((1200, 1200))

            # Save to WebP in memory
            buffer = BytesIO()
            img.save(
                buffer,
                format="WEBP",
                quality=80,
                optimize=True,
            )

            # New filename
            filename = os.path.splitext(
                os.path.basename(self.image.name)
            )[0] + ".webp"

            # Replace the file with WebP version
            self.image.save(
                filename,
                ContentFile(buffer.getvalue()),
                save=False,
            )

            super().save(update_fields=["image"])

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)  
    name = models.CharField(max_length=100)  
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Business(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="businesses",
    )
    category = models.ManyToManyField(
        Category,
        related_name="Businesses"
    )
    sub_category = models.CharField(max_length=100, blank=True)
    state = models.ForeignKey("State",on_delete=models.CASCADE)
    city = ChainedForeignKey(
        City,
        chained_field="state",
        chained_model_field="state",
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE,
    )
    phone = models.CharField(
    max_length=20,
    blank=True,
    null=True
    )
    rating = models.DecimalField(
        max_digits=2, 
        decimal_places=1, 
        default=3.7
    )
    description = models.TextField(max_length=100, blank=True)
    address = models.TextField()
    google_map_image = models.URLField(blank=True, null=True)
    image = models.ImageField(
        upload_to="business/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "webp"]
            )
        ],
        blank=True,
        null=True,
    )
    project_image1 = models.ImageField(
    upload_to="business/projects/",
    blank=True,
    null=True,
    )
    project_caption1 = models.CharField(max_length=200, blank=True)
    project_location1 = models.CharField(max_length=200, blank=True)
    project_image2 = models.ImageField(
    upload_to="business/projects/",
    blank=True,
    null=True,
    )
    project_caption2 = models.CharField(max_length=200, blank=True)
    project_location2 = models.CharField(max_length=200, blank=True)
    project_image3 = models.ImageField(
    upload_to="business/projects/",
    blank=True,
    null=True,
    )
    project_caption3 = models.CharField(max_length=200, blank=True)
    project_location3 = models.CharField(max_length=200, blank=True)
    project_image4 = models.ImageField(
    upload_to="business/projects/",
    blank=True,
    null=True,
    )
    project_caption4 = models.CharField(max_length=200, blank=True)
    project_location4 = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False)
    STATUS = [
    ('V', 'Verified'),
    ('P', 'Pending'),
    ]
    status = models.CharField(
        max_length=2,
        choices=STATUS,
        default='P',
    )
    PROVIDES = [
    ('P', 'Pan indai'),
    ('R', 'Regional'),
    ]
    provides = models.CharField(
        max_length=2,
        choices=PROVIDES,
        default='R',
    )
    created_at = models.DateTimeField(default=timezone.now)
    def get_absolute_url(self):
        return reverse(
            "business_detail",
            kwargs={
                "city_slug": self.city.slug,
                "category_slug": self.category.slug,
                "business_slug": self.slug,
            },
        )
    def save(self, *args, **kwargs):
        if not self.slug:
         self.slug = slugify(self.name)

    # Pehle original files save hongi
        super().save(*args, **kwargs)

        updated_fields = []

        for field in [
        "image",
        "project_image1",
        "project_image2",
        "project_image3",
        "project_image4",
        ]:
         if convert_image_to_webp(self, field):
            updated_fields.append(field)

            if updated_fields:
                super().save(update_fields=updated_fields)
    
    def __str__(self):
         return self.name


  
class ServiceCityPage(models.Model):
    service = models.ForeignKey(Category, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    slug = models.SlugField(unique=True,blank=True)

    content = CKEditor5Field("Content", config_name="default")

    meta_title = models.CharField(max_length=200)
    meta_description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    def get_absolute_url(self):
      return reverse(
        "service_city",
        kwargs={
            "service_slug": self.service.slug,
            "city_slug": self.city.slug,
        },
    )
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.service.name}-in-{self.city.name}")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.service.name} in {self.city.name}"
    
class Blogcategory(models.Model):
    name = models.CharField(max_length =100)
    slug = models.SlugField(unique = True, blank =True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)    
    def __str__(self):
        return self.name  


class Blog(models.Model):
    # Core content
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = CKEditor5Field("Content", config_name="default")
    category = models.ForeignKey(
        "Blogcategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blogs"
    )

    # SEO fields
    meta_title = models.CharField(max_length=70, blank=True, help_text="SEO title (max 70 chars)")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO description (max 160 chars)")
    excerpt = models.TextField(blank=True)
    # Media
    image = models.ImageField(
        upload_to="blog_images/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "webp"]
            )
        ],
        blank=True,
        null=True,
    )

    # Author & timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    # Category relationship (optional, if you want blogs grouped)
    
    def get_absolute_url(self):
     return reverse(
        "blog_detail",
        kwargs={
            "blog_slug": self.slug,
        },
    )
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

        # Process image if uploaded
        if self.image and self.image.name:
            try:
                img = Image.open(self.image.path)

                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                img.thumbnail((1200, 1200))

                buffer = BytesIO()
                img.save(
                    buffer,
                    format="WEBP",
                    quality=80,
                    optimize=True,
                )

                filename = os.path.splitext(
                    os.path.basename(self.image.name)
                )[0] + ".webp"

                self.image.save(
                    filename,
                    ContentFile(buffer.getvalue()),
                    save=False,
                )

                super().save(update_fields=["image"])
            except Exception as e:
                print(f"Image processing skipped: {e}")

    def __str__(self):
        return self.title
    


class Lead(models.Model):
    
    customer_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    service_required = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer_name} - {self.service_required}"


class BlogView(models.Model):
    blog = models.ForeignKey(
        "Blog",
        on_delete=models.CASCADE,
        related_name="views"
    )
    ip_address = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("blog", "ip_address")

    def __str__(self):
        return f"{self.blog.title} - {self.ip_address}"
    

    