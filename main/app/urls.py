from django.urls import path
from .views import home, find_contractors, about, why_fireseva,contractor_detail,blog_detail, blog, contact, all_service, submit_enquiry
urlpatterns = [
    path('', home, name='home'),
    path('find-contractors/', find_contractors, name='find_contractors'),
    path('about/', about, name='about'),
    path('why-fireseva/', why_fireseva, name='why_fireseva'),
    path('blog/', blog, name='blog'),
    path('contact/', contact, name='contact'),
     path('blog/<slug:blog_slug>/', blog_detail, name='blog_detail'),
    path('contractor/<slug:city_slug>/<slug:category_slug>/<slug:business_slug>/',contractor_detail, name='contractor_detail'),
    path('all-services/', all_service, name='all_service'),
    path('submit-enquiry/', submit_enquiry, name='submit_enquiry'),
]