from django.contrib import admin
from .models import Customer, Category, Item, ItemType, Shipper, Price, SellingInfo

# Register your models here.


@admin.register(Customer)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time_create', 'cat', 'is_published')
    list_display_links = ('id', 'name')
    ordering = ['time_create', 'name']
    list_editable = ['is_published']
    list_per_page = 10
    list_filter = ['cat__name', 'is_published']


# admin.site.register(Customer, MarketAdmin)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    ordering = ['name']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'item_type')
    list_display_links = ('id', 'name')


@admin.register(ItemType)
class ItemType(admin.ModelAdmin):
    list_display = ('id', 'typename',)
    list_display_links = ('id', 'typename')


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'shipper', 'value', )
    list_display_links = ('id', 'value')


@admin.register(Shipper)
class ShipperAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')


@admin.register(SellingInfo)
class SellingInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'quantity',)
    list_display_links = ('id', 'customer')


