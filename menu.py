import pygame
from pygame import mixer
from pygame import mouse

def play_music ():
    mixer.init()
    song = "music_title.mp3"
    mixer.music.load(song)
    mixer.music.play()
    mixer.music.set_volume(0.3)

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0,0,20,20)
        self.offset = -150
        play_music()

    
    def draw_cursor(self):
        cursor = pygame.transform.scale(pygame.image.load("menuarrow.png").convert_alpha(), (50,50))
        self.game.display.blit(cursor, (self.cursor_rect.x , self.cursor_rect.y+72))

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 70
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 110
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            title = pygame.image.load("Title.png").convert_alpha()
            background = pygame.image.load("backgroundtitle.png").convert_alpha()
            new_title = pygame.transform.scale(title, (1000,500))
            new_background = pygame.transform.scale(background, (1280,815))
            self.game.display.blit(new_background, (0,0))
            self.game.display.blit(new_title, (145,5))
            self.game.draw_text('Start Game', 40, self.startx, 530)
            self.game.draw_text('Options', 40, self.optionsx, 570)
            self.game.draw_text('Credits', 40, self.creditsx, 610)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            else:
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
        if self.game.UP_KEY:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
    
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Start":
                self.game.scene = True
            elif self.state == "Options":
                self.game.curr_menu = self.game.options
            else:
                self.game.curr_menu = self.game.credits
            self.run_display = False
        if self.game.MOUSE_BUTTON:
                x = pygame.mouse.get_pos()
                print(x[1])
                if 410 < x[1] < 445:
                    self.game.scene = True
                elif 458 < x[1] < 480:
                    self.game.curr_menu = self.game.options
                elif 500 < x[1] < 523:
                    self.game.curr_menu = self.game.credits
                self.run_display = False
                
                
    
class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 80
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Options', 70, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 300)
            self.game.draw_text('Volume', 30, self.volx, self.voly)
            self.game.draw_text('Controls', 30, self.controlsx, self.controlsy)
            self.game.draw_text('Press ESC to Return to Main Menu', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 320)
            self.draw_cursor()
            self.blit_screen()
    
    def check_input(self):
        if self.game.ESC_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            pass



class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.ESC_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 70, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Made by OuterRim, Pepsi, and Speedspace', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 40)
            self.game.draw_text('Press Enter to Return to Main Menu', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 320)
            self.blit_screen()


