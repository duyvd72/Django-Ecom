from django.db import models
from accounts.models import Account
from store.models import Item, Variation


class Cart(models.Model):
    cart_id = models.CharField(max_length=255, blank=True)
    date_add = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.item.public_price * self.quantity

    def __unicode__(self):
        return self.item