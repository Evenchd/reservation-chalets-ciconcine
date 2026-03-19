from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReservationForm  # Assure-toi que forms.py existe avec ReservationForm
from .models import Reservation
from membre.models import Membre
from chalet.models import Chalet
from django.core.mail import send_mail
from django.conf import settings
from datetime import date, timedelta

@login_required
def reservations_membre(request):
    membre = get_object_or_404(Membre, user=request.user)
    reservations = Reservation.objects.filter(membre=membre)
    return render(request, 'reservation/liste_membre.html', {'reservations': reservations})

@login_required
def creer_reservation(request, chalet_id):
    chalet = get_object_or_404(Chalet, id=chalet_id)
    membre = get_object_or_404(Membre, user=request.user)

    if request.method == 'POST':
        form = ReservationForm(request.POST, chalet=chalet, membre=membre)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.membre = membre
            reservation.chalet = chalet
            reservation.statut = 'en_attente'  # Pour approbation admin
            reservation.save()
            messages.success(request, 'Réservation soumise ! En attente d\'approbation.')
            send_mail(
                subject='Confirmation de réservation soumise - Club Ciconcine',
                message=f'Bonjour {reservation.membre.nom_complet},\n\nVotre réservation n° {reservation.numero_reservation} pour le chalet {reservation.chalet.nom} du {reservation.date_arrivee} au {reservation.date_depart} a été soumise et est en attente d\'approbation.\n\nMerci,\nClub Ciconcine',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[reservation.membre.email],
                fail_silently=False,  # Pour voir les erreurs dans la console si problème
            )
            
            return redirect('reservations_membre')
    else:
        form = ReservationForm(chalet=chalet, membre=membre)

    return render(request, 'reservation/creer.html', {'form': form, 'chalet': chalet})

@login_required  # Ajouté : Décorateur manquant pour protéger la vue
def annuler_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, membre__user=request.user, statut__in=['en_attente', 'approuvee'])
    if (reservation.date_arrivee - date.today()) >= timedelta(days=7):
        reservation.statut = 'annulee'
        reservation.save()
        messages.success(request, 'Réservation annulée avec succès.')
        # Option : Envoyer email d'annulation
        send_mail(
            subject='Annulation de réservation - Club Ciconcine',
            message=f'Bonjour {reservation.membre.nom_complet},\n\nVotre réservation n° {reservation.numero_reservation} a été annulée.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[reservation.membre.email],
            fail_silently=False,
        )
    else:
        messages.error(request, 'Annulation possible seulement 7 jours à l\'avance.')
    return redirect('reservations_membre')