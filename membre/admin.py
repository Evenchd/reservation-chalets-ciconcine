from django.contrib import admin
from .models import Membre

@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ('nom_complet', 'numero_membre', 'email', 'cotisation_payee', 'bloque', 'date_inscription')
    list_filter = ('cotisation_payee', 'bloque')
    search_fields = ('nom_complet', 'numero_membre', 'email')
    ordering = ('-date_inscription',)
    actions = ['bloquer_membres', 'debloquer_membres', 'marquer_cotisation_payee']

    def bloquer_membres(self, request, queryset):
        queryset.update(bloque=True)
    bloquer_membres.short_description = "Bloquer les membres sélectionnés"

    def debloquer_membres(self, request, queryset):
        queryset.update(bloque=False)
    debloquer_membres.short_description = "Débloquer les membres sélectionnés"

    def marquer_cotisation_payee(self, request, queryset):
        queryset.update(cotisation_payee=True, frais_impayes=0)
    marquer_cotisation_payee.short_description = "Marquer cotisation payée pour les sélectionnés"