from django.contrib import admin
from django.utils.html import format_html
from .models import Chalet

@admin.register(Chalet)
class ChaletAdmin(admin.ModelAdmin):
    list_display = (
        'thumbnail',
        'nom',
        'capacite_max',
        'localisation',
        'services_hiver',
    )
    list_filter = ('services_hiver',)
    search_fields = ('nom', 'localisation')
    ordering = ('nom',)

    fields = (
        'nom',
        'photo',
        'thumbnail',
        'capacite_max',
        'localisation',
        'equipements',
        'services_hiver',
    )
    readonly_fields = ('thumbnail',)

    def thumbnail(self, obj):
        if obj.pk and obj.photo:
            return format_html(
                '<img src="{url}" style="height: 60px; width: auto; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.2);">',
                url=obj.photo.url
            )
        return '<span style="color: #999; font-style: italic;">Pas de photo</span>'

    thumbnail.short_description = 'Photo'
    thumbnail.admin_order_field = 'photo'