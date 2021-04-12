from django.shortcuts import HttpResponse, redirect, render
from combat_app import models as combat_models
import random
import math
from django.contrib import messages


def home(request):
    context = {
        'version': 1.4
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
    start_fight = combat_models.ActiveFight.objects.start_fight(
        request.POST)
    return redirect("/fight")


def fight(request):
    this_fight = combat_models.ActiveFight.objects.get(id=1)
    health = combat_models.FighterHealth.objects.all()
    fighter = combat_models.Fighter.objects.all()
    if this_fight.fight_active == True:
        print('************fight round', this_fight.fight_round)
        if this_fight.fight_round > 40:
            return redirect('/result')
        else:
            # uses weighted roll to choose first attacker based on attributes
            f1_speed = this_fight.fighter1.speed
            f1_attack = this_fight.fighter1.attack
            f1_agility = this_fight.fighter1.agility
            f2_speed = this_fight.fighter2.speed
            f2_attack = this_fight.fighter2.attack
            f2_agility = this_fight.fighter2.agility
            speed_mod = combat_models.FirstAttack.objects.get(id=1).speed_mod
            attack_mod = combat_models.FirstAttack.objects.get(id=1).attack_mod
            agility_mod = combat_models.FirstAttack.objects.get(
                id=1).agility_mod
            fighter1_first_att_val = math.ceil(f1_speed * speed_mod +
                                               f1_attack * attack_mod + f1_agility * agility_mod)
            fighter2_first_att_val = math.ceil(f2_speed * speed_mod +
                                               f2_attack * attack_mod + f2_agility * agility_mod)
            first_attack_roll = random.randint(
                1, fighter1_first_att_val+fighter2_first_att_val)
            print("*****fighter 1 first attack value>>>", fighter1_first_att_val)
            print("*****fighter 2 first attack value>>>", fighter2_first_att_val)
            print("*****first attack roll>>>", first_attack_roll)

            if this_fight.fight_round % 2 == 1:  # new logic will go in this line
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
