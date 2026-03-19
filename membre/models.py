from django.db import models
from django.contrib.auth.models import User

class Membre(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Lien avec l'utilisateur Django pour auth
    numero_membre = models.CharField(max_length=20, unique=True)  # Numéro unique
    nom_complet = models.CharField(max_length=100)
    email = models.EmailField()
    cotisation_payee = models.BooleanField(default=False)  # True si cotisation annuelle payée
    frais_impayes = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Montant impayé
    bloque = models.BooleanField(default=False)  # Admin peut bloquer
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom_complet} ({self.numero_membre})"

    def peut_reserver(self):
        return self.cotisation_payee and self.frais_impayes == 0 and not self.bloque


