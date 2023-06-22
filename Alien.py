import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self,color,x,y,file_path):
        super().__init__()
        
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))
        
        if color == 'tier1': 
            self.value = 100
            self.life = 1
        elif color == 'tier2': 
            self.value = 200
            self.life = 2
        elif color == 'tier3': 
            self.value = 300
            self.life = 3

    def update(self,direction):
        self.rect.x += direction