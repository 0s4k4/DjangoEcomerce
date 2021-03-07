from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from .models import (
    Item,
    Order,
    OrderItem
)

# Create your views here.

#se añade la function de home
def home(request) :
    return render(request, 'home.html', {'name' : 'andika'})

#Usamos el modelo Item como modelo de inicio y home.html como vista de plantilla. home.html se puede encontrar en el directorio de plantillas

class HomeView(ListView):
    model = Item
    template_name="home.html"
#Usamos el modelo Item como modelo de inicio y product.html como vista de plantilla. product.html se puede encontrar en el directorio de plantillas
class ProductView(DateDetailView):
    model = Item
    template_name="product.html"
#Usamos el modelo Item como modelo de inicio y product.html como vista de plantilla. product.html se puede encontrar en el directorio de plantillas
@login_required
def add_to_cart(request, pk) :
    item = get_object_or_404(Item, pk = pk )
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user = request.user,
        ordered = False
    )
    order_qs = Order.objects.filter(user=request.user, ordered= False)

    if order_qs.exists() :
        order = order_qs[0]
        
        if order.items.filter(item__pk = item.pk).exists() :
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Cantidad agregada al producto")
            return redirect("core:order-summary", pk = pk)
        else:
            order.items.add(order_item)
            messages.info(request, "Cantidad agregada al prodcuto")
            return redirect("core:order-summary", pk = pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request, "item agregado a tu carrito")
        return redirect("core:order-summary", pk = pk)
#Esta función agregará su producto a la base de datos de OrderItem y agregará un pedido detallado a la base de datos de pedidos
@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk )
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.delete()
            messages.info(request, "Item \""+order_item.item.item_name+"\" remover de tu carrito")
            return redirect("core:order-summary")
        else:
            messages.info(request, "este producto no esta en tu carrito")
            return redirect("core:order-summary", pk=pk)
    else:
        #add message doesnt have order
        messages.info(request, "tu no tienes una orden")
        return redirect("core:order-summary", pk = pk)


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object' : order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "No existe una orden")
            return redirect("/")
@login_required
def reduce_quantity_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs =  Order.objects.filter(
        user = request.user,
        ordered = False
    )
    if order_qs.exist():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exist():
            order_item = OrderItem.objects.filter(
                item = item,
                user = request.user,
                ordered = False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, "cantidad de producto a sido actualizo")
            return redirect("core:order-summary")
        else:
            messages.info(request, "este producto esta en tu carrito")
            return redirect("core:order-summary")
    else:
        #añadir mensaje cuando no exista orden
        messages.info(request, "tu no tienes esta orden")
        return redirect("core:order-summary")