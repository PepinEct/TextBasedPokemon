import threading
import os
import json
from grids import Grid
from math import floor, ceil
import keyboard
"""
===================================
                NOTE
===================================
It doensn't work yet so yea

===================================
                INFO
===================================
-Your pokemom gets renderd at a res of 10x10
-Gridres = 50x32
- ~ is an invisable character that will act as an space


===================================
        CURRENTLY WORKING ON
===================================
GUI CHOICE MENU ETC

"""
LEFT_KEY = 'a'
RIGHT_KEY = 'd'
os.system('MODE 10000,10000')
MAIN_POK_POS = ((6, 8), (16, 19))
OPP_PO_POS = ((35, 20), (40, 27))
FILLER_ICON = '~'
class POKEMOM:
    def __init__(self, TEMPLATEFILE) -> None:
        #stores pokemomdata
        with open(TEMPLATEFILE, 'r') as file:
            data = json.load(file)
        self.HP = data['HP']
        self.Level = data['LVL']
        self.template = data['template']
        self.name = data['name']
        self.HEALTHBAR = None
        self.Turn = False
        

def isEven(num):
    if floor(num/2)*2 != num:
        return False
    else:
        return True
class HEALTHBAR:
    def __init__(self, MAX_HP=15, HPBAR_MAXLEN = 5) -> None:
        self.maxHP = MAX_HP
        self.hpLeft = MAX_HP
        self.HPBAR_MAXLEN = HPBAR_MAXLEN
        self.HPPERBAR = self.maxHP / HPBAR_MAXLEN
        self.template = f'|{"="*HPBAR_MAXLEN}|{self.hpLeft}'
    def hit(self, amount:int):
        self.hpLeft-=amount
        fullbar = ceil(self.hpLeft/self.HPPERBAR)
        rest = self.HPBAR_MAXLEN-fullbar
        self.template = f'|{"="*fullbar}{"-"*rest}|{self.hpLeft}'


