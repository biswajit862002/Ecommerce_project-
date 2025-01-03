from django.contrib import admin
from .models import Customer, Product, Cart, OrderPlaced, Payment, Wishlist
from django.utils.html import format_html
from django.urls import reverse

# Register your models here.

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'name', 'locality', 'city', 'mobile', 'zipcode', 'state'
    ]


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'product_image'
    ]


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'product_info', 'quantity' 
    ]

    def product_info(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'razorpay_order_id', 'razorpay_payment_status', 'razorpay_payment_id', 'paid']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'customer', 'customer_info', 'product_id', 'product_info', 'quantity', 'ordered_date', 'status', 'payment_info'
    ]

    def customer_info(self, obj):
        link = reverse("admin:app_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)
    
    def product_info(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)
    
    def payment_info(self, obj):
        link = reverse("admin:app_payment_change", args=[obj.payment.pk])
        return format_html('<a href="{}">{}</a>', link, obj.payment.razorpay_payment_id)
    

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product_info']

    def product_info(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)