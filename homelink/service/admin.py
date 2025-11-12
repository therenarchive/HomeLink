from django.contrib import admin

from .models import Category,Work, Payment

admin.site.register(Category)
admin.site.register(Work)
admin.site.register(Payment)