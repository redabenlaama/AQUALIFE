from django.contrib import admin
from .models import Bassin, Espece, Alimentation

admin.site.register(Bassin)
admin.site.register(Espece)
admin.site.register(Alimentation)