from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.liste_especes, name='liste_especes'),
    path('espece/<int:id>/', views.detail_espece, name='detail_espece'),
    path('ajouter/', views.ajouter_espece, name='ajouter_espece'),
    path('modifier/<int:id>/', views.modifier_espece, name='modifier_espece'),
    path('supprimer/<int:id>/', views.supprimer_espece, name='supprimer_espece'),
    path('bassins/', views.liste_bassins, name='liste_bassins'),
    path('alertes/', views.alertes, name='alertes'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('home/', views.home, name='home'),
    path('ajouter_bassin/', views.ajouter_bassin, name='ajouter_bassin'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
