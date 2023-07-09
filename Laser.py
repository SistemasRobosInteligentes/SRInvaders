import pygame
        
class Laser(pygame.sprite.Sprite):
    def __init__(self,pos,speed,screen_height, screen_width, camera_height):
        super().__init__()
        """self.image = pygame.Surface((4,20))
        arrow_shape = [
        'sggs',
        'sggs',
        'gggg',
        'gbbg',
        'gbbg',
        'sbbs',
        'sbbs',
        'sbbs',
        'sbbs',
        'sbbs',
        'sbbs',
        'sbbs',
        'sbbs',
        'sbbs',
        'sbbs',
        'sggs',
        'sggs',
        'gggg',
        'gssg',
        'gssg']
        COLORS = {'g' : (128,128,128),
                  'b' : (139,69,19),
                  's' : (0,0,0)}

        for i in range(len(arrow_shape)):
            for j in range(len(arrow_shape[i])):
                if COLORS[arrow_shape[i][j]] == 's':
                    continue
                
                color = COLORS[arrow_shape[i][j]]
                rect = pygame.Rect(j, i, 1, 1)
                pygame.draw.rect(self.image, color, rect)
        """
        
        self.screen_height = screen_height    
        self.screen_width = screen_width
        self.camera_height = camera_height
        
        if (self.screen_width/1920 < self.screen_height/1080):
            self.image = pygame.transform.scale(pygame.image.load('Images/arrow.png').convert_alpha(),(round(20*self.screen_width/1920),round(20*self.screen_width/1920)))
        else:
            self.image = pygame.transform.scale(pygame.image.load('Images/arrow.png').convert_alpha(),(round(20*self.screen_height/1080),round(20*self.screen_height/1080)))
        
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        

    def destroy(self):
        if self.rect.y <= -50 + self.camera_height or self.rect.y >= self.screen_height + self.camera_height + 50:
            self.kill()

    def update(self):
        self.rect.y += round(self.speed*self.screen_height/1080)
        self.destroy()
