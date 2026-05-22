from django.contrib import admin
from .models import Supplier, Customer, SupplierPayment, CustomerPayment


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'company_name', 'initial_debt', 'is_active', 'created_by', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'phone_number', 'company_name', 'inn')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'company_name', 'initial_debt', 'credit_limit', 'discount_percent', 'is_active', 'created_by', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'phone_number', 'company_name', 'inn')


@admin.register(SupplierPayment)
class SupplierPaymentAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'date', 'amount', 'payment_type', 'reference_number', 'created_by', 'created_at')
    list_filter = ('payment_type', 'supplier')
    search_fields = ('supplier__name', 'reference_number')


@admin.register(CustomerPayment)
class CustomerPaymentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date', 'amount', 'payment_type', 'reference_number', 'created_by', 'created_at')
    list_filter = ('payment_type', 'customer')
    search_fields = ('customer__name', 'reference_number')
