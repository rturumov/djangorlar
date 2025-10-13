from django.contrib import admin
from .models import Restaurant, MenuItem, Category, Option, ItemCategory, ItemOption


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "is_deleted", "deleted_at")
    list_filter = ("is_deleted",)
    search_fields = ("name",)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant", "available", "is_deleted")
    list_filter = ("available", "is_deleted")
    search_fields = ("name", "restaurant__name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_deleted", "deleted_at")
    list_filter = ("is_deleted",)
    search_fields = ("name",)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("name", "is_deleted", "deleted_at")
    list_filter = ("is_deleted",)
    search_fields = ("name",)


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ("item", "category", "position", "is_deleted")
    list_filter = ("is_deleted",)
    search_fields = ("item__name", "category__name")


@admin.register(ItemOption)
class ItemOptionAdmin(admin.ModelAdmin):
    list_display = ("item", "option", "price_delta", "is_default", "is_deleted")
    list_filter = ("is_default", "is_deleted")
    search_fields = ("item__name", "option__name")