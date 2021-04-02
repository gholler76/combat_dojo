from django.shortcuts import HttpResponse, redirect, render
from combat_app import models as combat_models
import random
import math


def home(request):
    context = {
        'version': 1.0
    }
    return render(request, "home.html", context)


def info(request):

    return render(request, "info.html")


def select(request):
    fighters = combat_models.Fighter.objects.all()
    context = {
        'fighters': fighters,
    }
    return render(request, "select.html", context)


def fight_start(request):
    # reset ActiveFight for new fight
    this_fight = combat_models.ActiveFight.objects.get(id=1)
    health = combat_models.FighterHealth.objects.all()
    this_fight.fighter1 = combat_models.Fighter.objects.get(
        id=request.POST['fighter1'])
    this_fight.fighter2 = combat_models.Fighter.objects.get(
        id=request.POST['fighter2'])
    this_fight.fight_round = 1
    this_fight.fight_active = True
    this_fight.save()
    health_fighter1 = health.get(id=1)
    health_fighter1.fighter = request.POST['fighter1']
    health_fighter1.health = 100
    health_fighter1.save()
    health_fighter2 = health.get(id=2)
    health_fighter2.fighter = request.POST['fighter2']
    health_fighter2.health = 100
    health_fighter2.save()

    return redirect("/fight")


def fight(request):
    this_fight = combat_models.ActiveFight.objects.get(id=1)
    health = combat_models.FighterHealth.objects.all()
    if this_fight.fight_active == True:
        print('************fight round', this_fight.fight_round)
        if this_fight.fight_round > 40:
            return redirect('/result')
        # assigns attacker to fighter2 in even rounds
        # current base model - will update to attribute-weighted roll
        else:
            if this_fight.fight_round % 2 == 1:
                assign_action = combat_models.FightAction.objects.get(id=1)
                assign_action.attacker = this_fight.fighter1_id
                assign_action.defender = this_fight.fighter2_id
                assign_action.save()
            else:
                assign_action = combat_models.FightAction.objects.get(id=1)
                assign_action.attacker = this_fight.fighter2_id
                assign_action.defender = this_fight.fighter1_id
                assign_action.save()
        print('**********attacker', assign_action.attacker)
        print('**********defender', assign_action.defender)
        # context used to provide fighter role each round and update health
        if health.get(id=1).health == 0 or health.get(id=2).health == 0:
            return redirect('/result')
        context = {
            'fight': this_fight,
            'attacker': assign_action.attacker,
            'defender': assign_action.defender,
            'health_fighter1': health.get(id=1),
            'health_fighter2': health.get(id=2)
        }
        return render(request, 'fight.html', context)
    else:
        return redirect('/result')


def fight_advance(request):
    this_fight = combat_models.ActiveFight.objects.get(id=1)
    health = combat_models.FighterHealth.objects.all()
    action = combat_models.FightAction.objects.get(id=1)
    print('***********defender', action.defender)
    # manually assigned here but will be attribute-based depending on technique
    defender = action.defender
    attacker = action.attacker
    attacker_val = 22
    defender_val = 11
    # roll determines if attacker or defender wins round
    roll = random.randint(1, attacker_val+defender_val)
    print('**************roll', roll)
    damage = 20
    recovery = 5
    defender_health = health.get(fighter=defender)
    if roll <= attacker_val:
        defender_health.health = max(defender_health.health - damage, 0)
        defender_health.save()
    else:
        defender_health.health = min(defender_health.health + recovery, 100)
        defender_health.save()
    this_fight.fight_round = this_fight.fight_round + 1
    this_fight.save()
    return redirect('/fight')


def result(request):
    this_fight = combat_models.ActiveFight.objects.get(id=1)
    fighter1 = combat_models.FighterHealth.objects.get(id=1)
    fighter2 = combat_models.FighterHealth.objects.get(id=2)
    fighter = combat_models.Fighter.objects.all()
    winner = {}
    if fighter1.health > fighter2.health:
        winner = fighter1
    elif fighter2.health > fighter1.health:
        winner = fighter2
    else:
        draw = "This fight ended in a draw!"
    print('************winner', winner.fighter)
    context = {
        'winner': winner.fighter,
        # 'draw': draw,
        # 'name': fighter.fighter_type.get(id=winner)
    }
    return render(request, "result.html", context)
