from django.contrib import admin
from combat_app import models as combat_models

# Register your models here.

admin.site.register(combat_models.Fighter)
admin.site.register(combat_models.Attack)
admin.site.register(combat_models.FirstAttack)
admin.site.register(combat_models.Defense)
admin.site.register(combat_models.Base)
admin.site.register(combat_models.ActiveFight)
admin.site.register(combat_models.FightAction)
admin.site.register(combat_models.FighterHealth)
