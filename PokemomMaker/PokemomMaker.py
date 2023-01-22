import json



#---------------------------------------------------------------Start grids lib---------------------------------------------------------------
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

#---------------------------------------------------------------End grids lib---------------------------------------------------------------

TEMPLATE_FILENAME = 'Drawing.txt'
AMNT_MOVES = 4 #standard, only change for testing
grid = Grid()
XDIM = 20
YDIM = 20
grid.CreateGrid(XDIM, YDIM, ' ')
name = input('Enter name:\n>>')
main = {"Note": "Made with pokemommaker"}
hp = 0

def getInt(msg) -> int:
    while True:
        try:
            temp = round(int(input(f'{msg}\n>>')))
            break
        except: print("Enter a round number please")
    return temp


hp = getInt('Enter amount hp (btwn 20 and 40 recommended)')
DEF = getInt('Enter amount def (btwn 5 and 30 recommended)')
SP_DEF = getInt('Enter amount SP def (btwn 5 and 30 recommended)')
ATT = getInt('Enter amount attack (btwn 10 and 35 recommended)')
SP_ATT = getInt('Enter amount SP attack (btwn 10 and 35 recommended)')
speed = getInt('Enter amount speed (btwn 3 and 6 recommended)')

def getTemplateRaw() -> str:
    with open(TEMPLATE_FILENAME, 'r') as file:
        lines = ''
        for line in file:
            lines+=line
        return lines

def getTemplate() -> str:
    with open(TEMPLATE_FILENAME, 'r') as file:
        lines = ''
        for line in file:
            lines+=line.replace('\\', '\\\\').replace('\n', '\\n')
        return lines

def makeMoveset() -> dict:
    movesets = {}
    for x in range(AMNT_MOVES):
        temp = {}
        movename = input(f"Enter move {x+1}'s name:\n>>")
        max_use = getInt(f'How many times can "{movename}" be used?')
        isSP = None
        while True:
            getSp = input("Is this move SP? (y/n)\n>>")
            if getSp.lower() == 'y':
                isSP = True
                break
            elif getSp.lower() == 'n':
                isSP = False
                break
            else:
                print("Please enter one of the options.")
        slogan = input(f'Enter slogan of move: "{movename}" (text that appears in the textbox at the bottom)\n(use %name% for the name of the pokemom)\n(use %target% for the opponents name)\n>>')
        dmg = getInt(f'Enter amount damage of {movename}')
        temp['slogan'] = slogan
        temp['DMG'] = dmg
        temp["MAX_USE"] = max_use
        temp['isSP'] = isSP
        movesets[movename] = temp
    return movesets


def makeTemplate(name, LVL=1, template='',HP=15, ATT=5, SP_ATT=5, DEF=5, SP_DEF=5, SPEED=5, MOVESETS={}):
    moveSets = MOVESETS
    if len(moveSets) == 0:
        for x in range(4):
            moveSets[f'move{x+1}'] = {"slogan":'', 'SP_DMG':1, 'DMG':1}
    template = {'name':name,'template':template, 'moveset':moveSets,'HP':HP, 'LVL':LVL, 'items':[],'ATT':ATT, 'SP_ATT':SP_ATT, 'DEF':DEF, 'SP_DEF':SP_DEF, 'SPEED':SPEED}
    with open(f'{name}.json', 'w') as file:
        json.dump(template, file, indent=4)

def showTemplate(template, grid: Grid):
    posx = 0
    posy = YDIM-1
    for char in template:
        if char != '\n':
            grid.set(posx, posy, char)
            posx+=1
        else:
            posy-=1
            posx=0
    grid.ShowGrid()

moveset = makeMoveset()

print("This is your drawing/template:\n")

template = getTemplateRaw()
showTemplate(getTemplateRaw(), grid)

x = input('Want to continue? (y/n)\n>>')

if x == 'y':
    with open(f'{name}.json', 'w') as file:
        makeTemplate(name, template=template, DEF=DEF, MOVESETS=moveset, SPEED=speed, ATT=ATT, SP_ATT=SP_ATT, SP_DEF=SP_DEF, HP=hp)
    print(f"Done! Put the '{name}.json' in your pokemom folder and enjoy!")
else:
    print("Canceled!")


