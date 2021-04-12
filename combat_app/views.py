from django.shortcuts import HttpResponse, redirect, render
from combat_app import models as combat_models
import random
import math
from django.contrib import messages


def home(request):
    context = {
        'version': 1.2
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


def generate_select(request, uid):
    other_fighters = combat_models.Fighter.objects.exclude(id=uid)
    return render(request, 'partial.html', {'other_fighters': other_fighters})


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
    round_advance = combat_models.ActiveFight.objects.round_result(
        request.POST, request)
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
