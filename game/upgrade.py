from building import Building
from resource import Cost, Affect
from math import *
from random import random,choice,choices
class upgrade:
    def __init__(self,targets,effect):
        self.targets=targets;
        self.effect=effect;
        self.name=""
    def apply(self):
        for t in self.targets:
            self.effect(t);

def effect_discount(amount):
    def discount(target):
        for c in target.costs:
            c.amount=c.amount-amount;
            if c.amount<1:c.amount=1;
    return discount;
def effect_bonus_building(amount):
    def bonus_buildings(target):
        target.bonus=target.bonus+1;
    return bonus_buildings;
def effect_bonus_building_affects(amount):
    def bonus_affects(target):
        for a in target.affects:
            a.bonus=a.bonus+amount;
    return bonus_affects


def generate_random_upgrade(game_state):
    effects_pool=[effect_discount,effect_bonus_building,effect_bonus_building_affects]
    building_pool=[]
    for i,b in enumerate(game_state["Buildings"]):
        visible=True;
        for cost in b.costs:
            if not game_state['wallet'].has(cost.name):
                visible=False;
        if visible: building_pool.append(b)
    targets= choices(building_pool,k=choice((range(1,len(building_pool)))))
    effect = choice(effects_pool)
    scale = round(random()*10);
    return upgrade(targets,effect(scale));

