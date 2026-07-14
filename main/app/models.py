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
    category = models.ForeignKey("Category",on_delete=models.CASCADE)
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
    is_featured = models.BooleanField(default=False)
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

        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            # RGB conversion
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Resize (optional)
            img.thumbnail((1200, 1200))

            # WebP memory buffer
            buffer = BytesIO()
            img.save(
                buffer,
                format="WEBP",
                quality=80,
                optimize=True,
            )

            # New filename
            filename = os.path.splitext(os.path.basename(self.image.name))[0] + ".webp"

            # Delete old file
            if os.path.exists(self.image.path):
                os.remove(self.image.path)

            # Save webp image
            self.image.save(
                filename,
                ContentFile(buffer.getvalue()),
                save=False,
            )

            super().save(update_fields=["image"])
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
    

    