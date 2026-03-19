#from django import forms
#from django.contrib.auth.forms import UserCreationForm
#from .models import Membre
#from django.contrib.auth.models import User
#
#class InscriptionMembreForm(UserCreationForm):
#    nom_complet = forms.CharField(max_length=100, label="Nom complet")
#    numero_membre = forms.CharField(max_length=20, label="Numéro de membre")
#    email = forms.EmailField(label="Email")
#
#    class Meta:
#        model = User
#        fields = ('username', 'email', 'password1', 'password2')
#
#    def save(self, commit=True):
#        user = super().save(commit=False)
#        user.email = self.cleaned_data['email']
#        if commit:
#            user.save()
#            Membre.objects.create(
#                user=user,
#                nom_complet=self.cleaned_data['nom_complet'],
#                numero_membre=self.cleaned_data['numero_membre'],
#                email=user.email,
#                cotisation_payee=True  # Par défaut pour tests
#            )
#        return user