from django.contrib import admin
from WebApp.models import CartDB, BeneficiaryRegister, ShopOwner, OrderStatus, OrderDB

# Register your models here using decorators (CORRECT WAY):

@admin.register(CartDB)  # Use @admin.register decorator
class CartDBAdmin(admin.ModelAdmin):
    list_filter = ('order',) # You can create custom Admin classes if needed, or just leave it as simple @admin.register(CartDB)
    pass # You can add configurations here if needed, like list_display, etc.

@admin.register(BeneficiaryRegister) # Use @admin.register decorator
class BeneficiaryRegisterAdmin(admin.ModelAdmin):
    pass

@admin.register(ShopOwner) # Use @admin.register decorator
class ShopOwnerAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderDB) # Use @admin.register decorator
class OrderDBAdmin(admin.ModelAdmin):
    pass

@admin.register(OrderStatus) # Use @admin.register decorator
class OrderStatusAdmin(admin.ModelAdmin):
    pass