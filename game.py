import pygame
from menu import *
import os
from projectmonstertactics import main
import spritemanager as sm


class Game():
    def __init__(self):
        pygame.init()
        #inititialize game states
        self.running, self.playing, self.scene = True, False, False
        #initialize keys
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        #Create the window
        self.DISPLAY_W, self.DISPLAY_H = 1280, 800
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))

        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0,0,0), (255,255,255)
        
        self.main_menu = MainMenu(self)
        self.curr_menu = MainMenu(self)
        self.credits = CreditsMenu(self)
        self.cut = 1
        self.clock = pygame.time.Clock()

    def opening(self):
        earth = sm.Earth()
        lightning = sm.Lightning()
        cliff = sm.Cliff()
        rad = sm.Rad()
        hooded = sm.Hooded()
        while self.scene:
            while self.cut == 1:
                self.cutscene(["THE YEAR IS 20XX AND THE EARTH IS STILL STANDING"], sprite = earth)
                self.cutscene_choice()
            self.break_cutscene()
            while self.cut == 2:
                self.cutscene(["BUT THIS STORY ISN'T ABOUT EARTH...", "AT LEAST NOT THE EARTH YOU KNOW"], sprite = None)
                self.cutscene_choice()
            self.break_cutscene()
            while self.cut == 3:
                self.cutscene(["EARTH-235 LIES IN THE WAKE OF A HORRIFIC WAVE OF RADIATION"], sprite = rad)
                self.cutscene_choice()
            self.break_cutscene()
            while self.cut == 4:
                self.cutscene(["ALL KINDS OF MONSTERS POPULATE THIS WASTELAND...", "VYING FOR POWER ON A DEVASTATED PLANET"], sprite = None)
                self.cutscene_choice()
            self.break_cutscene()
            while self.cut == 5:
                self.cutscene(["WITH HOPES OF RESTORING ORDER, YOU SET OUT TOWARDS THE BATTLEFIELD"], sprite = hooded)
                self.cutscene_choice()
            self.break_cutscene()
            while self.cut == 6:
                self.cutscene(["LEAD YOUR TROOPS AND PUT AN END TO THIS MONSTER MASH!"], sprite = cliff)
                self.cutscene_choice()
            while self.cut == 7:
                self.cutscene(["LEAD YOUR TROOPS AND PUT AN END TO THIS MONSTER MASH!"], sprite = lightning)
                self.cutscene_choice()
            if self.cut > 7:
                self.break_cutscene()
                self.scene = False
                self.playing = True

    def cutscene(self, text, sprite = None):
        self.display.fill(self.BLACK)
        if len(text) > 1:
            self.draw_text(text[0], 30, self.DISPLAY_W/2, self.DISPLAY_H/2)
            self.draw_text(text[1], 30, self.DISPLAY_W/1.9, self.DISPLAY_H/1.7)
        else:
            self.draw_text(text[0], 30, self.DISPLAY_W/2, self.DISPLAY_H/1.2)
        if sprite != None:
            self.window.blits([(self.display, (0,0)), (sprite.get_image(), (420,150))])
            sprite.update()
        else:
            self.window.blit(self.display, (0,0))
        pygame.display.flip()
        self.reset_keys()
    
    def break_cutscene(self):
        self.display.fill(self.BLACK)
        self.window.blit(self.display, (0,0))
        pygame.display.flip()
    
    def cutscene_choice(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.cut += 1
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
                pygame.quit()
                exit()
        

    def game_loop(self):
        if self.playing:
            main()
        while self.playing:
            self.check_events()
            

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
    
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)
    

    