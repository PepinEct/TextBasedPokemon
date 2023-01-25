import threading
import os
import json
from math import floor, ceil
import time
import random

#External libaries
from playsound import playsound
import keyboard

"""
==================================
            KNOWN BUGS
==================================
--------------FIXED--------------
-The back button didn't appear and
if pressed it caused a crash
-The recalculation/translation
doens't function quite right
example: sourkid, use any move

==================================
         RECENT CHANGES
==================================
-The sp def and sp attacks can now
be used, as well as the isSp var
(in moves obj in json)
--------------------------------
-The attack stat can now be used
-The attacks can be used a limited
amount.
-Updated pokemmommaker for the new
changes.
-Modified existing pokemom
==================================
                TODO
==================================
-Add functinality for potions
-Add mutliple pokemon option #lower priority cuz time
-2v2 mode
-level system
-Add a way to boost stats
===================================
                NOTE
===================================
It does work, kinda unstable but yea
===================================
                INFO
===================================
-Your pokemom gets renderd at a res of 10x10
-Gridres = 50x32
- ~ is an invisable character that will act as an space
-Defence is a percentage
-Not everything in the pokemon.json will function (not implemented)
- %$&` are illegal character(s) (for moves)

===================================
        CURRENTLY WORKING ON
===================================
-New mode (story type thing)
-Reworking the optionmenu's for
better overview
"""
LEFT_KEY = 'a'
RIGHT_KEY = 'd'
UP_KEY = 'w'
DOWN_KEY = 's'
SOUNDS_FOLDER = 'Sounds'
ENABLE_DEBUG = False #Enable for debugging
POKEMOM_FOLDER = 'Pokemom'
os.system('MODE 10000,10000')
os.system('title Pokemom!')
MAIN_POK_POS = ((6, 9), (16, 20))
MAIN_POK_HPBAR_POS = (MAIN_POK_POS[0][0]+3, MAIN_POK_POS[0][1]-1)
OPP_PO_POS = ((35, 20), (40, 27))
OPP_POK_HPBAR_POS = (OPP_PO_POS[0][0]-1, OPP_PO_POS[0][1]-4)
FILLER_ICON = '~'
SHOW_SP = True
CHAR_MOVE_BYPASS_CHAR= '%'
SETTING_FILENAME = 'PokeSettings.json'
SETTING = {"Choose pokemom": True}
TENICO = '$'
FIVICO = '%'
ONEICO = '&'
ZEROICO = '^'
TWOICO = '*'
EIGHTICO = '`'

#loads settings from file
try:
    with open(SETTING_FILENAME, 'r') as file:
        SETTING = json.load(file)

    
except(FileNotFoundError):
    with open(SETTING_FILENAME, 'w') as file:
        json.dump(SETTING, file, indent=4)

#Settings that get loaded
CHOOSE_POK = SETTING['Choose pokemom']
#AMOUNT_RANDOM_POK = SETTING['Amount Chosen pokemom']

#Copied from my 'grids' libary
class Grid:
    GRID_MAX_X=10
    GRID_MAX_Y=10
    FILL_CHAR = '#'
    PROJECTILE_CHAR = 'O'
    def __init__(self, FILL_CHAR='#') -> None:
        self.grid = []
        #self.getRes() #Unaccisary
        self.FILL_CHAR = FILL_CHAR
        self.CreateGrid()
         
    def getRatio(self, Res:tuple):
        self.ratio = {}
        temp = 0
        #Only for horizontal sceens
        if Res[0] > Res[1]:
            temp = round(Res[0] / Res[1], 1)
            self.ratio[Res[0]] = 1
            self.ratio[Res[1]] = temp
        return self.ratio
    def CreateGrid(self, X=GRID_MAX_X, Y=GRID_MAX_Y,char=''):
        if char == '':
            char = self.FILL_CHAR
        self.GRID_MAX_X = X
        self.GRID_MAX_Y= Y
        self.grid=[]
        for y in range(Y):
            temp= []
            for x in range(X):
                temp.append(char)
            self.grid.append(temp)
    def ShowGrid(self, useIndex=False):
        y_pos = len(self.grid)-1
        for y in self.grid:
            if useIndex:
                print(f"{y_pos}. ", end='\t')
            for x in y:
                print(f" {x} ", end='')
            print(' ')
            y_pos-=1
        if useIndex:
            print('\t', end='')
            for x in range(len(y)):
                print(f" {x} ", end='')

    def set(self, X, Y, char=PROJECTILE_CHAR):
        Y = len(self.grid)-Y-1
        temp = self.grid[Y]
        temp[X] = char
        self.grid[Y] = temp

