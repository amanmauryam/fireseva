from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from app.models import Business, Category, State, City
from app.decorators import heavy_ratelimit


@login_required(login_url="login")
@heavy_ratelimit(rate='60/m')
def manage_business(request):
    businesses_list = Business.objects.filter(user=request.user).order_by("-created_at")
    paginator = Paginator(businesses_list, 10)
    page = request.GET.get("page")
    businesses = paginator.get_page(page)
    return render(
        request,
        "dashboard/manage_business.html",
        {"businesses": businesses, "active_page": "businesses"},
    )


@login_required(login_url="login")
@heavy_ratelimit(rate='10/m')
def manage_business_add(request):
    if request.method == "POST":
        name = request.POST.get("name")
        category_id = request.POST.get("category")
        state_id = request.POST.get("state")
        city_id = request.POST.get("city")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        if name and category_id and state_id and city_id:
            business = Business.objects.create(
                name=name,
                user=request.user,
                category_id=category_id,
                state_id=state_id,
                city_id=city_id,
                phone=phone,
                address=address or "",
            )
            if request.FILES.get("image"):
                business.image = request.FILES["image"]
                business.save()
            messages.success(request, "Business added successfully!")
            return redirect("manage_business")
        messages.error(request, "Please fill in all required fields.")
    categories = Category.objects.all()
    states = State.objects.all()
    return render(
        request,
        "dashboard/manage_business_form.html",
        {"categories": categories, "states": states, "active_page": "businesses"},
    )

@heavy_ratelimit(rate='20/m')
@login_required(login_url="login")
def manage_business_edit(request, pk):
    business = get_object_or_404(Business, pk=pk, user=request.user)
    if request.method == "POST":
        business.name = request.POST.get("name", business.name)
        business.phone = request.POST.get("phone", business.phone)
        business.address = request.POST.get("address", business.address)
        if request.POST.get("category"):
            business.categories_id = request.POST.get("category")
        if request.POST.get("state"):
            business.state_id = request.POST.get("state")
        if request.POST.get("city"):
            business.city_id = request.POST.get("city")
        if request.FILES.get("image"):
            business.image = request.FILES["image"]
        business.save()
        messages.success(request, "Business updated successfully!")
        return redirect("manage_business")
    categories = Category.objects.all()
    states = State.objects.all()
    return render(
        request,
        "dashboard/manage_business_form.html",
        {"business": business, "categories": categories, "states": states, "editing": True, "active_page": "businesses"},
    )


@login_required(login_url="login")
@heavy_ratelimit(rate='5/m')
def manage_business_delete(request, pk):
    business = get_object_or_404(Business, pk=pk, user=request.user)
    if request.method == "POST":
        business.delete()
        messages.success(request, "Business deleted successfully!")
    return redirect("manage_business")

