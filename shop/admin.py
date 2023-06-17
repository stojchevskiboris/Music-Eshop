from django.contrib import admin
from .models import Instrument, Cart, Customer, Order

# Register your models here.


admin.site.register(Instrument)


class CartAdmin(admin.ModelAdmin):
    pass
    list_display = ("usersession", "instrument")


admin.site.register(Cart, CartAdmin)
admin.site.register(Customer)
admin.site.register(Order)
