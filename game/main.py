#!/bin/python
from cyberbrain import trace
from list_of_buildings import buildings 
from list_of_resources import resources 
from list_of_locations import locations 
from button import BUTTON
from upgrade import generate_random_upgrade;
loc = iter(locations)
from wallet import Wallet 
import pygame, sys, math
from random import random
from pygame.locals import *
pygame.init()
display = pygame.display.set_mode((840, 580))
#Definitions
def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]

def drawtext(string, fs, x, y, r, g, b):
    textfont = pygame.font.SysFont('Open Sans', fs)
    textbox = textfont.render(str(string), False, (r, g, b))
    display.blit(textbox, (x, y))
def render(state):
    display.fill(state['BGCOLOR']);
    start_x_buildings = 20;
    start_y_buildings = 90;
    start_x_resources = 600;
    start_y_resources = 10;
    start_x_buttons = 70;
    start_y_buttons =300
    font_size=28;
    keys = ["T","F","R","D","K"]
    for i,b in enumerate(game_state["Buildings"]):
        costs_string = ""
        visible=True;
        for cost in b.costs:
            if not game_state['wallet'].has(cost.name):
                visible=False;
            costs_string+="("+cost.name+": "+str(round(cost.amount))+")"
        if visible:
            drawtext(f"{keys[i]}:) {b.name}: {str(round(b.count))} bonus:{b.bonus}",font_size,start_x_buildings,start_y_buildings+i*60,255,255,192)
            drawtext(costs_string,font_size,start_x_buildings,start_y_buildings+i*60+28,255,255,192)
    for i,b in enumerate(game_state['wallet'].resources):
        drawtext(b.name+": "+str(round(b.amount)),font_size,start_x_resources,start_y_resources+i*60,255,255,192)
        drawtext("bonus:"+str(b.bonus),font_size,start_x_resources,start_y_resources+i*60+28,255,255,192)
    for i,b in enumerate(game_state['upgrade_buttons']):
        s = "!"
        visible=True;
        print(len(b.costs),"cost len")

        for cost in b.costs:
            if not game_state['wallet'].has(cost.name):
                visible=False;
            s=s+"("+cost.name+": "+str(round(cost.amount))+")"
        if visible:
            drawtext(f"{i}:) {b.name}",font_size,start_x_buttons,start_y_buttons+i*60,255,255,192)
            drawtext(s,font_size,start_x_buttons,start_y_buttons+i*60+28,255,255,192)

    pygame.display.update()

    #drawtext(str(research) + ' Research (R) is improving production by x' + str(tickrate) + ' and costs ' + str(researchcost) + ' bananas.', 18, 10, 40, 31, 255, 0)
 

def update(state):
    for building in state['Buildings']:
        for afb in building.affects:
            for resource in state['wallet'].resources:
                if afb.name==resource.name and building.count>0:
                    bonus = ((resource.bonus&building.bonus)*(resource.bonus&building.bonus))*building.count; 
                    resource.amount += ((afb.amount*building.count / 60)  * state['tick_rate']) + bonus

    state['upgrade_buttons']=[s for s in state['upgrade_buttons'] if not (s.pressed and s.singleUse)]
            

    return state;

game_state = {
    "BGCOLOR":(47,47,47),
    "Buildings":buildings,
    "Location":next(loc),
    "wallet":Wallet(),
    "tick_rate":1,
    "update":update,
    "clock":pygame.time.Clock(),
    "research_count":0,
    "upgrade_buttons":[]
}
game_state['wallet'].resources.append(resources[0])#we only need the first one - the rest will get added via teh game
#more can be appended here with there default value changed for testing
for x in range(3):
    upgrade = generate_random_upgrade(game_state);
    game_state['upgrade_buttons'].append(BUTTON(upgrade))
@trace
def run ():
    while 1:
        print(len(game_state['upgrade_buttons']),"is count")
        game_state['clock'].tick(60)
        keypress = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        #Key bindings
        if keypress[pygame.K_t]:game_state["Buildings"][0].buy(game_state["wallet"])
        if keypress[pygame.K_f]:game_state["Buildings"][1].buy(game_state["wallet"])
        if keypress[pygame.K_r]:game_state["Buildings"][2].buy(game_state["wallet"],game_state)
        if keypress[pygame.K_d]:game_state["Buildings"][3].buy(game_state["wallet"],[game_state,next(loc,locations[0])])
        if keypress[pygame.K_k]:game_state["Buildings"][4].buy(game_state["wallet"])

        for x in range(1,11):
            try:
                key = "K_"+str(x%10)
                if keypress[pygame[f'{key}']]:print("pressed",game_state['upgrade_buttons'][index].press(game_state['wallet']))
            except:
                pass
        if random()<0.00001 and len(game_state['upgrade_buttons'])<game_state["research_count"]:
            upgrade = generate_random_upgrade(game_state);
            game_state['upgrade_buttons'].append(BUTTON(upgrade))
            print("buttons", len(game_state['upgrade_buttons']))
            for b in game_state['upgrade_buttons']:
                print(b.name,"button name",namestr(b.effect,globals()))
        game_state=game_state['update'](game_state);
        render(game_state)
run()