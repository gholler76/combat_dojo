from django.db import models
import math
import random
from django.contrib import messages
from django.urls import reverse
from django.http import HttpRequest
import decimal


class FightManager (models.Manager):

    def get_absolute_url(self):
        return reverse('fight_advance', args=[str(self.id)])

    def start_fight(self, post_data, request):
        # reset ActiveFight for new fight after fighter select
        messages.info(request, "Prepare for Combat!!!")
        this_fight = ActiveFight.objects.get(id=1)
        health = FighterHealth.objects.all()
        this_fight.fighter1 = Fighter.objects.get(
            id=post_data['fighter1'])
        this_fight.fighter2 = Fighter.objects.get(
            id=post_data['fighter2'])
        this_fight.fight_round = 1
        this_fight.fight_active = True
        this_fight.save()
        health_fighter1 = health.get(id=1)
        health_fighter1.fighter = post_data['fighter1']
        health_fighter1.health = 100
        health_fighter1.save()
        health_fighter2 = health.get(id=2)
        health_fighter2.fighter = post_data['fighter2']
        health_fighter2.health = 100
        health_fighter2.save()
        # uses weighted roll to choose first attacker based on attributes
        f1_speed = this_fight.fighter1.speed
        f1_attack = this_fight.fighter1.attack
        f1_agility = this_fight.fighter1.agility
        f2_speed = this_fight.fighter2.speed
        f2_attack = this_fight.fighter2.attack
        f2_agility = this_fight.fighter2.agility
        speed_mod = FirstAttack.objects.get(id=1).speed_mod
        attack_mod = FirstAttack.objects.get(id=1).attack_mod
        agility_mod = FirstAttack.objects.get(
            id=1).agility_mod
        fighter1_first_att_val = math.ceil(f1_speed * speed_mod +
                                           f1_attack * attack_mod + f1_agility * agility_mod)
        fighter2_first_att_val = math.ceil(f2_speed * speed_mod +
                                           f2_attack * attack_mod + f2_agility * agility_mod)
        first_attack_roll = random.randint(
            1, fighter1_first_att_val+fighter2_first_att_val)
        if first_attack_roll <= fighter1_first_att_val:
            assign_action = FightAction.objects.get(id=1)
            assign_action.attacker = this_fight.fighter1_id
            assign_action.defender = this_fight.fighter2_id
            assign_action.save()
        else:
            assign_action = FightAction.objects.get(id=1)
            assign_action.attacker = this_fight.fighter2_id
            assign_action.defender = this_fight.fighter1_id
            assign_action.save()

        return request

    def round_result(self, post_data, request):
        # set round data
        this_fight = ActiveFight.objects.get(id=1)
        health = FighterHealth.objects.all()
        fighter = Fighter.objects.all()
        action = FightAction.objects.get(id=1)
        defender = action.defender
        attacker = action.attacker
        player = post_data["player"]
        tech = post_data["technique"]
        quick = "quick"
        Normal = "Normal"
        dodge = "dodge"
        Block = "Block"

        # set technique value selected by player, assign random selection to CPU
        this_attacker = Fighter.objects.all().get(id=attacker)
        # call base volues and mods
        power = this_attacker.power
        a_speed = this_attacker.speed
        attack = this_attacker.attack
        this_defender = Fighter.objects.all().get(id=defender)
        d_speed = this_defender.speed
        agility = this_defender.agility
        defense = this_defender.defense
        this_defender = Fighter.objects.all().get(id=defender)
        qa_power = TechniqueMod.objects.get(id=1).qa_power
        na_power = TechniqueMod.objects.get(id=1).na_power
        sa_power = TechniqueMod.objects.get(id=1).sa_power
        qa_speed = TechniqueMod.objects.get(id=1).qa_speed
        na_speed = TechniqueMod.objects.get(id=1).na_speed
        sa_speed = TechniqueMod.objects.get(id=1).sa_speed
        qa_attack = TechniqueMod.objects.get(id=1).qa_attack
        na_attack = TechniqueMod.objects.get(id=1).na_attack
        sa_attack = TechniqueMod.objects.get(id=1).sa_attack
        dd_speed = TechniqueMod.objects.get(id=1).dd_speed
        nd_speed = TechniqueMod.objects.get(id=1).nd_speed
        cd_speed = TechniqueMod.objects.get(id=1).cd_speed
        dd_agility = TechniqueMod.objects.get(id=1).dd_agility
        nd_agility = TechniqueMod.objects.get(id=1).nd_agility
        cd_agility = TechniqueMod.objects.get(id=1).cd_agility
        dd_defense = TechniqueMod.objects.get(id=1).dd_defense
        nd_defense = TechniqueMod.objects.get(id=1).nd_defense
        cd_defense = TechniqueMod.objects.get(id=1).cd_defense
        # assign attack or defense to player, vice versa for CPU
        if player == "attack":
            attack_tech = tech
            defense_tech = Defense.objects.get(
                id=random.randint(1, 3)).defense_type
            if attack_tech == quick:
                this_attack = math.ceil(
                    power * qa_power +
                    a_speed * qa_speed
                    + attack * qa_attack)
            elif attack_tech == Normal:
                this_attack = math.ceil(
                    power * na_power +
                    a_speed * na_speed +
                    attack * na_attack)
            else:
                this_attack = math.ceil(
                    power * sa_power +
                    a_speed * sa_speed +
                    attack * sa_attack)
            if defense_tech == dodge:
                this_defense = math.ceil(
                    d_speed * dd_speed +
                    agility * dd_agility +
                    defense * dd_defense)
            elif defense_tech == Block:
                this_defense = math.ceil(
                    d_speed * nd_speed +
                    agility * nd_agility +
                    defense * nd_defense)
            else:
                this_defense = math.ceil(
                    d_speed * cd_speed +
                    agility * cd_agility +
                    defense * cd_defense)
        # switch player to defense if not attack
        else:
            defense_tech = tech
            attack_tech = Attack.objects.get(
                id=random.randint(1, 3)).attack_type
            if defense_tech == dodge:
                this_defense = math.ceil(
                    d_speed * dd_speed +
                    agility * dd_agility +
                    defense * dd_defense)
            elif defense_tech == Block:
                this_defense = math.ceil(
                    d_speed * nd_speed +
                    agility * nd_agility +
                    defense * nd_defense)
            else:
                this_defense = math.ceil(
                    d_speed * cd_speed +
                    agility * cd_agility +
                    defense * cd_defense)
            if attack_tech == quick:
                this_attack = math.ceil(
                    power * qa_power +
                    a_speed * qa_speed +
                    attack * qa_attack)
            elif attack_tech == Normal:
                this_attack = math.ceil(
                    power * na_power +
                    a_speed * na_speed +
                    attack * na_attack)
            else:
                this_attack = math.ceil(
                    power * sa_power +
                    a_speed * sa_speed +
                    attack * sa_attack)
        # after round values for att/def are established, dice roll to see who wins
        attacker_val = this_attack
        defender_val = this_defense
        roll = random.randint(1, attacker_val+defender_val)
        # load base combat values
        base_recovery = Base.objects.get(id=1).base_recovery
        base_miss = Base.objects.get(id=1).base_miss
        base_damage = Base.objects.get(id=1).base_damage
        base_parry = Base.objects.get(id=1).base_parry
        # load techniques used in the round
        damage_mod = Attack.objects.get(
            attack_type=str(attack_tech)).damage_mod
        recovery_mod = Defense.objects.get(
            defense_type=str(defense_tech)).recovery_mod
        # apply modifiers to base damage and recovery values based on who won the roll
        r_max = 20
        defender_recovery = this_defender.recovery
        damage = math.ceil(
            base_damage*(damage_mod * decimal.Decimal("{:.2f}".format(power/r_max))))
        recovery = math.ceil(
            base_recovery * (recovery_mod * decimal.Decimal("{:.2f}".format(defender_recovery/r_max))))
        defender_health = health.get(fighter=defender)
        if roll <= attacker_val:
            defender_health.health = max(
                defender_health.health - damage, 0)
            defender_health.save()
            messages.info(request, "Attack was successful!")
        else:
            defender_health.health = min(
                defender_health.health + recovery, 100)
            defender_health.save()
            messages.info(request, "Defense was successful!")
        # advance round by 1
        this_fight.fight_round = this_fight.fight_round + 1
        this_fight.save()
        # flip attacker and defendee for next round
        new_attacker = action.defender
        new_defender = action.attacker
        action.attacker = new_attacker
        action.save()
        action.defender = new_defender
        action.save()
        return request

