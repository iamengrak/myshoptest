from django.contrib import admin
from .models import Payment
from django.core.mail import send_mail

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_id', 'amount', 'is_verified', 'created_at')
    actions = ['verify_payments', 'reject_payments']

    def verify_payments(self, request, queryset):
        queryset.update(is_verified=True)
        for payment in queryset:
            send_mail(
                'Payment Verified',
                'Your payment has been verified.',
                'admin@example.com',
                [payment.user.email],
                fail_silently=False,
            )
    verify_payments.short_description = "Mark selected payments as verified"

    def reject_payments(self, request, queryset):
        for payment in queryset:
            send_mail(
                'Payment Not Verified',
                'Your payment could not be verified.',
                'admin@example.com',
                [payment.user.email],
                fail_silently=False,
            )
    reject_payments.short_description = "Mark selected payments as not verified"

admin.site.register(Payment, PaymentAdmin)