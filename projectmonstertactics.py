import pygame
import spritemanager as sm

# Gameboard is 16x12, but one dimentional
# Convert (x,y) to (z) by (x+y*16)
# Convert (z) to (x,y) by (z%16, z//16)
gameBoard = [None] * 192

def xytoz(x, y):
    return x+y*16

def ztoxy(z):
    return (z%16,z//16)

def getUnitAt(x, y):
    return gameBoard[xytoz(x,y)]

def setUnitAt(x, y, unit):
    gameBoard[xytoz(x,y)] = unit

def main():

    cursorXPos = 0
    cursorYPos = 0

    cursorMovementBuffer = 0
    selectBuffer = 0

    selectedTileX = -1
    selectedTileY = -1

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1280,800))

    # initialize the pygame module
    pygame.init()

    # load and set the logo
    logo = pygame.image.load("vampire2.png").convert_alpha()
    logo = pygame.transform.scale(logo, (64, 64))
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Project Monster Tactics")

    #Loading tile images, may change later to store them as sprites
    redTile = pygame.image.load("red_tile.png").convert_alpha()
    blueTile = pygame.image.load("blue_tile.png").convert_alpha()
    lblueTile = pygame.image.load("lblue_tile.png").convert_alpha()
    purpleTile = pygame.image.load("purple_tile.png").convert_alpha()
    whiteTile = pygame.image.load("white_tile.png").convert_alpha()
    whiteTile = pygame.transform.scale(whiteTile, (64, 64))
    lblueTile = pygame.transform.scale(lblueTile, (64, 64))
    purpleTile = pygame.transform.scale(purpleTile, (64, 64))

    #Creating sprites defined in spritemanager
    cursor = sm.Cursor()
    setUnitAt(0, 5, sm.Vampire())
    setUnitAt(0, 2, sm.Werewolf())
    setUnitAt(3, 3, sm.Mummy())

    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:

        screen.fill((255, 255, 255))

        cursor.update()

        for x in range(16):
            for y in range(12):
                screen.blit(purpleTile, (25+x*64,20+y*64))

        if (selectedTileX != -1 and selectedTileY != -1):
            screen.blit(lblueTile, (25+selectedTileX*64,20+selectedTileY*64))

        for x in range(16):
            for y in range(12):
                if (getUnitAt(x,y) != None):
                    unit = getUnitAt(x,y)
                    unit.update()
                    screen.blit(getUnitAt(x,y).get_image(), (25+x*64,20+y*64))

        screen.blit(cursor.get_image(), (25+cursorXPos*64,20+cursorYPos*64))        

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

        keystate = pygame.key.get_pressed()
        if not cursorMovementBuffer:
            if (keystate[pygame.K_UP] and cursorYPos > 0):
                cursorYPos -= 1
                cursorMovementBuffer = 2
            elif (keystate[pygame.K_DOWN] and cursorYPos < 11):
                cursorYPos += 1
                cursorMovementBuffer = 2
            elif (keystate[pygame.K_RIGHT] and cursorXPos < 15):
                cursorXPos += 1
                cursorMovementBuffer = 2
            elif (keystate[pygame.K_LEFT] and cursorXPos > 0):
                cursorXPos -= 1
                cursorMovementBuffer = 2
        else:
            if cursorMovementBuffer > 0:
                cursorMovementBuffer -= 1

        if (keystate[pygame.K_SPACE] and selectBuffer == 0):
            # THE BELOW CONDITIONAL WILL BE CHANGED TO CHECK IF UNIT BELONGS TO PLAYER AND IF UNIT HAS ALREADY MOVED
            if(getUnitAt(selectedTileX, selectedTileY) != None and getUnitAt(cursorXPos, cursorYPos) == None):
                setUnitAt(cursorXPos,cursorYPos, getUnitAt(selectedTileX, selectedTileY))
                setUnitAt(selectedTileX,selectedTileY, None)
                selectedTileX = -1
                selectedTileY = -1
            elif ((selectedTileX,selectedTileY) == (cursorXPos, cursorYPos)):
                selectedTileX = -1
                selectedTileY = -1
            else:
                selectedTileX = cursorXPos
                selectedTileY = cursorYPos
            selectBuffer = 3
        elif (selectBuffer > 0):
            selectBuffer -= 1

        # For debug, remove later
        if (keystate[pygame.K_0]):
            setUnitAt(0,0, sm.Vampire())
        
        if (keystate[pygame.K_1]):
            setUnitAt(0,0, sm.Mummy())

        if (keystate[pygame.K_2]):
            setUnitAt(0,0, sm.Werewolf())


        pygame.display.flip()
        clock.tick(30)
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()