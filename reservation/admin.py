from django.contrib import admin
from .models import Reservation
from django.core.mail import send_mail
from django.conf import settings

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('numero_reservation', 'membre', 'chalet', 'date_arrivee', 'date_depart', 'statut', 'date_creation')
    list_filter = ('statut', 'chalet', 'membre')
    search_fields = ('membre__nom_complet', 'chalet__nom', 'numero_reservation')
    ordering = ('-date_creation',)
    actions = ['approuver_reservations', 'annuler_reservations']

    def approuver_reservations(self, request, queryset):
        queryset.update(statut='approuvee')
        for res in queryset:
            send_mail(
                subject='Réservation approuvée - Club Ciconcine',
                message=f'Bonjour {res.membre.nom_complet},\n\nVotre réservation n° {res.numero_reservation} pour le chalet {res.chalet.nom} du {res.date_arrivee} au {res.date_depart} a été approuvée !\n\nBon séjour,\nClub Ciconcine',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[res.membre.email],
                fail_silently=False,
        )
        self.message_user(request, "Réservations approuvées et emails envoyés.")
    approuver_reservations.short_description = "Approuver les réservations sélectionnées"

    def annuler_reservations(self, request, queryset):
        queryset.update(statut='annulee')
        # TODO: Ajouter envoi d'email d'annulation ici plus tard
    annuler_reservations.short_description = "Annuler les réservations sélectionnées"