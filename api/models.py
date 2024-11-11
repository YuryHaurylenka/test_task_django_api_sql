from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Link(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="links")
    url = models.URLField(max_length=255)
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=50, default="website")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or self.url


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collections")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    links = models.ManyToManyField("Link", related_name="collections")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