# game models


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
    # fighter1 and fighter2 link from ActiveFight model
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
    created_at = models.DateTimeField(auto_now_add=True)
    base_parry = models.DecimalField(max_digits=3, decimal_places=2)
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


class TechniqueMod (models.Model):
    qa_power = models.DecimalField(max_digits=2, decimal_places=2)
    qa_speed = models.DecimalField(max_digits=2, decimal_places=2)
    qa_attack = models.DecimalField(max_digits=2, decimal_places=2)
    na_power = models.DecimalField(max_digits=2, decimal_places=2)
    na_speed = models.DecimalField(max_digits=2, decimal_places=2)
    na_attack = models.DecimalField(max_digits=2, decimal_places=2)
    sa_power = models.DecimalField(max_digits=2, decimal_places=2)
    sa_speed = models.DecimalField(max_digits=2, decimal_places=2)
    sa_attack = models.DecimalField(max_digits=2, decimal_places=2)
    dd_speed = models.DecimalField(max_digits=2, decimal_places=2)
    dd_agility = models.DecimalField(max_digits=2, decimal_places=2)
    dd_defense = models.DecimalField(max_digits=2, decimal_places=2)
    nd_speed = models.DecimalField(max_digits=2, decimal_places=2)
    nd_agility = models.DecimalField(max_digits=2, decimal_places=2)
    nd_defense = models.DecimalField(max_digits=2, decimal_places=2)
    cd_speed = models.DecimalField(max_digits=2, decimal_places=2)
    cd_agility = models.DecimalField(max_digits=2, decimal_places=2)
    cd_defense = models.DecimalField(max_digits=2, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = FightManager()

    def __unicode__(self):
        return self.qa_power
        return self.qa_speed
        return self.qa_attack
        return self.na_power
        return self.na_speed
        return self.na_attack
        return self.sa_power
        return self.sa_speed
        return self.sa_attack
        return self.dd_speed
        return self.dd_agility
        return self.dd_defense
        return self.nd_speed
        return self.nd_agility
        return self.nd_defense
        return self.cd_speed
        return self.cd_agility
        return self.cd_defense
