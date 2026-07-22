from django.urls import path
from .views import home, robots_txt,service_deatil,service_city_page, find_contractors,login_view,signup_view,load_cities,logout_view, about, why_fireseva,contractor_detail,blog_detail, blog, contact, all_service, submit_enquiry
urlpatterns = [
    path('', home, name='home'),
    path('find-contractors/', find_contractors, name='find_contractors'),
    path('about/', about, name='about'),
    path('why-fireseva/', why_fireseva, name='why_fireseva'),
    path('blog/', blog, name='blog'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('contact/', contact, name='contact'),
    path("robots.txt", robots_txt, name="robots_txt"),
    path('service/<slug:service_slug>/',service_deatil,name='service_deatil'),
    path('<slug:service_slug>-in-<slug:city_slug>/',service_city_page,name='service_city'),
    path('blog/<slug:blog_slug>/', blog_detail, name='blog_detail'),
    path('contractor/<slug:business_slug>/',contractor_detail, name='contractor_detail'),
    path('all-services/', all_service, name='all_service'),
    path('ajax/cities/', load_cities, name='load_cities'),
    path('submit-enquiry/', submit_enquiry, name='submit_enquiry'),
]