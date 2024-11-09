from django.contrib import admin

from features.address.models import Province, Municipality, Barangay

# Register your models here.
admin.site.register(Province)
admin.site.register(Municipality)
admin.site.register(Barangay)