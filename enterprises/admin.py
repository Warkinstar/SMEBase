from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(BusinessType)
admin.site.register(OwnershipType)
admin.site.register(Employee)
admin.site.register(Financials)

