import pygame
import platform
import pyautogui


class menuOptions():

    def __init__(self):
        self.name = "Steve"
        self.difficulty = 0
        self.menu_music = pygame.mixer.Sound('Sounds/menu.wav')
        self.menu_music.set_volume(0.1)
        self.sound = True
        self.camera = True
        self.keyboard_visible = False
        
        self.menu_click = pygame.mixer.Sound('Sounds/minecraft_click.wav')
        self.menu_click.set_volume(0.1)

    def setDifficulty(self,value, difficulty):
        self.difficulty = difficulty
        self.menu_click.play()

    def setName (self,name):
        self.name = name
    
    def setSound (self,value,sound):
        self.sound =sound
        if(self.sound):
            self.menu_music.set_volume(0.1)
            self.menu_click.set_volume(0.1)
        elif(self.sound == False):
            self.menu_music.set_volume(0)
            self.menu_click.set_volume(0)
    
    def setCamera (self,value,camera):
        self.camera = camera
        
    def setKeyboard(self,value, keyboard):
        self.keyboard_visible = keyboard
        system = platform.system()
        
        if system == 'Windows':
            pyautogui.hotkey('win', 'ctrl', 'o')
        elif system == 'Darwin':  # macOS
            pyautogui.hotkey('command', 'control', 'o')
        elif system == 'Linux':
            pyautogui.hotkey('ctrl', 'o')
        #print(self.keyboard_visible)
    """
    def toggleKeyboard(self):
        if self.keyboard_visible:
            self.keyboard_visible = False
        else:
            self.keyboard_visible = True"""
