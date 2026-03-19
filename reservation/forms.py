from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, timedelta
from .models import Reservation
from membre.models import Membre


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date_arrivee', 'date_depart', 'invites_payants', 'invites_famille']
        widgets = {
            'date_arrivee': forms.DateInput(attrs={'type': 'date'}),
            'date_depart': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'date_arrivee': 'Date d’arrivée',
            'date_depart': 'Date de départ',
            'invites_payants': 'Invités payants (25$/nuit)',
            'invites_famille': 'Invités famille (gratuits)',
        }

    def __init__(self, *args, **kwargs):
        self.chalet = kwargs.pop('chalet', None)
        self.membre = kwargs.pop('membre', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        date_arrivee = cleaned_data.get('date_arrivee')
        date_depart = cleaned_data.get('date_depart')
        invites_payants = cleaned_data.get('invites_payants') or 0
        invites_famille = cleaned_data.get('invites_famille') or 0

        # Champs obligatoires
        if not date_arrivee or not date_depart:
            raise ValidationError("Les dates d'arrivée et de départ sont obligatoires.")

        if not self.chalet or not self.membre:
            raise ValidationError("Erreur interne : chalet ou membre manquant.")

        # Droit de réservation
        if not self.membre.peut_reserver():
            raise ValidationError(
                "Vous ne pouvez pas réserver : cotisation non payée ou compte bloqué. "
                "Contactez l'administrateur."
            )

        today = date.today()

        # Validations dates de base
        if date_arrivee < today:
            raise ValidationError("La date d'arrivée ne peut pas être dans le passé.")

        if date_depart <= date_arrivee:
            raise ValidationError("La date de départ doit être après la date d'arrivée.")

        duree = (date_depart - date_arrivee).days
        if not (1 <= duree <= 7):
            raise ValidationError("La durée doit être de 1 à 7 nuits.")

        # ───────────────────────────────────────────────
        # RÈGLE STRICTE : UNE SEULE RÉSERVATION ACTIVE/FUTURE PAR MEMBRE
        # (peu importe le chalet)
        # ───────────────────────────────────────────────
        reservations_existantes = Reservation.objects.filter(
            membre=self.membre,
            statut__in=['en_attente', 'approuvee'],
            date_depart__gt=today,          # ignore les réservations déjà terminées
        )

        if reservations_existantes.exists():
            # On prend la première pour afficher des infos utiles dans le message
            res = reservations_existantes.first()
            raise ValidationError(
                f"Vous avez déjà une réservation en cours ou future "
                f"du {res.date_arrivee} au {res.date_depart} "
                f"(chalet {res.chalet}).\n\n"
                "Vous ne pouvez avoir **qu'une seule réservation à la fois**, "
                "peu importe le chalet.\n"
                f"Vous pourrez créer une nouvelle réservation à partir du {res.date_depart}."
            )

        # ───────────────────────────────────────────────
        # Vérification disponibilité DU CHALET CHOISI
        # ───────────────────────────────────────────────
        chevauchement_chalet = Reservation.objects.filter(
            chalet=self.chalet,
            statut__in=['en_attente', 'approuvee'],
            date_arrivee__lt=date_depart,
            date_depart__gt=date_arrivee,
        ).exclude(
            pk=self.instance.pk if self.instance and self.instance.pk else None
        ).exists()

        if chevauchement_chalet:
            raise ValidationError("Ces dates sont déjà réservées pour ce chalet.")

        # ───────────────────────────────────────────────
        # Capacité
        # ───────────────────────────────────────────────
        total_personnes = 1 + invites_payants + invites_famille
        if total_personnes > self.chalet.capacite_max:
            raise ValidationError(
                f"Capacité maximale dépassée : {total_personnes} personnes "
                f"(maximum {self.chalet.capacite_max} pour ce chalet)."
            )

        return cleaned_data
    