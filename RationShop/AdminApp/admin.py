from django.contrib import admin
from AdminApp.models import Stock, RationItems

# Register your models here using decorators (CORRECT WAY):

@admin.register(Stock) # Use @admin.register decorator
class StockAdmin(admin.ModelAdmin): # You can create custom Admin classes if needed
    pass # Add configurations here if needed

@admin.register(RationItems) # Use @admin.register decorator
class RationItemsAdmin(admin.ModelAdmin): # You can create custom Admin classes if needed
    pass # Add configurations here if needed