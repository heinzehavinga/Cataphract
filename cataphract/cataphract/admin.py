from django.contrib import admin
from django.utils.html import format_html

from .models import *

admin.site.register(World)
admin.site.register(Region)
admin.site.register(Hex)

admin.site.register(Unittype)
admin.site.register(Strongholdtype)
admin.site.register(Faction)
admin.site.register(Commander)
admin.site.register(Strongholds)
admin.site.register(Army)
admin.site.register(Detachment)
admin.site.register(Order)
admin.site.register(Player)


@admin.register(Map)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'world', 'bio', 'height', 'width', 'image', 'image_thumbnail')
    readonly_fields = ('image_preview',)

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 200px;" />',
                obj.image.url
            )
        return "-"
    image_thumbnail.short_description = 'Thumbnail'

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 400px; max-width: 200px;" />',
                obj.image.url
            )
        return "-"
    image_preview.short_description = 'Preview'
