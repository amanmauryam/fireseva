from django.urls import path
from django.views.generic.base import RedirectView
from dashboard.views import (
    manage_business,
    manage_business_add,
    manage_business_edit,
    manage_business_delete,
   
)

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="manage_business", permanent=False), name="dashboard_home"),
    path("businesses/", manage_business, name="manage_business"),
    path("businesses/add/", manage_business_add, name="manage_business_add"),
    path("businesses/<int:pk>/edit/", manage_business_edit, name="manage_business_edit"),
    path("businesses/<int:pk>/delete/", manage_business_delete, name="manage_business_delete"),
]
