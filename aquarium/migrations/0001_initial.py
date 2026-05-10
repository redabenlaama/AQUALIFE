from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bassin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_bassin', models.CharField(max_length=100)),
                ('volume_litres', models.IntegerField()),
                ('type_eau', models.CharField(choices=[('douce', 'Douce'), ('saumatre', 'Saumâtre'), ('salee', 'Salée')], max_length=20)),
                ('temperature_actuelle', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Espece',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_commun', models.CharField(max_length=100)),
                ('nom_scientifique', models.CharField(max_length=100)),
                ('famille', models.CharField(max_length=100)),
                ('statut', models.CharField(max_length=100)),
                ('bassin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aquarium.bassin')),
            ],
        ),
        migrations.CreateModel(
            name='Alimentation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_nourriture', models.CharField(max_length=100)),
                ('frequence_journaliere', models.IntegerField()),
                ('espece', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aquarium.espece')),
            ],
        ),
    ]
