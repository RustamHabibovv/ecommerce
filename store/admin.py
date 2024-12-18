from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'seller')  # Customize columns
    search_fields = ('name', 'category')  # Add search functionality
    list_filter = ('category',)  # Add filtering options

def save_model(self, request, obj, form, change):
    if not obj.seller:  # If no seller is set, assign the current user
        obj.seller = 'Rustamadmin'
    super().save_model(request, obj, form, change)