class GUI:
    def __init__(self) -> None:
        #handles gui
        self.grid = Grid()
        #Grid gets renderd at a res of 50 x 32
        self.grid.CreateGrid(50, 32, ' ')
        self.update()
        self.ContentBoxDims = None

    #Renders healthbar
    def renderHealthbar(self, hpbar: HEALTHBAR, start: tuple, name=None):
        for x in range(len(hpbar.template)):
            self.grid.set(start[0]+x, start[1], hpbar.template[x])
        if name != None:
            for x in range(len(name)):
                self.grid.set(start[0]+x, start[1]+1, name[x])

    #renders contentbbox
    def renderContentBox(self, start:tuple, end:tuple):
        #generates box with content
        self.ContentBoxDims = (start, end)
        for x in range(end[0]-start[0]):
            self.grid.set(start[0]+x, start[1], '-')
            self.grid.set(start[0]+x, end[1], '-')
        for y in range(end[1]-start[1]+1):
            self.grid.set(start[0], start[1]+y, '|')
            self.grid.set(end[0], end[1]-y, '|')
    
    #Renders screen in contentbox
    def renderTextContentBox(self, text:str):
        
        start = self.ContentBoxDims[0]
        end = self.ContentBoxDims[1]
        textzoneStart = (start[0]+1, start[1]+1) #start of space inside textbox
        textzoneEnd = (end[0]-1, end[1]-1) #end of space inside textbox
        maxLen = textzoneEnd[0] - textzoneStart[1]+1
        maxHeight = textzoneEnd[1] - textzoneStart[1]+1

        #part that calculates the lines
        templine = ''
        lines = []
        for word in text.split(' '):
            lenght = len(word)+1 #+1 for the space
            if not len(templine)+lenght >= maxLen:
                #if the word fits
                templine+=f'{word} '
            else:
                lines.append(templine)
                templine = f'{word} '
        if len(templine) != 0:
            lines.append(templine)
        
        #rendering it on the sceen
        posY = textzoneEnd[1]
        posX = textzoneStart[0]
        loop = 0
        for line in lines:
            if loop >= maxHeight:
                break
            for char in line:
                if char != FILLER_ICON:
                    self.grid.set(posX, posY, char)
                posX+=1
            posX=textzoneStart[0]
            posY-=1
            loop +=1
    def AttackChoiceMenu(self, margin=4):
        template = ''
        _start = self.ContentBoxDims[0]
        _end = self.ContentBoxDims[1]
        MaxLen = _end[0] - _start[0] - 2
        MaxHeight = _end[1] - _start[1] -1
        template+=' '*margin





    def BattleChoiceMenu(self, options: tuple, msg='', margin=4) -> int:
        #Makes a choice between Attack or Item
        #Transitions to attack and item menu's
        template = ''
        template+=msg
        _start = self.ContentBoxDims[0]
        _end = self.ContentBoxDims[1]
        MaxLen = _end[0] - _start[0] - 2
        MaxHeight = _end[1] - _start[1] -1
        
        template+=' '*margin
        choice = 0
        if len(options) > 2:
            pass

        else:
            #2 options
            for x in range(len(options)):
                template+=f'{x+1} {options[x]}{" "*margin}'
            self.renderTextContentBox(template.replace(f'{choice+1}', '>'))
            #Loops for choice
            pressed = False
            self.update()
            while True:
                
                if keyboard.is_pressed(RIGHT_KEY):
                    if not choice == len(options)-1:
                        choice+=1
                        pressed = True
                elif keyboard.is_pressed(LEFT_KEY):
                    if not choice == 0:
                        choice-=1
                        pressed = True
                elif keyboard.is_pressed('\n'):
                    return choice
                if pressed:
                    self.renderTextContentBox(template.replace(f'{choice+1}', '>'))
                    self.update()
                    pressed = False

        




    def renderPok(self, pokemom: POKEMOM ,start: tuple, end: tuple):
        #renders a square for the pokemon
        chords = []
        cur_x = start[0]
        cur_y = start[1]
        for y in range(end[1]-start[1]+1):
            for x in range(end[0]-start[0]+1):
                chords.append((cur_x, cur_y))
                cur_x+=1
            cur_y+=1
            cur_x=start[0]

        #clears the area for the pokemom (TEMP!)
        for chord in chords:
            self.grid.set(chord[0], chord[1], ' ')
        cur_x = start[0]
        cur_y = end[1]
        for char in pokemom.template:
            if char == '\n':
                cur_y-=1
                cur_x=start[0]
            else:
                self.grid.set(cur_x, cur_y, char)
                cur_x+=1


        
    
    def update(self):
        os.system('cls')
        self.grid.ShowGrid()





def makeTemplate(name, LVL=1, template='',HP=15, ATT=5, SP_ATT=5, DEF=5, SP_DEF=5, SPEED=5):
    moveSets = {}
    for x in range(4):
        moveSets[f'move{x+1}'] = {"slogan":'', 'SP_DMG':1, 'DMG':1}
    template = {'name':name,'template':'', 'moveset':moveSets,'HP':HP, 'LVL':LVL, 'items':[],'ATT':ATT, 'SP_ATT':SP_ATT, 'DEF':DEF, 'SP_DEF':SP_DEF, 'SPEED':SPEED}
    with open(f'{name}.json', 'w') as file:
        json.dump(template, file, indent=4)


gui = GUI()
x= HEALTHBAR(100, HPBAR_MAXLEN=5)
x.hit(78)

me = POKEMOM('Pepin.json')
you= POKEMOM('Test.json')

gui.renderPok(me, MAIN_POK_POS[0], MAIN_POK_POS[1])
gui.renderPok(you, OPP_PO_POS[0], OPP_PO_POS[1])

print('') #for some weird reason this has to be done to make it work
gui.renderContentBox((0,0), (49,5))


gui.renderHealthbar(x, (MAIN_POK_POS[0][0]+3, MAIN_POK_POS[0][1]-1), me.name)




u = HEALTHBAR(32)
u.hit(9)
gui.renderHealthbar(u, (OPP_PO_POS[0][0], OPP_PO_POS[0][1]), you.name)
gui.update()
print(gui.BattleChoiceMenu(("Attack", "Item")))

#gui.BattleChoiceMenu(("Hello", 'World'), msg='What will you do?')

#input()
