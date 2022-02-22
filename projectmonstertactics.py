from enum import Enum
import pygame
import spritemanager as sm

# Gameboard is 16x12, but one dimentional
# Convert (x,y) to (z) by (x+y*16)
# Convert (z) to (x,y) by (z%16, z//16)
gameBoard = [None] * 192

# Lists used to store refrences to player and enemy units
# Use createUnitAt() and removeUnit() to create and destroy units
# and they'll mangae these for you
playerUnits = []
enemyUnits = []
isPlayerTurn = 1

# Enum used to differentiate types of cursor modes. Only one should need to be active,
# so its just stored in the cursorMode variable. 
# MAINBOARD is when you're moving around the main board
# DROPDOWN is when you finished moving a unit and deciding what action to take
# TARGETCHOICE is when you select an attacking or supportive action which requires you to choose a target next
class cm(Enum):
    MAINBOARD = 0
    DROPDOWN = 1
    TARGETCHOICE = 2

cursorMode = cm.MAINBOARD

# Utility Functions for helping to manage unit coordinates
def xytoz(x, y):
    return x+y*16

def ztoxy(z):
    return (z%16,z//16)

def getUnitAt(x, y):
    return gameBoard[xytoz(x,y)]

def getDistanceBetween(x1,y1,x2,y2):
    xdif = abs(x1-x2)
    ydif = abs(y1-y2)
    return xdif + ydif

# DO NOT USE THIS METHOD TO CREATE UNITS. USE createUnitAt() INSTEAD
# ONLY USE THIS FOR MOVING UNITS AROUND BY SETTING THE NEW LOCATION
# WITH setUnitAt(newX, newY, getUnitAt(oldX, oldY))
# THEN CLEARING THE OLD LOCATION BY setUnitAt(oldX, oldY, None)
# ENSURE YOU DO NOT OVERWRITE ANY UNITS BY CHECKING getUnitAT(newX, newY) == None
# IF YOU DON'T NEED TO DO ANYTHING FANCY JUST USE safeMoveUnits() INSTEAD

def setUnitAt(x, y, unit):
    gameBoard[xytoz(x,y)] = unit

def safeMoveUnits(oldX, oldY, newX, newY):
    if getUnitAt(oldX, oldY) != None:
        if getUnitAt(newX, newY) == None:
            setUnitAt(newX, newY, getUnitAt(oldX, oldY))
            setUnitAt(oldX, oldY, None)
        else:
            print("WARNING: UNIT AT " + newX + ", " + newY + " WAS GOING TO BE OVERWRITED")
    else:
        print("WARNING: THERE IS NO UNIT AT " + oldX + ", " + oldY + " TO MOVE")

def createUnitAt(x, y, unit: sm.UnitSprite, isPlayerUnit):
    if isPlayerUnit:
        playerUnits.append(unit)
    else:
        unit.makeIntoEnemy()
        enemyUnits.append(unit)
    gameBoard[xytoz(x,y)] = unit

def removeUnit(unit: sm.UnitSprite, isplayerUnit):
    if isplayerUnit:
        playerUnits.remove(unit)
    else:
        enemyUnits.remove(unit)

def setToPlayerTurn():
    global isPlayerTurn
    isPlayerTurn = 1
    for unit in playerUnits:
        unit.hasMoved = 0
    for unit in enemyUnits:
        unit.hasMoved = 1

def setToEnemyTurn():
    global isPlayerTurn
    isPlayerTurn = 0
    for unit in playerUnits:
        unit.hasMoved = 1
    for unit in enemyUnits:
        unit.hasMoved = 0

def main():

    # Cursor coordinates for the main board
    cursorXPos = 0
    cursorYPos = 0

    # Dropdown menu selection cursor location
    dropDownCursorValue = 0

    cursorMovementBuffer = 0
    selectBuffer = 0

    selectedTileX = -1
    selectedTileY = -1

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1280,815))

    # Information and methods for controlling movement canceling
    unitLocationChache = (-1,-1)
    def undoMove():
        safeMoveUnits(cursorXPos, cursorYPos, unitLocationChache[0], unitLocationChache[1])

    # Stores refrences to units needed for displaying stats
    playerUnitForStatDisplay = None
    enemyUnitForStatDisplay = None

    # initialize the pygame module
    pygame.init()

    # load and set the logo
    logo = pygame.image.load("vampire2.png").convert_alpha()
    logo = pygame.transform.scale(logo, (64, 64))
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Project Monster Tactics")

    #Loading tile images, may change later to store them as sprites
    redTile = pygame.image.load("red_tile.png").convert_alpha()
    lblueTile = pygame.image.load("lblue_tile.png").convert_alpha()
    purpleTile = pygame.image.load("purple_tile.png").convert_alpha()

    fullmenu = pygame.image.load("dropdownmenu4.png").convert_alpha()

    playerblockSprite = pygame.image.load("playerstatsblock.png").convert_alpha()
    enemyblockSprite = pygame.image.load("enemystatsblock.png").convert_alpha()

    lblueTile = pygame.transform.scale(lblueTile, (64, 64))
    redTile = pygame.transform.scale(redTile, (64, 64))
    purpleTile = pygame.transform.scale(purpleTile, (64, 64))

    atkIcon = sm.GenericStaticSprite("swords")
    healthIcon = sm.GenericStaticSprite("heart")
    moveIcon = sm.GenericStaticSprite("boot")

    # Text management
    gameFontType = pygame.font.get_default_font()
    def getTextSurface(text, size):
        fullGameFont = pygame.font.Font(gameFontType, size)
        textSurface = fullGameFont.render(text, True, (0,0,0))
        return textSurface


    #Creating sprites defined in spritemanager
    cursor = sm.Cursor()
    createUnitAt(0, 5, sm.Vampire(), 1)
    createUnitAt(0, 2, sm.Werewolf(), 1)
    createUnitAt(3, 3, sm.Mummy(), 1)

    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:

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
                cursorMovementBuffer = 3
            if (keystate[pygame.K_DOWN] and cursorYPos < 11):
                cursorYPos += 1
                cursorMovementBuffer = 3
            if (keystate[pygame.K_RIGHT] and cursorXPos < 15):
                cursorXPos += 1
                cursorMovementBuffer = 3
            if (keystate[pygame.K_LEFT] and cursorXPos > 0):
                cursorXPos -= 1
                cursorMovementBuffer = 3
        else:
            if cursorMovementBuffer > 0:
                cursorMovementBuffer -= 1

        if (keystate[pygame.K_SPACE] and selectBuffer == 0):
            # THE BELOW CONDITIONAL WILL BE CHANGED TO CHECK IF UNIT BELONGS TO PLAYER AND IF UNIT HAS ALREADY MOVED
            if(getUnitAt(cursorXPos, cursorYPos) == None and getUnitAt(selectedTileX, selectedTileY) != None):
                if getUnitAt(selectedTileX, selectedTileY).MOV >= getDistanceBetween(cursorXPos,cursorYPos,selectedTileX,selectedTileY ):
                    unitLocationChache = (selectedTileX, selectedTileY)
                    setUnitAt(cursorXPos,cursorYPos, getUnitAt(selectedTileX, selectedTileY))
                    setUnitAt(selectedTileX,selectedTileY, None)
                    getUnitAt(cursorXPos,cursorYPos).hasMoved = 1
                    selectedTileX = -1
                    selectedTileY = -1
            elif ((selectedTileX,selectedTileY) == (cursorXPos, cursorYPos)):
                selectedTileX = -1
                selectedTileY = -1
            elif ((getUnitAt(cursorXPos, cursorYPos) != None) and ((getUnitAt(cursorXPos, cursorYPos).isAlly) and getUnitAt(cursorXPos, cursorYPos).hasMoved == 0)):
                selectedTileX = cursorXPos
                selectedTileY = cursorYPos
            selectBuffer = 5
        elif (selectBuffer > 0):
            selectBuffer -= 1

        # If the cursor is over a unit, update stat displays
        if getUnitAt(cursorXPos, cursorYPos) != None:
            if getUnitAt(cursorXPos, cursorYPos).isAlly:
                playerUnitForStatDisplay = getUnitAt(cursorXPos, cursorYPos)
            else:
                enemyUnitForStatDisplay = getUnitAt(cursorXPos, cursorYPos)

        # For debug, remove later
        if (keystate[pygame.K_0]):
            createUnitAt(0,0, sm.Vampire(),0)
        
        if (keystate[pygame.K_1]):
            createUnitAt(0,0, sm.Mummy(),0)

        if (keystate[pygame.K_2]):
            createUnitAt(0,0, sm.Werewolf(),0)

        if (keystate[pygame.K_3]):
            setToPlayerTurn()

        if (keystate[pygame.K_4]):
            setToEnemyTurn()

        if isPlayerTurn:
            allPlayerUnitsMoved = 1
            for unit in playerUnits:
                if not unit.hasMoved:
                    allPlayerUnitsMoved = 0
            if allPlayerUnitsMoved:
                print("here")
                setToEnemyTurn()
        else:
            allEnemyUnitsMoved = 1
            for unit in enemyUnits:  
                if not unit.hasMoved:
                    allEnemyUnitsMoved = 0
            if allEnemyUnitsMoved:
                setToPlayerTurn()


        # MANAGE DRAWING TO SCREEN FOR THE REST OF THE GAME LOOP

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
                    if not getUnitAt(x,y).isAlly:
                        screen.blit(redTile, (25+x*64,20+y*64))
                    unit.update()
                    screen.blit(getUnitAt(x,y).get_image(), (25+x*64,20+y*64))


        # Draw sprites which contain stats for player
        screen.blit(playerblockSprite, (1064,20))
        screen.blit(healthIcon.get_image(), (1069,89))
        screen.blit(atkIcon.get_image(), (1069,153))
        screen.blit(moveIcon.get_image(), (1069,217))
        if playerUnitForStatDisplay != None:
            screen.blit(playerUnitForStatDisplay.get_image(), (1069,25))
            screen.blit(getTextSurface(": " + str(playerUnitForStatDisplay.HP), 64), (1133,89))
            screen.blit(getTextSurface(": " + str(playerUnitForStatDisplay.ATK), 64), (1133,153))
            screen.blit(getTextSurface(": " + str(playerUnitForStatDisplay.MOV), 64), (1133,217))

        screen.blit(enemyblockSprite, (1064,410))
        screen.blit(healthIcon.get_image(), (1069,84+390))
        screen.blit(atkIcon.get_image(), (1069,148+390))
        screen.blit(moveIcon.get_image(), (1069,212+390))
        if enemyUnitForStatDisplay != None:
            screen.blit(enemyUnitForStatDisplay.get_image(), (1069,25+390))
            screen.blit(getTextSurface(": " + str(enemyUnitForStatDisplay.HP), 64), (1133,89+390))
            screen.blit(getTextSurface(": " + str(enemyUnitForStatDisplay.ATK), 64), (1133,153+390))
            screen.blit(getTextSurface(": " + str(enemyUnitForStatDisplay.MOV), 64), (1133,217+390))

        screen.blit(cursor.get_image(), (25+cursorXPos*64,20+cursorYPos*64))        

        screen.blit(fullmenu, (25+(1+cursorXPos)*64,20+(1+cursorYPos)*64))

        pygame.display.flip()

        # Doesn't actually manage drawing to screen, but I think it's still important to call it last in the game loop
        clock.tick(30)
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()