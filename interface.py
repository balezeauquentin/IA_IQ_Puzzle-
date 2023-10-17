import pygame as pg
from jeu import *

# TODO:
# Finir la preview de la piece avant de la poser
# Ameliorer les graphismes


class Interface:

    #Default size of a square from a shape
    SQUARE_SIZE = 100

    TITLE = "IQ Puzzler"

    # Couleurs (r,g,b)
    class Colors:
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        GREEN = (0, 255, 0)
        MAGENTA = (255, 0, 255)
        CYAN = (0, 255, 255)
        YELLOW = (255, 255, 0)
        PINK = (255, 0, 128)
        PURPLE = (192, 0, 192)
        ORANGE = (255, 128, 0)
        DARK_GREEN = (0, 255, 128)
        GREY = (128, 128, 128)
        BLACK = (0, 0, 0)
        WHITE = (255, 255 ,255)   


    def __init__(self, height = 5, width = 11) -> None:

        # Used to make sure when a key is held down that we only press it once
        self.previous_keys = []

        # By default select the first shape
        self.held_shape_id = 1
        self.held_shape = Piece(self.held_shape_id)

        self.plateau = Plateau(height, width)

        # Creates the pygame window
        self.bkg_color = Interface.Colors.WHITE
        self.WIN_WIDTH = width * self.SQUARE_SIZE
        self.WIN_HEIGHT = height * self.SQUARE_SIZE
        self.screen = pg.display.set_mode((self.WIN_WIDTH , self.WIN_HEIGHT))
        pg.display.set_caption(self.TITLE)

        self.isRunning = True

    def update(self) -> None:
        """
        Called once every frame
        """
        self.screen.fill(self.bkg_color)
        x,y = 0,0
        
        for ligne in self.plateau:
            for case in ligne:
                if case != 0:
                    self.drawSquare(case,x,y)
                x += self.SQUARE_SIZE
            x = 0
            y += self.SQUARE_SIZE

        self.drawGrid()
        pg.display.flip() 
        pg.display.update()

    def drawGrid(self) -> None:
        #Draws horizontal lines
        for y in range(len(self.plateau)):
            pg.draw.line(self.screen, Interface.Colors.BLACK, (0, y*self.SQUARE_SIZE), (self.WIN_WIDTH, y*self.SQUARE_SIZE))
        for x in range(len(self.plateau[0])):
            pg.draw.line(self.screen, Interface.Colors.BLACK, (x * self.SQUARE_SIZE, 0), (x * self.SQUARE_SIZE, self.WIN_WIDTH))

    def drawSquare(self, squareID:int, x:int, y:int) -> None:
        pg.draw.rect(self.screen, getColorFromID(squareID), pg.Rect(x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def drawPreview(self):
        p = Piece(self.held_shape_id)
        placer_piece(self.plateau, )
        pg.draw.rect(self.screen, getColorFromID(squareID), pg.Rect(x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def events(self) -> None:
        """
        Call events() before update()
        """
        self.mousePos = pg.mouse.get_pos()
        keys = pg.key.get_pressed()
        for event in pg.event.get():        
            if event.type == pg.QUIT: 
                self.isRunning = False
            if event.type == pg.MOUSEBUTTONDOWN:
                pos_rectified = int(self.mousePos[1] / self.SQUARE_SIZE), int(self.mousePos[0] / self.SQUARE_SIZE)
                placer_piece(self.plateau, self.held_shape, pos_rectified)
        if keys[pg.K_ESCAPE] :
            self.isRunning = False
        if keys[pg.K_LEFT] and keys[pg.K_LEFT] != self.previous_keys[pg.K_LEFT]:
            self.change_piece_id("+")
        if keys[pg.K_RIGHT] and  keys[pg.K_RIGHT] != self.previous_keys[pg.K_RIGHT]:
            self.change_piece_id("-")
        
        # if keys[pg.K_r] and keys[pg.K_r] != self.previous_keys[pg.K_r]:
        #     self.held_shape = tourner_piece_horraire(self.held_shape)

        self.previous_keys = keys

    def change_piece_id(self,mode:str) -> None:
        """
        Changes the ID of the shape currently in the players hand
        Does checking to make sure the ID does go higher than the number of shapes present in the game
        """
        if(mode == "+" and self.held_shape_id < 12):
            self.held_shape_id += 1
        elif(mode == "-" and self.held_shape_id > 1):
            self.held_shape_id -= 1
        elif mode == "+" and self.held_shape_id == 12:
            self.held_shape_id = 1
        elif mode == "-" and self.held_shape_id == 1:
            self.held_shape_id = 12
        else:
            self.held_shape_id = 1

        
        self.held_shape = Piece(self.held_shape_id)

    

def getColorFromID(id:int) -> tuple[int,int,int] | None:
    """
    Returns a color given the ID of a shape
    """
    match id:
        case 1:
            color = Interface.Colors.RED
        case 2:
            color = Interface.Colors.BLUE
        case 3:
            color = Interface.Colors.GREEN
        case 4:
            color = Interface.Colors.MAGENTA
        case 5:
            color = Interface.Colors.CYAN
        case 6:
            color = Interface.Colors.YELLOW
        case 7:
            color = Interface.Colors.ORANGE
        case 8:
            color = Interface.Colors.PINK
        case 9:
            color = Interface.Colors.PURPLE
        case 10:
            color = Interface.Colors.DARK_GREEN
        case 11:
            color = Interface.Colors.GREY
        case 12:
            color = Interface.Colors.BLACK
        case _:
            color = None
    return color

if __name__ == "__main__":
    inte = Interface()
    p = Piece(1)
    # placer_piece(inte.plateau, p, (2,0))
    # placer_piece(inte.plateau, Piece(2), (0,4))
    # placer_piece(inte.plateau, Piece(3), (1,2))
    # placer_piece(inte.plateau, Piece(4), (1,1))
    # placer_piece(inte.plateau, Piece(5), (0,5))


    pg.time.Clock().tick(60)
    while inte.isRunning: 
        inte.events()
        inte.update()