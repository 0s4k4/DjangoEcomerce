  
from django.conf import settings
from django.db import models
from django.shortcuts import reverse

CATEGORY = (
    ('C', 'Camisa'),
    ('RD', 'Ropa Deportiva'),
    ('O', 'Otro')
)

LABEL = (
    ('N', 'New'),
    ('BS', 'Best Seller')
)

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY, max_length=2)
    label = models.CharField(choices=LABEL, max_length=2)
    description = models.TextField()

    def __str__(self):
        return self.item_name
#devolverá la URL del producto
    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            "pk" : self.pk
        
        })
#Devolveré la URL a la función agregar artículo al carrito en el archivo views.py que haremos
    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            "pk" : self.pk
        })
#devolverá la URL a la función eliminar el artículo del carrito en el archivo views.py que haremos
    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            "pk" : self.pk
        })
#OrderItem almacena datos del producto que desea pedir y la cantidad del producto
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.item_name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

 
#El modelo order almacenará información detallada de los pedidos realizados, pero en esta parte del tutorial no mostraremos la información completa del pedido, agregaremos otro campo en la siguiente parte

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

