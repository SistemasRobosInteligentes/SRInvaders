import pygame
import pygame.gfxdraw



class Button(pygame.sprite.Sprite):

    def __init__(self, position, text,size,buttons,screen, 
                 colors="white on black", hover_colors="black on white", style=1, borderc=(255,255,255), command=lambda: print("No command activated for this button")):
        # the hover_colors attribute needs to be fixed
        super().__init__()

        self.screen = screen
        self.size = size
        self.text = text
        self.command = command
        # --- colors ---
        self.colors = colors
        self.original_colors = colors
        self.fg, self.bg = self.colors.split(" on ")
        
        if hover_colors == "black on white":
            self.hover_colors = f"{self.bg} on {self.fg}"
        else:
            self.hover_colors = hover_colors
        
        self.style = style
        self.borderc = borderc # for the style2
        # font
        self.font = pygame.font.Font('Font/Pixeled.ttf',self.size)
        self.render()
        self.x, self.y, self.w , self.h = self.text_render.get_rect()
        self.x, self.y = position
        self.w = self.w * 2
        self.h = self.h * 2



        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.position = position
        self.pressed = 1
        buttons.add(self)

    def render(self):
        self.text_render = self.font.render(self.text, 1, self.fg)
        self.image = self.text_render

    def update(self,cap,menu_options, monitor_height,monitor_width, screen,game,gameRun,menu_inicial, camera_height):
        self.fg, self.bg = self.colors.split(" on ")
        if self.style == 1:
            self.draw_button1()
        elif self.style == 2:
            self.draw_button2()
        self.hover()
        self.click(cap,menu_options, monitor_height,monitor_width, screen,game,gameRun,menu_inicial, camera_height)

    def draw_button1(self):
        ''' draws 4 lines around the button and the background '''
        # TOP LINE
        pygame.draw.line(self.screen, (150,150,150), (self.x - self.w/4 , self.y- self.h/4), (self.x + 3*self.w/4 , self.y- self.h/4), 10)

        #LEFT LINE
        pygame.draw.line(self.screen, (150,150,150), (self.x - self.w/4, self.y - self.h/4), (self.x - self.w/4 , self.y + 3*self.h/4), 10)


        #DOWN LINE
        pygame.draw.line(self.screen, (150,150,150), (self.x - self.w/4, self.y + 3*self.h/4), (self.x + 3*self.w/4 , self.y + 3*self.h/4), 10)

        #RIGHT LINE
        pygame.draw.line(self.screen, (150,150,150), (self.x + 3*self.w/4, self.y - self.h/4), [self.x + 3*self.w/4 , self.y + 3*self.h/4], 10)


        # background of the button
        pygame.draw.rect(self.screen, self.bg, (self.x - self.w/4, self.y - self.h/4, self.w , self.h))  

    def hover(self):
        ''' checks if the mouse is over the button and changes the color if it is true '''
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            # you can change the colors when the pointer is on the button if you want
            self.colors = self.hover_colors
            # pygame.mouse.set_cursor(*pygame.cursors.diamond)
        else:
            self.colors = self.original_colors
            
        self.render()

    def restart(game,cap,menu_options, monitor_height,monitor_width, screen,gameRun,menu_inicial, camera_height):
        cap.release()
        gameRun(menu_options, monitor_height,monitor_width, screen, camera_height)

    def menu(game,cap,menu_options, monitor_height,monitor_width, screen,gameRun,menu_inicial, camera_height):
        cap.release()
        game.game_music.stop()
        menu_options.menu_music.play(loops = -1)
        menu_inicial.mainloop(screen)

    def click(self,cap,menu_options, monitor_height,monitor_width, screen,game,gameRun,menu_inicial, camera_height):
        ''' checks if you click on the button and makes the call to the action just one time'''
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and self.pressed == 1:
                print("Executing code for button '" + self.text + "'")
                self.command(game,cap,menu_options, monitor_height,monitor_width, screen,gameRun,menu_inicial, camera_height)
                self.pressed = 0
                  
            if pygame.mouse.get_pressed() == (0,0,0):
                self.pressed = 1


       