#End libery




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
        self.moveset = data['moveset']
        self.Turn = False
        self.speed = data['SPEED']
        self.defence = data['DEF']
        self.attack = data['ATT']
        self.sp_def = data['SP_DEF']
        self.sp_att = data['SP_ATT']
        
        #Adds used to moveset
        for move in self.moveset:
            self.moveset[move]['Used'] = self.moveset[move]['MAX_USE']

    def setMoveUses(self, move:str, Amount:int=-1):
        self.moveset[move]['Used'] += Amount


#-------------------------------------------Start standalone functions-------------------------------------------

def debug(msg:str, logfile = 'logs.txt', IsList=False):
    if ENABLE_DEBUG:
        template=''
        if type(msg) == 'list' or type(msg) == dict or IsList:
            for x in msg:
                template+=f'{x} '
            with open(logfile, 'a') as file:
                file.writelines(template+'\n')
        else:
            with open(logfile, 'a') as file:
                file.writelines(str(msg)+'\n')

def pressEnter():
    input()
    time.sleep(1)

class placeholder:
    #a pokemom placeholder
    def __init__(self) -> None:
        self.template = '          \n          \n          \n          \n          \n          \n          \n          \n          \n          '


def isEven(num):
    if num == 0:
        return False
    if floor(num/2)*2 != num:
        return False
    else:
        return True

def makeAmntTemplate(num: int):
    if num == 0:
        return ZEROICO
    ten = int(floor(num/10))
    num -= ten*10
    fiv = floor(num / 5)
    num -= fiv*5
    two = floor(num / 2)
    num -= two*2
    one = int(num / 1)
    template = f"{ten*TENICO}{FIVICO*fiv}{two*TWOICO}{one*ONEICO}"
    return template
    

def TranslateAmntLine(line:str): #new translator
    pulled = []
    for char in line:
        pulled.append(char)
    locs = []
    pos = 0
    index = 9999
    tempAmnt = 0
    templates = {}
    tempTemp = ''
    for char in pulled:
        if char == TENICO:
            tempAmnt+=10
            tempTemp+=TENICO
            locs.append(pos)
        elif char == FIVICO:
            tempAmnt+=5
            tempTemp+=FIVICO
            locs.append(pos)
        elif char == ZEROICO:
            tempTemp+=ZEROICO
            locs.append(pos)
        elif char == TWOICO:
            tempAmnt+=2
            tempTemp+=TWOICO
            locs.append(pos)
        elif char == ONEICO:
            tempAmnt +=1
            tempTemp+=ONEICO
            locs.append(pos)
        else:
            if tempTemp!='':
                first = False
                for x in locs:
                    if not first:
                        pulled[x] = str(index)
                        first = True
                    else:
                        pulled[x] = ''
                templates[str(index)] = tempAmnt
                index+=1
                locs = []
                tempTemp =''
                tempAmnt = 0
        pos+=1
    line = ''
    for char in pulled:
        line+=char
    for index in templates:
        line = line.replace(index, str(templates[str(index)]))
    return line


#-------------------------------------------End standalone functions-------------------------------------------

class HEALTHBAR:
    def __init__(self, MAX_HP=15, HPBAR_MAXLEN = 5, padding=3) -> None:
        self.maxHP = MAX_HP
        self.hpLeft = MAX_HP
        self.HPBAR_MAXLEN = HPBAR_MAXLEN
        self.HPPERBAR = self.maxHP / HPBAR_MAXLEN
        self.template = f'|{"="*HPBAR_MAXLEN}|{self.hpLeft}'+' '*padding
        self.padding = padding
    def hit(self, amount:int):
        self.hpLeft-=amount
        if self.hpLeft <= 0:
            self.hpLeft = 0
        fullbar = ceil(self.hpLeft/self.HPPERBAR)
        rest = self.HPBAR_MAXLEN-fullbar
        self.template = f'|{"="*fullbar}{"-"*rest}|{self.hpLeft}'+' '*self.padding
        #debug(f'{self.template}')


class SOUNDS:
    def play(x):
        y = threading.Thread(target=x)
        #y.setDaemon(True)
        y.start()
    def select():
        playsound(f"{SOUNDS_FOLDER}/select.wav")



