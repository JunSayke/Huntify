from django.contrib import admin
from .models import CustomUser
from booking_feature.admin import BoardingHouseInline, BookingInline

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'updated_at', 'account_type', 'is_active')
    readonly_fields = ('id', 'date_joined', 'updated_at')

    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj)
        if obj is not None:
            if obj.account_type == 'landlord':
                inline_instances.append(BoardingHouseInline(self.model, self.admin_site))
            elif obj.account_type == 'tenant':
                inline_instances.append(BookingInline(self.model, self.admin_site))
        return inline_instances

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
