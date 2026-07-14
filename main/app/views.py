import json
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category, Lead, City, Business, Blog,Blog,BlogView,Blogcategory
from django.core.paginator import Paginator
import requests
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from .utils import send_telegram_message
from .decorators import heavy_ratelimit
from django.views.decorators.csrf import ensure_csrf_cookie
# Create your views here.


@ensure_csrf_cookie
@heavy_ratelimit(rate="5/m")
def login_view(request):
    if request.method == "POST":
        recaptcha_response = request.POST.get("g-recaptcha-response")
        if not recaptcha_response:
            messages.error(request, "Please complete the reCAPTCHA.")
            return render(
                request,
                "pages/login.html",
                {"RECAPTCHA_SITE_KEY": settings.RECAPTCHA_SITE_KEY},
            )
        google_response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": settings.RECAPTCHA_SECRET_KEY,
                "response": recaptcha_response,
            },
        ).json()

        if not google_response.get("success"):
            messages.error(request, "reCAPTCHA verification failed.")
            return render(
                request,
                "pages/login.html",
                {"RECAPTCHA_SITE_KEY": settings.RECAPTCHA_SITE_KEY},
            )
        email = request.POST.get("email").strip()
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "manage_business")
            return redirect(next_url)
        messages.error(request, "Invalid email or password.")
    return render(
        request,
        "pages/login.html",
        {
            "RECAPTCHA_SITE_KEY": settings.RECAPTCHA_SITE_KEY,
        },
    )


@ensure_csrf_cookie
@heavy_ratelimit(rate='3/m')
def signup_view(request):
    if request.method == 'POST':
        recaptcha_response = request.POST.get("g-recaptcha-response")
        if not recaptcha_response:
            messages.error(request, "Please complete the reCAPTCHA.")
            return render(
                request,
                "pages/signup.html",
                {"RECAPTCHA_SITE_KEY":settings.RECAPTCHA_SITE_KEY},

            )
        google_response = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": settings.RECAPTCHA_SECRET_KEY,
                "response": recaptcha_response,
            },
        ).json()
        if not google_response.get("success"):
             messages.error(request, "reCAPTCHA verification failed.")
             return render(
                 request,
                 "pages/signup.html",
                 {"RECAPTCHA_SITE_KEY": settings.RECAPTCHA_SITE_KEY},
             )

        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif not email:
            messages.error(request, 'Email is required.')
        else:
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, 'Enter a valid email address.')
                return render(request, 'pages/signup.html')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'An account with this email already exists.')
                return render(request, 'pages/signup.html')

            if len(password1) < 8:
                messages.error(request, 'Password must be at least 8 characters.')
                return render(request, 'pages/signup.html')

            if password1.isdigit():
                messages.error(request, 'Password cannot be entirely numeric.')
                return render(request, 'pages/signup.html')

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password1
            )
            login(request, user)
            return redirect('manage_business')

    return render(
        request,
        'pages/signup.html',
        {
            "RECAPTCHA_SITE_KEY": settings.RECAPTCHA_SITE_KEY,
        },
        )


@heavy_ratelimit(rate='30/m')
def logout_view(request):
    logout(request)
    return redirect('home')




def home(request):
    return render(request,"pages/home.html")

def find_contractors(request):
    city_slug = request.GET.get("city")
    service_slug = request.GET.get("rental_item")
    cities = City.objects.all()
    Categories = Category.objects.all()
    businesses = Business.objects.filter(city__slug=city_slug,category__slug=service_slug)
    paginator = Paginator(businesses, 6)
    page_number = request.GET.get("page")
    businesses = paginator.get_page(page_number)
        
    context = {
        'cities':cities,
        'city_slug':city_slug,
        'service_slug' : service_slug,
        'Categories' : Categories,
        'businesses':businesses,
    }

    
    return render(request, 'pages/find_contractor.html',context)

def contractor_detail(request, category_slug, business_slug,city_slug):
    business = get_object_or_404(
        Business.objects.select_related("category"),
        slug=business_slug,
        category__slug=category_slug,
        city__slug=city_slug,
    )
    similar_businesses = (
    Business.objects
    .filter(
        category__slug=category_slug
    )
    .exclude(slug=business_slug)
    .order_by('?')[:4]
    )
    return render(request, 'pages/contractor_detail.html',{ 'business':business,'similar_businesses':similar_businesses})



def about(request):
    return render(request,"pages/about.html")

def why_fireseva(request):
    return render(request,"pages/why_fireseva.html")

def blog(request):
    blogcategories = Blogcategory.objects.all()
    category_slug = request.GET.get("category")
    blogs = Blog.objects.all()
    if category_slug:
        blogs = blogs.filter(category__slug=category_slug)
    paginator = Paginator(blogs, 2)  
    featured_article = Blog.objects.all().order_by('-created_at').first() 
    page_number = request.GET.get("page")
    blogs = paginator.get_page(page_number)
    return render(request, 'pages/blog.html', {
        'blogcategories': blogcategories,
        'blogs': blogs,
        'active_category': category_slug,
        'featured_article':featured_article
    })


def contact(request):
    return render(request,"pages/contact.html")

def all_service(request):
    services = Category.objects.all()
    return render(request,"pages/all_service.html",{"services":services})

@csrf_exempt
def submit_enquiry(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "errors": {"__all__": "Invalid request method."}}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "errors": {"__all__": "Invalid JSON payload."}}, status=400)

    errors = {}

    name = data.get("name", "").strip()
    phone = data.get("phone", "").strip()
    service = data.get("service", "").strip()
    city = data.get("city", "").strip()
    message = data.get("message", "").strip()

    if not name:
        errors["name"] = "Name is required."
    if not phone:
        errors["phone"] = "Phone number is required."
    elif not phone.isdigit() or len(phone) < 10:
        errors["phone"] = "Enter a valid 10-digit phone number."
    if not service:
        errors["service"] = "Service is required."
    if not city:
        city = ""

    if errors:
        return JsonResponse({"success": False, "errors": errors}, status=400)

    lead = Lead.objects.create(
        customer_name=name,
        phone=phone,
        service_required=service,
        city=city,
        message=message,
    )
    try:
        send_telegram_message(
        f"""
🚨 New Lead Received

Name: {lead.customer_name}
Phone: {lead.phone}
Machine: {lead.service_required}
City: {lead.city}

Message:
{lead.message}
"""
    )

    except Exception as e:
        print("Telegram Error:", e)

    return JsonResponse({"success": True})
    
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def blog_detail(request, blog_slug):
    blog = get_object_or_404(Blog, slug = blog_slug)
    ip = get_client_ip(request)
    BlogView.objects.get_or_create(
        blog=blog,
        ip_address=ip
    )
    related = Blog.objects.none()
    if blog.category:
        related = (
        Blog.objects
        .filter(category=blog.category)
        .exclude(slug=blog_slug)
        .order_by('?')[:3]
        )
    return render(request, 'pages/blog_detail.html', {'blog': blog, 'related':related})
