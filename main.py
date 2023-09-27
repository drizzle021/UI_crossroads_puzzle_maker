import pygame
import json
import random

class Tile:
    def __init__(self, color, x, y):
        self.x = x
        self.y = y
        self.color = color
        self.SCALE = 600//8

        self.rect = pygame.Rect(x,y,self.SCALE,self.SCALE)
    def draw(self):
        pygame.draw.rect(win, self.color, (self.x,self.y,self.SCALE,self.SCALE))

    def changeColor(self,color):
        self.color = color

class Button:
    def __init__(self,rect, command, text):
        self.rect = rect
        self.command = command
        self.text = text
        self.render = FONT.render(self.text,False,(0,0,0))
        self.center = self.render.get_rect(center= self.rect.center)

    def draw(self):
        pygame.draw.rect(win,(255,255,255), self.rect)
        win.blit(self.render,self.center)

    def pushed(self):
        self.command()

class ColorButton:
    def __init__(self,rect,color):
        self.rect = rect
        self.color = color

    def draw(self):
        pygame.draw.rect(win, COLORS[self.color], self.rect)

    def pushed(self):
        print(f"changed to {COLORS[self.color]}")
        return self.color

def drawBG():
    win.fill((150,150,150))

def drawPanel():
    pygame.draw.rect(win, (220, 220, 220), (SCR_WIDTH, 0, SIDE_MARGIN, SCR_HEIGHT+LOWER_MARGIN))
    pygame.draw.rect(win, (220, 220, 220), (0, SCR_HEIGHT, SCR_WIDTH+SIDE_MARGIN, LOWER_MARGIN))

def switchToVertical():
    pass
    #print("switched to vertical")
def switchToHorizontal():
    pass
    #print("switched to horizontal")
def saveGrid():
    global grid
    startStates = scanGrid(grid)
    name = "".join([str(random.randint(0,10)) for i in range(19)])
    exportJSON(startStates,name)

def scanGrid(grid):
    s = set()
    # get colors used in grid
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] not in s and grid[i][j] not in ["W ","E "]:
                s.add(grid[i][j])

    states = []
    for color in s:
        state = [color.rstrip()]
        length = 1
        flag = 0
        for i in range(len(grid)):
            for j in range(len(grid)):
                if grid[i][j] == color:
                    # append coordinates
                    state.append(j)
                    state.append(i)
                    if grid[i][j+1] == color:
                        length+=1
                        if grid[i][j+2] == color:
                            length+=1
                        state.append(length)
                        state.append("h")
                        flag = 1
                        break
                    elif grid[i+1][j] == color:
                        length+=1
                        if grid[i+2][j] == color:
                            length+=1
                        state.append(length)
                        state.append("v")
                        flag = 1
                        break
            if flag == 1:
                break
        states.append(tuple(state))

    return tuple(states)
def exportJSON(startStates,name="test"):
    cars = {}

    for k,i in enumerate(startStates):
        cars.update({f"car{k}":{"color": i[0],
                     "x": i[1],
                     "y": i[2],
                     "size": i[3],
                     "direction": i[4]}})

    with open(f"{name}.json",mode="w") as f:
        json.dump(cars,f,indent=2)



COLORS = {

    "R " : (255, 0, 0),     #RED
    "G " : (0, 255, 0),     #GREEN
    "Pu" : (101, 28, 138),  #PURPLE
    "C " : (39, 216, 219),  #CYAN
    "Gr" : (105, 105, 105), #GREY
    "P " : (249, 61, 255),  #PINK
    "Y " : (255, 233, 36),  #YELLOW
    "O " : (255, 142, 36),  #ORANGE
    "W " : (0, 0, 0),       #WALL
    "E " : (150, 150, 150)  #EMPTY
}
pygame.font.init()
FONT = pygame.font.SysFont("monospace",15)

grid = [["E " for i in range(6)] for i in range(6)]

grid.insert(0, ["W " for i in range(6)])
grid.insert(len(grid), ["W " for i in range(6)])

for row in grid:
    row.insert(0, "W ")
    row.insert(len(grid), "W ")

