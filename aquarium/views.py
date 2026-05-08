from django.shortcuts import render, get_object_or_404, redirect
from .models import Espece, Bassin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group


def _get_especes_context(request):
    query = request.GET.get('q', '').strip()
    type_eau = request.GET.get('type_eau', '').strip()
    bassin_id = request.GET.get('bassin', '').strip()

    especes = Espece.objects.select_related('bassin').all()

    if query:
        especes = especes.filter(nom_commun__icontains=query)

    if type_eau:
        especes = especes.filter(bassin__type_eau=type_eau)

    if bassin_id:
        especes = especes.filter(bassin_id=bassin_id)

    return {
        'especes': especes,
        'bassins': Bassin.objects.all(),
        'query': query,
        'selected_type_eau': type_eau,
        'selected_bassin': bassin_id,
        'type_eau_choices': Bassin.TYPE_EAU,
    }




@login_required
def liste_especes(request):
    if not request.user.has_perm('aquarium.view_espece'):
        return redirect('home')

    return render(
        request,
        'aquarium/liste_especes.html',
        _get_especes_context(request)
    )


@login_required
def detail_espece(request, id):
    if not request.user.has_perm('aquarium.view_espece'):
        return redirect('home')

    espece = get_object_or_404(Espece, id=id)
    return render(request, 'aquarium/detail_espece.html', {'espece': espece})


@login_required
def ajouter_espece(request):
    if not request.user.has_perm('aquarium.add_espece'):
        return redirect('home')

    bassins = Bassin.objects.all()

    if request.method == "POST":
        nom = request.POST['nom']
        scientifique = request.POST['scientifique']
        famille = request.POST['famille']
        statut = request.POST['statut']
        bassin_id = request.POST['bassin']

        Espece.objects.create(
            nom_commun=nom,
            nom_scientifique=scientifique,
            famille=famille,
            statut=statut,
            bassin_id=bassin_id
        )

        return redirect('liste_especes')

    return render(request, 'aquarium/ajouter_espece.html', {'bassins': bassins})


@login_required
def modifier_espece(request, id):
    if not request.user.has_perm('aquarium.change_espece'):
        return redirect('home')

    espece = get_object_or_404(Espece, id=id)
    bassins = Bassin.objects.all()

    if request.method == "POST":
        espece.nom_commun = request.POST['nom']
        espece.nom_scientifique = request.POST['scientifique']
        espece.famille = request.POST['famille']
        espece.statut = request.POST['statut']
        espece.bassin_id = request.POST['bassin']
        espece.save()

        return redirect('liste_especes')

    return render(request, 'aquarium/modifier_espece.html', {
        'espece': espece,
        'bassins': bassins
    })


@login_required
def supprimer_espece(request, id):
    if not request.user.has_perm('aquarium.delete_espece'):
        return redirect('home')

    espece = get_object_or_404(Espece, id=id)
    espece.delete()
    return redirect('liste_especes')




@login_required
def liste_bassins(request):
    if not request.user.has_perm('aquarium.view_bassin'):
        return redirect('home')

    bassins = Bassin.objects.all()
    return render(request, 'aquarium/liste_bassins.html', {'bassins': bassins})

@login_required
def ajouter_bassin(request):
    if not request.user.has_perm('aquarium.add_bassin'):
        return redirect('home')

    if request.method == "POST":
        nom = request.POST.get('nom')
        volume = request.POST.get('volume')
        type_eau = request.POST.get('type_eau')
        temperature = request.POST.get('temperature')

        # 🔥 validation بسيطة
        if not volume:
            return render(request, 'aquarium/ajouter_bassin.html', {
                'error': "Volume obligatoire"
            })

        Bassin.objects.create(
            nom_bassin=nom,
            volume_litres=int(volume), 
            type_eau=type_eau,
            temperature_actuelle=float(temperature)
        )

        return redirect('liste_bassins')

    return render(request, 'aquarium/ajouter_bassin.html')


@login_required
def alertes(request):
    bassins = Bassin.objects.all()
    alertes = []

    for b in bassins:
        if b.temperature_actuelle > 30:
            alertes.append(f"⚠️ {b.nom_bassin} température trop élevée")

        if b.temperature_actuelle < 10:
            alertes.append(f"❄️ {b.nom_bassin} température trop basse")

    return render(request, 'aquarium/alertes.html', {
        'alertes': alertes
    })




def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'aquarium/login.html', {
                'error': 'Username ou password incorrect'
            })

    return render(request, 'aquarium/login.html')


def register_user(request):
    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

       
        if password != password_confirm:
            return render(request, 'aquarium/register.html', {
                'error': 'Les mots de passe ne correspondent pas'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'aquarium/register.html', {
                'error': 'Username déjà utilisé'
            })

      
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

       
        group = Group.objects.get(name='employes')
        user.groups.add(group)

       
        login(request, user)

        return redirect('home')

    return render(request, 'aquarium/register.html')

def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def home(request):
    return render(request, 'aquarium/home.html')