class GUI:
    def __init__(self) -> None:
        #handles gui
        self.grid = Grid()
        #Grid gets renderd at a res of 50 x 32
        self.grid.CreateGrid(50, 32, ' ')
        self.update()
        self.ContentBoxDims = None
        self.AUTOUPDATE = False

    #Renders healthbar
    def renderHealthbar(self, pok:POKEMOM, start: tuple):
        hpbar = pok.HEALTHBAR
        name = pok.name
        for x in range(len(hpbar.template)):
            self.grid.set(start[0]+x, start[1], hpbar.template[x])
        if name != None:
            for x in range(len(name)):
                self.grid.set(start[0]+x, start[1]+1, name[x])
        if self.AUTOUPDATE:
            self.update


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
        if self.AUTOUPDATE:
            self.update

    def clearContentBox(self):
        self.renderTextContentBox('')
        self.update()

    #Renders indivual line in contentbox
    def renderLineContentBox(self, text:str, line:int):
        start = self.ContentBoxDims[0]
        end = self.ContentBoxDims[1]
        textzoneStart = (start[0]+1, start[1]+1) #start of space inside textbox
        textzoneEnd = (end[0]-1, end[1]-1) #end of space inside textbox
        maxLen = textzoneEnd[0] - textzoneStart[1]+1
        maxHeight = textzoneEnd[1] - textzoneStart[1]+1
        pos = 0
        for char in text:
            self.grid.set(textzoneStart[0]+pos, textzoneEnd[1]-line, char.replace(FILLER_ICON, ' '))
            pos+=1


    def renderTextContentBox(self, text:str):
        
        start = self.ContentBoxDims[0]
        end = self.ContentBoxDims[1]
        textzoneStart = (start[0]+1, start[1]+1) #start of space inside textbox
        textzoneEnd = (end[0]-1, end[1]-1) #end of space inside textbox
        maxLen = textzoneEnd[0] - textzoneStart[1]+1
        maxHeight = textzoneEnd[1] - textzoneStart[1]+1

        #cleans the textbox
        for y in range(maxHeight):
            for x in range(maxLen):
                self.grid.set(textzoneStart[0]+x, textzoneEnd[1]-y, ' ')

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
                char = char.replace(FILLER_ICON, ' ')
                self.grid.set(posX, posY, char)
                posX+=1
            posX=textzoneStart[0]
            posY-=1
            loop +=1
        if self.AUTOUPDATE:
            self.update

    def AttackChoiceMenu(self, pok: POKEMOM, margin=4, AddBack=True, skipMoveset = False, msg='What will you do?', ShowUses=True, ShowSP_VIS=True):
        self.renderLineContentBox(msg, 0)
        
        _start = self.ContentBoxDims[0]
        _end = self.ContentBoxDims[1]
        MaxLen = _end[0] - _start[0] - 2
        choice = 1
        moves = []
        for move in pok.moveset:
            moves.append(move)
        if AddBack:
            moves.append('Back')
        pos = 0
        linepos = 1
        
        size = []
        xtraSpace = 0
        
        for x in range(floor(len(moves)/2)):
            size.append(moves[(x+1)*2-2])
        size.sort()
        templine = ''
        lines = []
        for move in moves:
            xtra_str = ''
            if ShowSP_VIS and SHOW_SP:
                try:
                    if pok.moveset[move]['isSP']:
                        xtra_str+='!'
                except(KeyError) as e: debug(e) #its the 'back' option wich is added to the 'moves'
            if isEven(pos):
                lines.append(templine)
                templine=''
                linepos+=1
            if not ShowUses:
                templine+=f'{FILLER_ICON*margin}{pos+1} {xtra_str}{move}'
            else:
                try:
                    templine+=f'{FILLER_ICON*margin}{pos+1} {xtra_str}{move}({makeAmntTemplate(pok.moveset[move]["Used"])}/{makeAmntTemplate(pok.moveset[move]["MAX_USE"])})'
                except(KeyError) as e: templine+=f'{FILLER_ICON*margin}{pos+1} {xtra_str}{move}' #Its prob 'back' or any other move that isnt part of the moveset (for setting etc)

            pos+=1
        if templine!='':
            lines.append(templine)

        #function that 'updates' the choice gui ig
        def CHOICEUPDATE(choice):
            pos = 1
            gui.clearContentBox()
            self.renderLineContentBox(msg, 0)
            for line in lines:
                line = line.replace(str(choice), '>')
                line = TranslateAmntLine(line)
                self.renderLineContentBox(line, pos)
                pos+=1
        CHOICEUPDATE(choice)
        self.update()
        #menu loop
        pressed = False
        while True:
                
                if keyboard.is_pressed(RIGHT_KEY):
                    if not choice == len(moves):
                        choice+=1
                        pressed = True
                elif keyboard.is_pressed(LEFT_KEY):
                    if not choice == 1:
                        choice-=1
                        pressed = True
                elif keyboard.is_pressed(UP_KEY):
                    if not choice <= 2:
                        choice-=2
                        pressed = True
                if keyboard.is_pressed(DOWN_KEY):
                    if not choice >= len(moves)-1:
                        choice+=2
                        pressed = True
                elif keyboard.is_pressed('\n'):
                    time.sleep(0.1)
                    #SOUNDS.play(SOUNDS.select)
                    try:
                        if not pok.moveset[(moves[choice-1])]['Used'] <= 0:
                            pok.moveset[(moves[choice-1])]['Used']-=1
                            return moves[choice-1]
                    except(TypeError): #prob not a pokemom
                        return moves[choice-1]
                    except(KeyError): #Prob back
                        return moves[choice-1]
                if pressed:
                    #SOUNDS.play(SOUNDS.select)
                    CHOICEUPDATE(choice)
                    self.update()
                    time.sleep(0.1)
                    pressed = False




    def BattleChoiceMenu(self, options: tuple, msg='', margin=4) -> int:
        #Makes a choice between Attack or Item
        #Transitions to attack and item menu's

        #returns index of options
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
            time.sleep(0.2)
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
                    #SOUNDS.play(SOUNDS.select)
                    time.sleep(0.1)
                    return choice
                if pressed:
                    self.renderTextContentBox(template.replace(f'{choice+1}', '>'))
                    self.update()
                    pressed = False
                    #SOUNDS.play(SOUNDS.select)
                    time.sleep(0.1)

        

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
        if self.AUTOUPDATE:
            self.update

    def update(self):
        os.system('cls')
        self.grid.ShowGrid()

