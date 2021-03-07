  
from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField

CATEGORY = (
    ('C', 'Camisa'),
    ('RD', 'Ropa Deportiva'),
    ('O', 'Otro')
)

LABEL = (
    ('N', 'Nuevo'),
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
#devuelve el valor del precio total de cada artículo del producto
    def get_total_item_price(self):
        return self.quantity * self.item.price
#devuelve el valor del precio total de cada artículo de producto basado en precios con descuento
    def get_discount_item_price(self):
        return self.quantity * self.item.discount_price
#devuelve el valor del precio ahorrado de los descuentos existentes
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_discount_item_price()
#devuelve qué función se utiliza como determinante de precio (ya sea utilizando el precio original o el precio con descuento)
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_discount_item_price()
        return self.get_total_item_price()


 
#El modelo order almacenará información detallada de los pedidos realizados, pero en esta parte del tutorial no mostraremos la información completa del pedido, agregaremos otro campo en la siguiente parte

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

#devuelve el valor del precio total de todos los artículos de producto pedidos
    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

class CheckoutAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
