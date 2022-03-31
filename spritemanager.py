from aifc import Error
import pygame
import os

# Text management
gameFontType = pygame.font.get_default_font()
def getTextSurface(text, size):
        fullGameFont = pygame.font.Font(gameFontType, size)
        textSurface = fullGameFont.render(text, True, (0,0,0))
        return textSurface

# This method is used to load the surfaces needed for animated and non-animated sprites
# When saving images for sprites, save as pngs and for animated sprites, have each frame
# be a seperate png differentiated by a number suffix starting at one and counting up.
# EXAMPLE: Non-animated sprite of cat: file named cat.png    Load it for a sprite with: myCatSprite.images = load_images("cat")
# *note that you do not include the ".png" in the string with the filename 
# EXAMPLE: Animated sprite of cat: files named cat1.png, cat2.png, cat3.png, ...    Load it for a sprite with: myCatSprite.images = load_images("cat")
def load_images(fileName):
    if(os.path.exists(fileName +".png")):
        return [pygame.image.load(fileName +".png").convert_alpha()]
    elif(os.path.exists(fileName +"1.png")):
        i = 1
        images = []
        images.append(pygame.image.load(fileName +"1.png").convert_alpha())
        while(os.path.exists(fileName + str(i + 1) +".png")):
            images.append(pygame.image.load(fileName + str(i + 1) +".png").convert_alpha())
            i += 1
        return images
    else:
        print("Did not find: " + fileName)

def resize_load_images(fileName):
    if(os.path.exists(fileName +".png")):
        return [pygame.transform.scale(pygame.image.load(fileName +".png").convert_alpha(),(400,400)).convert_alpha()]
    elif(os.path.exists(fileName +"1.png")):
        i = 1
        images = []
        images.append(pygame.transform.scale(pygame.image.load(fileName +"1.png").convert_alpha(),(400,400)).convert_alpha())
        while(os.path.exists(fileName + str(i + 1) +".png")):
            images.append(pygame.transform.scale(pygame.image.load(fileName + str(i + 1) + ".png").convert_alpha(),(400,400)).convert_alpha())
            i += 1
        return images
    else:
        print("Did not find: " + fileName)

# Use instantiations of this class for sprites that don't do much besides moving around.
# IF YOU WANT A SPRITE WITH MORE FUNCTIONALITY STORED IN IT: create a subclass of this sprite and incorperate that functionality there
# For example, a cusor. Make sure to set images and animCycle. 
# They can be set by just passing them as arguments
# images contains the sprites that make up the animation and should set using the load_images() function, 
#       or by passing the string for the images as the first argument during instantiation
# animCycle is how many game-frames each animation-frame should show before changing to the next game. The game runs at
#       30 game-frames per second, so keep that in mind when deciding how long each frame should last. It is 15 by default
# If you want the animation to pause, switch the animActive field
# If you want the animation to skip to a specific frame, use switch_to_frame()
# CORE USEAGE: call mySprite.update() each game-frame, and when blitting to screen, use mySprite.get_image() to get the appopriate frame to draw
class GenericAnimatedSprite(pygame.sprite.Sprite):

    animCycle = 15
    animActive = True
    gameFrameCounter = 0
    currentSpriteFrame = 0
    images = []

    def __init__(self, images: str, animCycle: int):
        pygame.sprite.Sprite.__init__(self)
        self.images = load_images(images)
        self.animCycle = animCycle

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def update(self):
        if self.animActive:
            self.gameFrameCounter += 1
            if(self.gameFrameCounter == self.animCycle):
                self.currentSpriteFrame += 1
                self.gameFrameCounter = 0
                if(self.currentSpriteFrame == len(self.images)):
                    self.currentSpriteFrame = 0
    
    def switch_to_frame(self, frame):
        if(frame<len(self.images) and frame > -1):
            self.currentSpriteFrame = frame
            self.gameFrameCounter = 0
        else:
            print("Frame out of bounds")

    def get_image(self):
        return self.images[self.currentSpriteFrame]
    