def autoDamage(host: POKEMOM, target:POKEMOM, gui:GUI) -> int:
    #returns damage
    temp = []
    for move in host.moveset:
        temp.append(move)
    using = host.moveset[temp[random.randint(0, len(temp)-1)]]
    if not using['isSP']:
        damage = round(using['DMG']/100*(100+target.defence))
        damage = round(damage/100*(100+host.attack))
    else:
        damage = round(using['DMG']/100*(100+target.sp_def))
        damage = round(damage/100*(100+host.sp_att))
    target.HEALTHBAR.hit(damage)
    gui.renderHealthbar(target, MAIN_POK_HPBAR_POS) #Only hardcoded part
    slogan = using['slogan'].replace('%name%', host.name).replace('%target%', target.name).split(';')
    for line in slogan:
        gui.renderTextContentBox(line)
        gui.update()
        input()
    
def Damage(host: POKEMOM, target:POKEMOM, move:dict, gui:GUI):
    move = host.moveset[move]
    #debug(move)
    if not move['isSP']:
        damage = round(move['DMG']/100*(100+target.defence))
        damage = round(damage/100*(100+host.attack))
        #debug('Not sp')
    else:
        damage = round(move['DMG']/100*(100+target.sp_def))
        damage = round(damage/100*(100+host.sp_att))
        #debug('Is sp')
    #debug(f'Damage: {damage}')
    slogan = move['slogan'].replace('%name%', host.name).replace('%target%', target.name).split(';')
    target.HEALTHBAR.hit(damage)
    gui.renderHealthbar(target, OPP_POK_HPBAR_POS) #Only hardcoded part, perhaps store pos in pok obj?

    gui.clearContentBox()
    gui.renderTextContentBox(slogan[0])
    gui.update()

    pressEnter()

    pressEnter()


def randomPok(amount: int) -> list:
    class holder:
        def __init__(self, filename, name) -> None:
            self.filename = filename
            self.name = name
    poks = {}
    total = []
    for pok in os.listdir(POKEMOM_FOLDER):
        total.append(POKEMOM(f'{POKEMOM_FOLDER}/{pok}'))
    for x in range(amount):
        pos = random.randint(0, len(total)-(1+x))
        poks[total[pos].name] = total[pos]
        total.pop(pos)

    return poks


