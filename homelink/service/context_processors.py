from .models import Category

def categories_processor(request):
    categories = Category.objects.all()
    search = request.GET.get('search', '')
    return ({ 'categories': categories, 'search':search })