import pygame


class menuOptions():

    def __init__(self):
        self.name = "Steve"
        self.difficulty = 0
        self.menu_music = pygame.mixer.Sound('menu.wav')
        self.menu_music.set_volume(0.1)

        self.menu_click = pygame.mixer.Sound('minecraft_click.wav')
        self.menu_click.set_volume(0.1)

    def setDifficulty(self,value, difficulty):
        self.difficulty = difficulty
        self.menu_click.play()

    def setName (self,name):
        self.name = name