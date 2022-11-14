from django.db import models


class Shop(models.Model):
    title = models.CharField(max_length=50)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.title


class Supplies(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='supplies')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='supplies')
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product} in {self.shop}"


class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='sales')
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product} from {self.shop}"
