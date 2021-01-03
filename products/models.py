from django.db import models

from accounts.models import User


class Group(models.Model):
    name = models.CharField(max_length=20)


class Product(models.Model):
    name = models.CharField(max_length=20)
    image = models.FileField(upload_to='static/product_images')
    group = models.ForeignKey(Group, related_name='products', on_delete=models.CASCADE)
    price = models.FloatField()
    stock = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_image_path(self):
        return '/'.join(str(self.image).split('/')[1:])


class ProductsToBuyers(models.Model):
    quantity = models.IntegerField()
    buyers = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    products = models.ForeignKey(Product, related_name='buyers', on_delete=models.CASCADE)


class Tag(models.Model):
    content = models.CharField(max_length=20)
    products = models.ManyToManyField(Product, related_name='tags')

    def __str__(self):
        return self.content
