import pygame


class menuOptions():

    def __init__(self):
        self.name = "Steve"
        self.difficulty = 0
        self.menu_music = pygame.mixer.Sound('Sounds/menu.wav')
        self.menu_music.set_volume(0.1)
        self.sound = True
        self.camera = True
        
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
    