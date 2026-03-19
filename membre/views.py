from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
#from .forms import InscriptionMembreForm  # Assure-toi que forms.py existe aussi !

#def inscription(request):
#    if request.method == 'POST':
#        form = InscriptionMembreForm(request.POST)
#        if form.is_valid():
#            user = form.save()
#            login(request, user)
#            return redirect('accueil')
#    else:
#        form = InscriptionMembreForm()
#    return render(request, 'membre/inscription.html', {'form': form})