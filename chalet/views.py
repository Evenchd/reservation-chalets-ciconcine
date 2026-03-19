from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Chalet
from reservation.models import Reservation
from django.http import JsonResponse
from datetime import date, timedelta
import json

def accueil(request):
    return render(request, 'accueil.html', {'message': 'Bienvenue au Club Ciconcine !'})

@login_required
def liste_chalets(request):
    chalets = Chalet.objects.all()
    return render(request, 'chalet/liste.html', {'chalets': chalets})

@login_required
def calendrier_chalet(request, chalet_id):
    chalet = get_object_or_404(Chalet, id=chalet_id)
    return render(request, 'chalet/calendrier.html', {'chalet': chalet})

@login_required
def evenements_chalet(request, chalet_id):
    chalet = get_object_or_404(Chalet, id=chalet_id)
    reservations = Reservation.objects.filter(chalet=chalet)
    events = []
    for res in reservations:
        color = '#28a745' if res.statut == 'approuvee' else '#ffc107' if res.statut == 'en_attente' else '#dc3545'
        events.append({
            'title': f"Réservé par {res.membre.nom_complet}" if res.statut == 'approuvee' else f"En attente",
            'start': res.date_arrivee.isoformat(),
            'end': res.date_depart.isoformat(),  # Changé pour exclusive : jour de départ libre
            'color': color,
            'classNames': ['fc-event-occupé'] if res.statut == 'approuvee' else ['fc-event-attente'],
        })
    return JsonResponse(events, safe=False)