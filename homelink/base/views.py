from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from service.models import Category,Work

from .forms import SignUpForm

# Create your views here.
def home(request):
    works = Work.objects.all()
    categories = Category.objects.all()
    featured_workers = Work.objects.filter(is_featured=True)
    regular_workers = Work.objects.filter(is_featured=False)

    return render (request, 'base/home.html', {
        "works": works,
        "categories": categories,
        'featured_workers': featured_workers,
        'regular_workers': regular_workers,
    })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.profile.acc_type = form.cleaned_data['acc_type']
            user.profile.save()

            return redirect('/login/')
    else:
        form = SignUpForm()
    
    return render (request, 'base/signup.html', {
        "form":form,
    })

def login(request):
    return render (request, 'base/login.html')

def workers_json(request):
    workers = Work.objects.exclude(longitude__isnull=True).exclude(latitude__isnull=True)
    data = [{
        'title': w.work_title,
        'category': str(w.category),
        'lat': w.latitude,
        'lng': w.longitude,
        'detail_url': reverse('service:service_detail', args=[w.id])
    }
    for w in workers
    ]
    return JsonResponse(data, safe=False)

def nearby_map(request):
    return render (request, 'base/nearby_map.html')

def featured(request):
    works = Work.objects.all()
    featured_workers = Work.objects.filter(is_featured=True)

    return render (request, 'base/featured.html', {
        'works':works,
        'featured_workers':featured_workers
    })

def contact(request):
    return render (request, 'base/contact.html')