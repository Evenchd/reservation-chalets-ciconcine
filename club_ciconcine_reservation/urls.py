"""
URL configuration for club_ciconcine_reservation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
#from membre.views import inscription
from chalet.views import accueil, liste_chalets, calendrier_chalet, evenements_chalet
from reservation.views import reservations_membre, creer_reservation, annuler_reservation # Ajout de creer_reservation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', accueil, name='accueil'),
    # path('inscription/', inscription, name='inscription'),  # Commenté pour club privé
    path('login/', auth_views.LoginView.as_view(template_name='membre/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('chalets/', liste_chalets, name='liste_chalets'),
    path('chalets/<int:chalet_id>/calendrier/', calendrier_chalet, name='calendrier_chalet'),
    path('evenements_chalet/<int:chalet_id>/', evenements_chalet, name='evenements_chalet'),
    path('mes-reservations/', reservations_membre, name='reservations_membre'),
    path('chalets/<int:chalet_id>/reserver/', creer_reservation, name='creer_reservation'),  # Ajouté pour permettre aux membres de réserver
    path('reservations/<int:reservation_id>/annuler/', annuler_reservation, name='annuler_reservation'),
]

# Pour médias (si pas déjà)
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)