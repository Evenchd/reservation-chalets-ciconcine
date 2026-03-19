from django.db import models
from membre.models import Membre
from chalet.models import Chalet
import uuid  # Pour numéro réservation unique
import random  # Ajouté pour générer les chiffres aléatoires dans save()

class Reservation(models.Model):
    STATUTS = (
        ('en_attente', 'En attente d\'approbation'),
        ('approuvee', 'Approuvée'),
        ('annulee', 'Annulée'),
    )

    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    chalet = models.ForeignKey(Chalet, on_delete=models.CASCADE)
    date_arrivee = models.DateField()
    date_depart = models.DateField()  # Max 7 jours
    invites_payants = models.PositiveIntegerField(default=0)  # 25$/nuit
    invites_famille = models.PositiveIntegerField(default=0)  # Gratuits
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')
    numero_reservation = models.CharField(max_length=50, unique=True, editable=False)  # Changé de UUID à CharField pour custom string
    date_creation = models.DateTimeField(auto_now_add=True)
    approuve_par = models.ForeignKey(Membre, on_delete=models.SET_NULL, null=True, blank=True, related_name='approbations')
    notes = models.TextField(blank=True)  # Ex: exceptions

    def save(self, *args, **kwargs):
        if not self.numero_reservation:
            # Génère format : YYYY-MM-DD-numero_membre-XXXX (4 chiffres aléatoires)
            date_str = self.date_arrivee.strftime('%Y-%m-%d')
            membre_num = self.membre.numero_membre
            random_num = str(random.randint(1000, 9999))  # 4 chiffres aléatoires
            self.numero_reservation = f"{date_str}-{membre_num}-{random_num}"

            # Vérifie unicité (rare collision, mais au cas)
            while Reservation.objects.filter(numero_reservation=self.numero_reservation).exists():
                random_num = str(random.randint(1000, 9999))
                self.numero_reservation = f"{date_str}-{membre_num}-{random_num}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Réservation {self.numero_reservation} pour {self.membre}"

    def duree(self):
        return (self.date_depart - self.date_arrivee).days

    class Meta:
        ordering = ['-date_creation']  # Pour logbook récent en premier
        