"""for row in grid:
    print(row)

customGrid = [
['W ', 'W ', 'W ', 'W ', 'W ', 'W ', 'W ', 'W '],
['W ', 'O ', 'O ', 'E ', 'E ', 'E ', 'Pu', 'W '],
['W ', 'Y ', 'E ', 'E ', 'G ', 'E ', 'Pu', 'W '],
['W ', 'Y ', 'R ', 'R ', 'G ', 'E ', 'Pu', 'E '],
['W ', 'Y ', 'E ', 'E ', 'G ', 'E ', 'E ', 'W '],
['W ', 'P ', 'E ', 'E ', 'E ', 'Gr', 'Gr', 'W '],
['W ', 'P ', 'E ', 'C ', 'C ', 'C ', 'E ', 'W '],
['W ', 'W ', 'W ', 'W ', 'W ', 'W ', 'W ', 'W ']
]
print()
states = scanGrid(customGrid)
exportJSON(states)"""

pygame.init()

SCR_WIDTH = 600
SCR_HEIGHT = 600

LOWER_MARGIN = 50
SIDE_MARGIN = 150

win = pygame.display.set_mode((SCR_WIDTH+SIDE_MARGIN,SCR_HEIGHT+LOWER_MARGIN))

run = True

tiles = [[Tile(COLORS[grid[i][j]],600//8*j,i*600//8) for i in range(8)]for j in range(8)]

verticalButton = Button(pygame.Rect(SCR_WIDTH+25,SCR_HEIGHT-200,100,40),switchToVertical,"Vertical")
horizontalButton = Button(pygame.Rect(SCR_WIDTH+25,SCR_HEIGHT-260,100,40),switchToHorizontal,"Horizontal")
saveButton = Button(pygame.Rect(SCR_WIDTH+25,SCR_HEIGHT-140,100,40),saveGrid,"Save")
colorButtons = [
    ColorButton(pygame.Rect(SCR_WIDTH+25,SCR_HEIGHT-300,20,20),"R "),
    ColorButton(pygame.Rect(SCR_WIDTH+45,SCR_HEIGHT-300,20,20),"G "),
    ColorButton(pygame.Rect(SCR_WIDTH+65,SCR_HEIGHT-300,20,20),"Pu"),
    ColorButton(pygame.Rect(SCR_WIDTH+85,SCR_HEIGHT-300,20,20),"Y "),
    ColorButton(pygame.Rect(SCR_WIDTH+25,SCR_HEIGHT-280,20,20),"C "),
    ColorButton(pygame.Rect(SCR_WIDTH+45,SCR_HEIGHT-280,20,20),"Gr"),
    ColorButton(pygame.Rect(SCR_WIDTH+65,SCR_HEIGHT-280,20,20),"P "),
    ColorButton(pygame.Rect(SCR_WIDTH+85,SCR_HEIGHT-280,20,20),"O "),
    ColorButton(pygame.Rect(SCR_WIDTH+130,SCR_HEIGHT-280,20,20),"E ")

]

selectedColor = "R "
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if verticalButton.rect.collidepoint(pos):
                verticalButton.pushed()
            if horizontalButton.rect.collidepoint(pos):
                horizontalButton.pushed()
            if saveButton.rect.collidepoint(pos):
                saveButton.pushed()

            for b in colorButtons:
                if b.rect.collidepoint(pos):
                    selectedColor=b.pushed()


            for k, row in enumerate(tiles):
                for tile in row:
                    if tile.rect.collidepoint(pos) and tile.color!=COLORS["W "]:
                        tile.changeColor(COLORS[selectedColor])
                        grid[row.index(tile)][k] = selectedColor



    drawBG()
    drawPanel()



    for row in tiles:
        for tile in row:
            tile.draw()

    for button in colorButtons:
        button.draw()

    verticalButton.draw()
    horizontalButton.draw()
    saveButton.draw()
    pygame.draw.rect(win, COLORS[selectedColor], pygame.Rect(SCR_WIDTH+30,SCR_HEIGHT-400,80,80))
    pygame.display.update()


pygame.quit()