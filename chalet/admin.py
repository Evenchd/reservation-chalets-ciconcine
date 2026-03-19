from django.contrib import admin
from .models import Chalet

@admin.register(Chalet)
class ChaletAdmin(admin.ModelAdmin):
    list_display = ('nom', 'capacite_max', 'localisation', 'services_hiver')
    list_filter = ('services_hiver',)
    search_fields = ('nom', 'localisation')
    ordering = ('nom',)
    fields = ('nom', 'capacite_max', 'localisation', 'equipements', 'services_hiver', 'photo')  # Champs éditables