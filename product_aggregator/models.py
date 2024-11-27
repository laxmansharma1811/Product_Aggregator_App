from django.db import models
from django.utils.timezone import now

class DarazProduct(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)  # FloatField for ratings
    color = models.CharField(max_length=50, null=True, blank=True)
    price_history = models.JSONField(default=list)

    def __str__(self):
        return self.name
    
class DarazPriceHistory(models.Model):
    product = models.ForeignKey(DarazProduct, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.product.name} - {self.price}'

class AmazonProduct(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(null=True, blank=True)
    reviews = models.CharField(max_length=50, null=True, blank=True)
    manufacturer = models.CharField(max_length=100, null=True, blank=True)
    asin = models.CharField(max_length=50, null=True, blank=True)
    price_history = models.JSONField(default=list)

    def __str__(self):
        return self.name
    

class AmazonPriceHistory(models.Model):
    product = models.ForeignKey(AmazonProduct, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=now)

    def __str__(self):
        return f'{self.product.name} - {self.price}'
