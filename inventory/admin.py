from django.contrib import admin
from .models import Warehouse, Category, Product, Incoming, IncomingItem, Outgoing, OutgoingItem


class IncomingItemInline(admin.TabularInline):
    model = IncomingItem
    extra = 0


class OutgoingItemInline(admin.TabularInline):
    model = OutgoingItem
    extra = 0


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'created_by', 'created_at')
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'warehouse', 'category', 'quantity', 'minimum_quantity', 'created_by', 'created_at')
    list_filter = ('warehouse', 'category')
    search_fields = ('name', 'barcode')


@admin.register(Incoming)
class IncomingAdmin(admin.ModelAdmin):
    list_display = ('id', 'warehouse', 'supplier', 'date', 'total_amount', 'paid_amount', 'debt', 'created_by')
    list_filter = ('warehouse', 'supplier')
    search_fields = ('invoice_number',)
    inlines = [IncomingItemInline]


@admin.register(Outgoing)
class OutgoingAdmin(admin.ModelAdmin):
    list_display = ('id', 'warehouse', 'customer', 'date', 'total_amount', 'paid_amount', 'debt', 'profit', 'created_by')
    list_filter = ('warehouse', 'customer')
    search_fields = ('invoice_number',)
    inlines = [OutgoingItemInline]
