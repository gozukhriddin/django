from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_quryset(self):
        return super().get_queryset().filter(status=Newa.Status.published)

class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Newa(models.Model):

    class Status(models.TextChoices):
        draft = 'DF', 'Draft'
        published = "PB", "Published"

    title=models.CharField(max_length=250)
    slug=models.SlugField(max_length=250)
    text=models.TextField()
    image=models.ImageField(upload_to='news/images')
    category=models.ForeignKey(Category,
                               on_delete=models.CASCADE)
    publish_time=models.DateTimeField(default=timezone.now)
    create_time=models.DateTimeField(auto_now_add=True)
    update_time=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=2,
                            choices=Status.choices,
                            default=Status.draft)

    object=models.Manager()
    pulished=PublishedManager ()



    class Meta:
        ordering = ["-publish_time"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("newdetail", args=[self.slug])



class ContactForm(models.Model):
    name=models.CharField(max_length=150)
    email=models.EmailField(max_length=150)
    message=models.TextField()

    def __str__(self):
        return self.email

# Create your models here.


class Comment(models.Model):
    new=models.ForeignKey(Newa,
                           on_delete=models.CASCADE,
                           related_name='comments')
    user=models.ForeignKey(User,
                           on_delete=models.CASCADE,
                           related_name='comments')
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    is_activ=models.BooleanField(default=False)

    class Meta:
        ordering=['-created']

    def __str__(self):
        return f"Commment {self.body} by {self.user}"