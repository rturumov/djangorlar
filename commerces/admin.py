from django.contrib import admin
from .models import Address, Order, OrderItem, OrderItemOption, PromoCode, OrderPromo

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "street", "building", "is_deleted", "deleted_at")
    list_filter = ("is_deleted", "city")
    search_fields = ("city", "street", "building")


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_percent", "is_deleted", "deleted_at")
    list_filter = ("is_deleted",)
    search_fields = ("code",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "restaurant", "status", "total", "is_deleted")
    list_filter = ("status", "is_deleted")
    search_fields = ("user__username", "restaurant__name")
    list_select_related = ("user", "restaurant", "address")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "item_name", "quantity", "item_price", "line_total", "is_deleted")
    list_filter = ("is_deleted",)
    search_fields = ("item_name",)


@admin.register(OrderItemOption)
class OrderItemOptionAdmin(admin.ModelAdmin):
    list_display = ("order_item", "option_name", "price_delta", "is_deleted")
    list_filter = ("is_deleted",)
    search_fields = ("option_name",)


@admin.register(OrderPromo)
class OrderPromoAdmin(admin.ModelAdmin):
    list_display = ("order", "promo_code", "applied_amount", "is_deleted")
    list_filter = ("is_deleted",)
