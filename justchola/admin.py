from django.contrib import admin
from . models import Destination, Product, Contact, Orders, OrderUpdate

# Register your models here.

admin.site.register(Destination)
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)