class GenericResizedAnimatedSprite(pygame.sprite.Sprite):

    animCycle = 15
    animActive = True
    gameFrameCounter = 0
    currentSpriteFrame = 0
    images = []

    def __init__(self, images, animCycle):
        pygame.sprite.Sprite.__init__(self)
        self.images = resize_load_images(images)
        self.animCycle = animCycle

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def update(self):
        if self.animActive:
            self.gameFrameCounter += 1
            if(self.gameFrameCounter == self.animCycle):
                self.currentSpriteFrame += 1
                self.gameFrameCounter = 0
                if(self.currentSpriteFrame == len(self.images)):
                    self.currentSpriteFrame = 0
    
    def switch_to_frame(self, frame):
        if(frame<len(self.images) and frame > -1):
            self.currentSpriteFrame = frame
            self.gameFrameCounter = 0
        else:
            print("Frame out of bounds")

    def get_image(self):
        return self.images[self.currentSpriteFrame]


# Basic sprite which is not animated
class GenericStaticSprite(pygame.sprite.Sprite):

    images = []

    def __init__(self, image: str):
        pygame.sprite.Sprite.__init__(self)
        self.images = load_images(image)

    def get_image(self):
        return self.images[0]


# Subclass of GenericAnimatedSprite intended to be used by creating further subclasses for each unit type.
# Avoid instatantiating this sprite on its own
class UnitSprite(GenericAnimatedSprite):

    maxHP = 1
    HP = 1
    ATK = 1
    MOV = 3
    
    hasMoved = 0
    isAlly = 1
    unitType = ""

    def __init__(self, maxHP, ATK, MOV, unitType):
        super().__init__()
        self.maxHP = maxHP
        self.HP = self.maxHP
        self.ATK = ATK
        self.MOV = MOV
        self.animCycle = 15
        self.unitType = unitType

    def update(self):
        super().update()
        if (self.hasMoved):
            self.animActive = False
        else:
            self.animActive = True

    def makeIntoEnemy(self):
        self.isAlly = 0
        self.images = load_images(self.unitType)
        for x in range(2):
            self.images[x] = pygame.transform.flip(self.images[x], True, False)

class Cursor(GenericAnimatedSprite):

    def __init__(self):
        super().__init__()
        self.images = load_images("cursor")
        self.animCycle = 5

class dropDownMenu(GenericAnimatedSprite):

    def __init__(self):
        super().__init__()
        self.images = load_images("dropdownmenu")

    def update(self):
        print("You should not be calling update on the dropdown menu because it is a special kind of animated sprite (it's not actually animated")
        raise Error

    def get_image(self, menuOptions: list):
        if len(menuOptions)>4:
            print("We don't support more than 4 menu options right now, more sprites would need to be made")
        menuSurface = self.images[len(menuOptions)-1].copy()
        i = 0
        for text in menuOptions:
            menuSurface.blit(getTextSurface(text, 45), (5, 16+82*i))
            i += 1
        return menuSurface

class Vampire(UnitSprite):

    def __init__(self):
        UnitSprite.__init__(self,5,3,4, "vampire")
        self.images = load_images("vampireplayer")

class Werewolf(UnitSprite):

    def __init__(self):
        UnitSprite.__init__(self,5,8,2, "werewolf")
        self.images = load_images("werewolfplayer")

class Mummy(UnitSprite):
    
    def __init__(self):
        super().__init__(10, 2, 3, "mummy")
        self.images = load_images("mummyplayer")

class Earth(GenericResizedAnimatedSprite):

    def __init__(self):
        self.images = resize_load_images("Earth")
        self.animCycle = 60

class Rad(GenericResizedAnimatedSprite):

    def __init__(self):
        self.images = resize_load_images("Rad")
        self.animCycle = 60


class Lightning(GenericResizedAnimatedSprite):

    def __init__(self):
        self.images = resize_load_images("lightning")

class Cliff(GenericResizedAnimatedSprite):

    def __init__(self):
        self.images = resize_load_images("cliff")
        self.animCycle = 30

class Hooded(GenericResizedAnimatedSprite):

    def __init__(self):
        self.images = resize_load_images("hooded")
        self.animCycle = 30

        