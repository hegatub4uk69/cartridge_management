from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Staff, Department, Cartridge, CartridgesHistory, Printers, CartridgesPrinter, CartridgeModel


class StaffInline(admin.StackedInline):
    model = Staff
    can_delete = False
    verbose_name_plural = 'Staff'

class UserAdmin(BaseUserAdmin):
    inlines = [StaffInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Department)
class DepartmentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id',)
    search_fields = ('id', 'name')
    list_editable = ('name',)
    list_filter = ('name',)

@admin.register(CartridgeModel)
class CartridgeModelsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id',)
    search_fields = ('id', 'name')
    list_editable = ('name',)
    list_filter = ('name',)

@admin.register(Cartridge)
class CartridgesAdmin(admin.ModelAdmin):
    list_display = ('id', 'model', 'department', 'description', 'date_of_last_location', 'date_added')
    list_display_links = ('id',)
    search_fields = ('id', 'model', 'department', 'description')
    list_editable = ('model', 'department', 'description', 'date_of_last_location')
    list_filter = ('model', 'department', 'date_added', 'date_of_last_location')

@admin.register(CartridgesHistory)
class CartridgesHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'cartridge', 'user', 'department', 'created_at')
    list_display_links = ('id',)
    search_fields = ('id', 'cartridge', 'user', 'department', 'created_at')
    list_editable = ('cartridge', 'user', 'department')
    list_filter = ('cartridge', 'user', 'department', 'created_at')

@admin.register(Printers)
class PrintersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type')
    list_display_links = ('id',)
    search_fields = ('id', 'name', 'type')
    list_editable = ('name', 'type')
    list_filter = ('name', 'type')

@admin.register(CartridgesPrinter)
class CartridgesPrintersAdmin(admin.ModelAdmin):
    list_display = ('id', 'cartridge_model', 'printer')
    list_display_links = ('id',)
    search_fields = ('id', 'cartridge_model', 'printer')
    list_editable = ('cartridge_model', 'printer')
    list_filter = ('cartridge_model', 'printer')