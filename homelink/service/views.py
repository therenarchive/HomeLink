import requests, uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.conf import settings
from service.models import Work, Category, Payment
from .forms import NewWorkForm, EditWork

from django.db.models import Q

def search_query(request):
    search = request.GET.get('search', '')
    category_id = request.GET.get('category', '')
    categories = Category.objects.all()
    works = Work.objects.all()
    featured_workers = Work.objects.filter(is_featured=True)
    regular_workers = Work.objects.filter(is_featured=False)
    
    if search:
        works = works.filter(Q(work_title__icontains=search) | Q(description__icontains=search))

        try:
            category= Category.objects.get(name__icontains=search)
            category.search_count +=1
            category.save()
        except Category.DoesNotExist:
            pass

    if category_id:
        works = works.filter(category_id=category_id)
        try:
            category = Category.objects.get(id=category_id)
            category.search_count +=1
            category.save()
        except Category.DoesNotExist:
            pass

    return render (request, 'base/home.html', {
        'works':works,
        'categories':categories,
        'featured_workers': featured_workers,
        'regular_workers': regular_workers,
        'search':search,
        'category_id': int(category_id) if category_id else None,
    })

def service_detail(request, pk):
    work = get_object_or_404(Work, pk=pk)
    return render(request, 'service/service_detail.html', {
        'work': work
        })


@login_required
def new_work(request):
    if request.method == 'POST':
        form = NewWorkForm(request.POST, request.FILES)

        if form.is_valid():
           work = form.save(commit=False)
           work.worker = request.user
           work.save()
           return redirect ('service:service_detail', pk=work.id)
    else:
        form = NewWorkForm()

    return render (request, 'service/listing_form.html', {
        'form': form
    })

@login_required
def edit(request, pk):
    work = get_object_or_404(Work, pk=pk, worker=request.user)

    if request.method == 'POST':
        form = EditWork(request.POST, request.FILES, instance=work)

        if form.is_valid:
            form.save()
            return redirect ('service:service_detail', pk=work.id)
    else:
        form = EditWork(instance=work)

    return render (request, 'service/listing_form.html', {
        'form': form,
        'title': 'Edit work',
    })

@login_required
def delete(request, pk):
    work = get_object_or_404(Work, pk=pk, worker=request.user)
    work.delete()

    return redirect ('dashboard:dashboard')

@login_required
def initiate_payment(request, pk):
    work = get_object_or_404(Work, pk=pk)
    amount = 200
    reference = str(uuid.uuid4())

    payment = Payment(work=work, amount=amount, reference=reference)

    data = {
        'amount': str(amount),
        'email': work.worker.email,
        'tx_ref': reference,
        'callback_url': settings.CHAPA_CALLBACK_URL,
        'return_url': f'http://127.0.0.1:8000/service/payment/success/{work.id}/',
        "customization[title]": "Featured",
        "customization[description]": "Get featured on the home page for 30 days",
    }

    headers = {
        'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}',
    }

    try:
        response = requests.post('http://api.chapa.co/v1/transaction/initialize', headers=headers, data=data)
        res = response.json()
        print("CHAPA RESPONSE:", res)
    except Exception as e:
        print("CHAPA ERROR:", e)
        return redirect('/')

    if res.get('status') == 'success':
        payment.save()  
        return redirect(res['data']['checkout_url'])
    else:
       
        print("CHAPA INIT FAILED:", res)
        return redirect('/')
    
def verify_payment(request):
    tx_ref = request.GET.get('trx_ref')

    if not tx_ref:
        messages.error(request, "No transaction reference provided.")
        return redirect('/')

    url = f"http://api.chapa.co/v1/transaction/verify/{tx_ref}"
    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
    }

    response = requests.get(url, headers=headers)
    res = response.json()
    print("VERIFY RESPONSE:", res)

    if res.get('status') == 'success' and res['data']['status'] == 'success':
        payment = Payment.objects.filter(reference=tx_ref).first()
        if payment:
            payment.work.is_featured = True
            payment.work.save()
            payment.status = 'success'
            payment.save()

        messages.success(request, "You are now featured for 30 days!")
        return redirect('service:service_detail', pk=payment.work.pk)

    messages.error(request, "Payment verification failed.")
    return redirect('dashboard:dashboard')

def payment_success(request, pk):
    messages.success(request, "Payment completed successfully!")
    
    return redirect('service:service_detail', pk=pk)
