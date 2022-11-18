# Register your models here.
from phantom_mask.AdminSite import admin_site
from pharmacy.admin.CustomerAdmin import CustomerAdmin
from pharmacy.admin.MaskAdmin import MaskAdmin
from pharmacy.admin.PharmacyAdmin import PharmacyAdmin
from pharmacy.models import Mask, Pharmacy, Customer

admin_site.register(Mask, MaskAdmin)
admin_site.register(Pharmacy, PharmacyAdmin)
admin_site.register(Customer, CustomerAdmin)
