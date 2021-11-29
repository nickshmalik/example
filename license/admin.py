from django.contrib import admin
from .models import Customer, License



class CustomerAdmin(admin.ModelAdmin):
    list_display = ('company', 'firstname', 'lastname', 'email',)
    list_display_links = ('company',)
    ordering = ('-id',)

class LicenseAdmin(admin.ModelAdmin):
    list_display = ('customer', 'license', 'red', 'green', 'date', 'grey',)
    list_display_links = ('customer',)
    list_filter = ('customer', 'date',)
    ordering = ('-id',)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(License, LicenseAdmin)