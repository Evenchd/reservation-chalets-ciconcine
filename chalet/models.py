from django.db import models

class Chalet(models.Model):
    nom = models.CharField(max_length=100)
    capacite_max = models.PositiveIntegerField()  # Ex: 4 personnes
    localisation = models.CharField(max_length=200)
    equipements = models.TextField()  # Liste séparée par virgules, ex: "BBQ, kayak, wifi"
    services_hiver = models.BooleanField(default=False)  # Services limités en hiver
    photo = models.ImageField(upload_to='chalets/', blank=True, null=True)  # Utilise Pillow pour images

    def __str__(self):
        return self.nom