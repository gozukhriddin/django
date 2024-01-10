from django.db import models
from django.contrib.auth.models import User
from django.db import models
# Create your models here.

class ProfileUser(models.Model):
    user=models.OneToOneField(User,
                              on_delete=models.CASCADE)
    photo=models.ImageField(upload_to='user', blank=True, null=True)
    date_brith =models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} profili"