def makeTemplate(name, LVL=1, template='',HP=15, ATT=5, SP_ATT=5, DEF=5, SP_DEF=5, SPEED=5):
    moveSets = {}
    for x in range(4):
        maxUses = 5 #temp
        moveSets[f'move{x+1}'] = {"slogan":'', 'SP_DMG':1, 'DMG':1, 'MAX_USE':maxUses, "Used":maxUses}
    template = {'name':name,'template':'', 'moveset':moveSets,'HP':HP, 'LVL':LVL, 'items':[],'ATT':ATT, 'SP_ATT':SP_ATT, 'DEF':DEF, 'SP_DEF':SP_DEF, 'SPEED':SPEED}
    with open(f'{name}.json', 'w') as file:
        json.dump(template, file, indent=4)

if __name__ == '__main__': #for testing
    #gameloop
    while True:
        #Initializing info
        gui = GUI()
        
        #pokemom gets chosen randomly, in the future there will be an menu for that
        availiblePok = os.listdir(POKEMOM_FOLDER)
        MainPok = POKEMOM(f"{POKEMOM_FOLDER}/{availiblePok[random.randint(0, len(availiblePok)-1)]}") #random file from the availible folder
        OppPok = POKEMOM(f"{POKEMOM_FOLDER}/{availiblePok[random.randint(0, len(availiblePok)-1)]}")
        MainPok.HEALTHBAR = HEALTHBAR(MainPok.HP)
        OppPok.HEALTHBAR = HEALTHBAR(OppPok.HP)

        #rendering contentbox
        gui.renderContentBox((0,0), (49,5)) #Contentbox

        #chosing poks manual
        if CHOOSE_POK:
            randomPoks = randomPok(4)
            msg = 'Choose one:'
            msg+=FILLER_ICON*(46-len(msg))
            temp = placeholder()
            temp.moveset = randomPoks
            choice = gui.AttackChoiceMenu(temp, AddBack=False, msg=msg, ShowUses=False, ShowSP_VIS=False)
            MainPok = randomPoks[choice]
            MainPok.HEALTHBAR = HEALTHBAR(MainPok.HP)
        

        #rendering poks
        gui.renderPok(MainPok, MAIN_POK_POS[0], MAIN_POK_POS[1]) #main pokemon
        gui.renderPok(OppPok, OPP_PO_POS[0], OPP_PO_POS[1]) #Opponent

        #Rendering
        gui.renderHealthbar(MainPok, MAIN_POK_HPBAR_POS)
        gui.renderHealthbar(OppPok, OPP_POK_HPBAR_POS)



        #Finally updating gui
        gui.update()
        print('') #for some odd reason this has to be done to make it work

        #Misc
        turn = MainPok.speed >= OppPok.speed
        
        gui.renderTextContentBox(f'A wild {OppPok.name} has appeared!')
        gui.update()
        input()
        input()
        if turn:
            gui.renderTextContentBox(f'The first turn is for {MainPok.name}')
        else:
            gui.renderTextContentBox(f'The first turn is for {OppPok.name}')
        gui.update()
        input()
        #Mainloop
        while True:
            gui.clearContentBox()

            #Checks if hp of one of the
            if MainPok.HEALTHBAR.hpLeft == 0:
                gui.renderPok(placeholder(), MAIN_POK_POS[0], MAIN_POK_POS[1])
                gui.renderTextContentBox(f'{MainPok.name} fainted, {OppPok.name} won!')
                gui.update()
                input()
                break
            elif OppPok.HEALTHBAR.hpLeft == 0:
                gui.renderPok(placeholder(), OPP_PO_POS[0], OPP_PO_POS[1])
                gui.renderTextContentBox(f'{OppPok.name} fainted, {MainPok.name} won!')
                gui.update()
                input()
                break
            if turn:
                #battleoptionloop
                while True:
                    gui.clearContentBox()
                    battleOption = gui.BattleChoiceMenu(("Attack", 'Run') ,'What will you do?')
                    gui.clearContentBox()
                    if battleOption == 0:
                        attackMenu = gui.AttackChoiceMenu(MainPok)
                        gui.clearContentBox()
                        gui.update()
                        if attackMenu == 'Back':
                            pass #back
                        else:
                            #attack, pehaps make function?
                            Damage(MainPok, OppPok, attackMenu, gui)

                            input()

                            break
                    else: #run
                        gui.clearContentBox()
                        gui.renderTextContentBox('You couldn\'t get away.')
                        gui.update()
                        input()
                        break
                    gui.clearContentBox()
                turn = False
            else:
                autoDamage(OppPok, MainPok, gui)
                turn= True
            #input()
        gui.clearContentBox()
        choice = gui.BattleChoiceMenu(("Yes", 'No'), 'Do you want to play again?')
        if choice != 0:
            break
