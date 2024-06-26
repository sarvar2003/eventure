from django.db import models


class Category(models.Model):

    """Category model"""

    title = models.CharField(max_length=50)
    slug_title = models.SlugField()

    def __str__(self) -> str:
        return str(self.title)


class Topic(models.Model):
    
    """Topic model"""

    title = models.CharField(max_length=50)
    slug_title = models.SlugField()
    category = models.ForeignKey("api.Category", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.title)