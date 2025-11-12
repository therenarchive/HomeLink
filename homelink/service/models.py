from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    search_count = models.FloatField(default=0)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class Work(models.Model):
    is_featured = models.BooleanField(default=False)
    work_title = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to="profiles", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    category = models.ForeignKey(Category, related_name="work", on_delete=models.CASCADE)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    worker = models.ForeignKey(User, related_name="work", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.work_title
    
class Payment(models.Model):
    work = models.ForeignKey(Work, null=True, on_delete=models.CASCADE)
    amount = models.FloatField()
    reference = models.CharField(unique=True)
    status = models.CharField(default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


