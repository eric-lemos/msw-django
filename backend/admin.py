from .models import Config, Devices, Log, Mics, Models, GroupExtend
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.contrib import admin

class ConfigList(admin.ModelAdmin):
    # Class responsable for the 'config' Table configuration on Django admin
    list_display = ('name', 'value', 'description')
    list_editable = ('value',)
    list_display_links = None
    search_fields = ('name',)
    list_per_page = 20

class DevicesList(admin.ModelAdmin):
    # Class responsable for the 'devices' Table configuration on Django admin
    list_display = ('id', 'alias', 'host', 'port', 'model')
    list_editable = ('alias', 'host', 'port')  
    search_fields = ('alias', 'host')
    list_display_links = ('id',)
    list_per_page = 20

class GroupExtendInline(admin.StackedInline):
    verbose_name_plural = 'groups'
    filter_horizontal = ('mics',)
    model = GroupExtend
    can_delete = False

class GroupAdmin(BaseGroupAdmin):
    inlines = (GroupExtendInline,)

class LogList(admin.ModelAdmin):
    # Class responsable for the 'log' Table configuration on Django admin
    list_display = ('id', 'type', 'system', 'subsystem', 'user', 'description','date_time',)
    list_filter = ('type','subsystem','system','date_time')
    search_fields = ('user', 'system','subsystem','type')
    list_display_links = ('id',)
    list_per_page = 20

class MicsList(admin.ModelAdmin):
    # Class responsable for the 'mics' Table configuration on Django admin
    list_display = ('id', 'device', 'name', 'alias', 'detail')
    search_fields = ('name', 'host')
    list_display_links = ('id',)
    list_editable = ('name',)
    list_filter = ('detail',)
    list_per_page = 20

class ModelsList(admin.ModelAdmin):
    # Class responsable for the 'models' Table configuration on Django admin
    list_display = ('id', 'model', 'manufacturer', 'max_rf', 'min_rf', 'max_aud', 'min_aud', 'max_gain', 'min_gain')
    list_editable = ('max_rf', 'min_rf', 'max_aud', 'min_aud', 'max_gain', 'min_gain')
    search_fields = ('model', 'manufacturer')
    list_filter = ('manufacturer',)
    list_display_links = ('id',)
    list_per_page = 20

admin.site.unregister(Group)
admin.site.register(Devices, DevicesList)
admin.site.register(Config, ConfigList)
admin.site.register(Models, ModelsList)
admin.site.register(Group, GroupAdmin)
admin.site.register(Mics, MicsList)
admin.site.register(Log, LogList)