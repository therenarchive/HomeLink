from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ACC_TYPE = (
        ('worker','Worker'),
        ('homeowner', 'Homeowner'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    acc_type = models.CharField(choices=ACC_TYPE)

    def __str__(self):
        return f" { self.user.username } - { self.acc_type }"
