from django.contrib import admin
from .models import Address, Order, OrderItem, OrderItemOption, PromoCode, OrderPromo

admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderItemOption)
admin.site.register(PromoCode)
admin.site.register(OrderPromo)