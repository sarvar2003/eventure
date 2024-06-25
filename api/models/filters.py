from django.db import models


class Category(models.Model):

    """Category model"""

    title = models.CharField(max_length=50)
    slug_title = models.SlugField()


class Topic(models.Model):
    
    """Topic model"""

    title = models.CharField(max_length=50)
    slug_title = models.SlugField()
    category = models.ForeignKey("api.Category", on_delete=models.CASCADE)
