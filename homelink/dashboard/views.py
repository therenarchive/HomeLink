from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from service.models import Work, Payment

@login_required
def dashboard(request):
    works = Work.objects.filter(worker=request.user)
    services = Work.objects.all()

    monthly_revenue = (
        Payment.objects.filter(status__iexact='success')
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total_revenue=Sum('amount'))
        .order_by('month')
    )

    return render (request, 'dashboard/dashboard.html', {
        'works': works,
        'services':services,
        'monthly_revenue': monthly_revenue,
    })
