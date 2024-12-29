# shop/admin.py
from django.contrib import admin
from .models import Category, Product, Payment  # Make sure to import Payment
from django.core.mail import send_mail

# Your existing admin configurations for Category and Product
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}

# Add the PaymentAdmin class
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_id', 'amount', 'is_verified', 'created_at')
    actions = ['verify_payments', 'reject_payments']

    def verify_payments(self, request, queryset):
        queryset.update(is_verified=True)
        for payment in queryset:
            send_mail(
                'Payment Verified',
                'Your payment has been verified.',
                'admin@cspace.com',
                [payment.user.email],
                fail_silently=False,
            )
    verify_payments.short_description = "Mark selected payments as verified"

    def reject_payments(self, request, queryset):
        for payment in queryset:
            send_mail(
                'Payment Not Verified',
                'Your payment could not be verified.',
                'admin@cspace.com',
                [payment.user.email],
                fail_silently=False,
            )
    reject_payments.short_description = "Mark selected payments as not verified"

admin.site.register(Payment, PaymentAdmin)