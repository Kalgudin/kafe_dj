from .models import CustomUser, Staff, Visitors

from django.contrib import admin


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    pass


@admin.register(Visitors)
class VisitorsAdmin(admin.ModelAdmin):
    pass
