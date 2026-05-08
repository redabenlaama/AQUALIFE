
from django.db import models

class Bassin(models.Model):
    TYPE_EAU = [
        ('douce', 'Douce'),
        ('saumatre', 'Saumâtre'),
        ('salee', 'Salée'),
    ]

    nom_bassin = models.CharField(max_length=100)
    volume_litres = models.IntegerField()
    type_eau = models.CharField(max_length=20, choices=TYPE_EAU)
    temperature_actuelle = models.FloatField()

    def __str__(self):
        return self.nom_bassin


class Espece(models.Model):
    nom_commun = models.CharField(max_length=100)
    nom_scientifique = models.CharField(max_length=100)
    famille = models.CharField(max_length=100)
    bassin = models.ForeignKey(Bassin, on_delete=models.CASCADE)
    statut = models.CharField(max_length=100)

    def __str__(self):
        return self.nom_commun


class Alimentation(models.Model):
    espece = models.ForeignKey(Espece, on_delete=models.CASCADE)
    type_nourriture = models.CharField(max_length=100)
    frequence_journaliere = models.IntegerField()
    

