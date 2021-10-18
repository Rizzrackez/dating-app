from django.db import models


class CategoryLevel2(models.Model):
    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CategoryLevel1(models.Model):
    url = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    categories_child = models.ManyToManyField('CategoryLevel2', blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey('CategoryLevel2', blank=True, null=True, on_delete=models.CASCADE)
    price = models.FloatField()
    photo_url = models.CharField(max_length=255)

    def __str__(self):
        return self.title