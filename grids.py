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