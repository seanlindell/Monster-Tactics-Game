import pygame
import spritemanager as sm

def main():

    cursorXPos = 0
    cursorYPos = 0
    cursorMovementBuffer = 0

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
    myVamp = sm.Vampire()
    myWere = sm.Werewolf()
    myMumm = sm.Mummy()

    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:

        screen.fill((255, 255, 255))

        cursor.update()
        myVamp.update()
        myWere.update()
        myMumm.update()

        for x in range(10):
            for y in range(10):
                screen.blit(purpleTile, (100+x*64,100+y*64))

        screen.blit(myVamp.get_image(), (100+1*64,100+1*64))
        screen.blit(myWere.get_image(), (100+2*64,100+2*64))
        screen.blit(myMumm.get_image(), (100+3*64,100+3*64))
        screen.blit(cursor.get_image(), (100+cursorXPos*64,100+cursorYPos*64))

        pygame.display.flip()
        clock.tick(30)

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
                cursorMovementBuffer = 1
            elif (keystate[pygame.K_DOWN] and cursorYPos < 9):
                cursorYPos += 1
                cursorMovementBuffer = 1
            elif (keystate[pygame.K_RIGHT] and cursorXPos < 9):
                cursorXPos += 1
                cursorMovementBuffer = 1
            elif (keystate[pygame.K_LEFT] and cursorXPos > 0):
                cursorXPos -= 1
                cursorMovementBuffer = 1
        else:
            cursorMovementBuffer = 0
        if (keystate[pygame.K_SPACE]):
            myVamp.animActive = (myVamp.animActive+1)%2
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()