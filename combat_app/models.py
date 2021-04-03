from django.db import models
from django.db.models.functions import Ceil


class FightManager (models.Manager):

    def get_queryset(self):
        return super(FightManager, self).get_queryset().defer(None)

    def round_count(self):
        error = {}
        if ActiveFight.fight_round > 40:
            error['round_limit'] = "Fight is over"
            return error

    def round_result(self, post_data):
        this_fight = combat_models.ActiveFight.objects.get(id=1)
        health = combat_models.FighterHealth.objects.all()
        action = combat_models.FightAction.objects.get(id=1)
        # manually assigned here but will be attribute-based depending on technique
        defender = action.defender
        attacker = action.attacker
        attacker_val = 22
        defender_val = 11
        # roll determines if attacker or defender wins round
        roll = random.randint(1, attacker_val+defender_val)
        damage = 20
        recovery = 5
        defender_health = health.get(fighter=defender)
        if roll <= attacker_val:
            defender_health.health = max(
                defender_health.health - damage, 0)
            defender_health.save()
        else:
            defender_health.health = min(
                defender_health.health + recovery, 100)
            defender_health.save()
            this_fight.fight_round = this_fight.fight_round + 1
            this_fight.save()


class Fighter(models.Model):
    fighter_type = models.CharField(max_length=20)
    power = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    speed = models.IntegerField()
    agility = models.IntegerField()
    recovery = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FightManager()

    def __str__(self):
        return self.fighter_type


class FighterHealth(models.Model):
    fighter = models.IntegerField(default=1)
    health = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FightManager()


class Attack(models.Model):
    attack_type = models.CharField(max_length=10)
    power_mod = models.DecimalField(max_digits=3, decimal_places=2)
    speed_mod = models.DecimalField(max_digits=3, decimal_places=2)
    attack_mod = models.DecimalField(max_digits=3, decimal_places=2)
    damage_mod = models.DecimalField(max_digits=3, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FightManager()

# this model will feed the roll for first attack


class FirstAttack(models.Model):
    speed_mod = models.DecimalField(max_digits=3, decimal_places=2)
    attack_mod = models.DecimalField(max_digits=3, decimal_places=2)
    agility_mod = models.DecimalField(max_digits=3, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FightManager()


class Defense(models.Model):
    defense_type = models.CharField(max_length=10)
    speed_mod = models.DecimalField(max_digits=3, decimal_places=2)
    agility_mod = models.DecimalField(max_digits=3, decimal_places=2)
    defense_mod = models.DecimalField(max_digits=3, decimal_places=2)
    recovery_mod = models.DecimalField(max_digits=3, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FightManager()


class Base(models.Model):
    base_recovery = models.IntegerField()
    base_miss = models.DecimalField(max_digits=3, decimal_places=2)
    base_damage = models.IntegerField()
    base_parry = models.DecimalField(max_digits=3, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FightManager()


class ActiveFight(models.Model):
    fighter1 = models.OneToOneField(
        Fighter, related_name="fighter1", null=True, blank=False, on_delete=models.CASCADE)
    fighter2 = models.OneToOneField(
        Fighter, related_name="fighter2", null=True, blank=False, on_delete=models.CASCADE)
    fight_round = models.IntegerField(default=1)
    fight_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FightManager()


class FightAction(models.Model):
    attacker = models.IntegerField(default=1)
    defender = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FightManager()
