#chicken invaders
#import pygame
import pygame
from random import choice, randint, random
import sqlite3
from threading import Thread
import time
import numpy as np


#SELF MADE CODE IMPORTS
from Alien import Alien
from Block import Block
from Extra import Extra
from Laser import Laser
from Player import Player
from Powerups import Powerups
from Ammobox import Ammobox
from Button import Button


shape = [
'  xxxxxxx',
' xxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxx     xxx',
'xx       xx']


class Game:
    def __init__(self,screen,screen_width,screen_height,camera_height,name,difficulty,sound, camera, player_user,tick):
        #Tick
        self.tick = tick
        #Screen setup
        self.screen = screen
        self.screen_width = screen_width
        self.camera = camera
        
        if self.camera:
            self.camera_height = camera_height
        else:
            self.camera_height = 0
        
        self.screen_height = screen_height - self.camera_height
        
        
        self.player_user = player_user
        
        # Player setup
        player_sprite = Player((screen_width / 2, round(0.98*self.screen_height + self.camera_height)),self.screen_width,self.screen_height, self.camera_height)

        self.player = pygame.sprite.GroupSingle(player_sprite)
        self.name = name
        
        #Difficulty setup
        self.difficulty = difficulty

        # Ammobox setup
        # Ammobox_sprite = Ammobox(random_side,screen_height + camera_height)
        self.ammobox = pygame.sprite.GroupSingle() #Ammobox_sprite
        self.ammobox_spawn_time = randint(200,300)
        self.ammobox_exists = False
        
        if(self.difficulty == 0):
            self.ammobox_timeout = 450
        elif(self.difficulty == 1):
            self.ammobox_timeout = 225
        elif(self.difficulty == 2):
            self.ammobox_timeout = 125
        else:
            self.ammobox_timeout = 450
        
        
        #Victory conditions
        self.lost = False     
        self.won = False
        self.leaderboard_path = "Database/MineInvader_Leaderboard.db"
        self.leaderboard_to_save = True


        # health and score setup
        self.lasers_quiver = self.player.sprite.lasers_quiver
        
        if (self.screen_width/1920 < self.screen_height/1080):

            self.lasers_surf = pygame.transform.scale(pygame.image.load('Images/quiver.png').convert_alpha(),(round(50*self.screen_width/1920),round(50*self.screen_width/1920)))
            #self.no_lasers_surf = pygame.transform.scale(pygame.image.load('Images/no_arrows_quiver.png').convert_alpha(),(round(55*self.screen_width/1920),round(55*self.screen_width/1920)))
            #self.red_frame_surf = pygame.transform.scale(pygame.image.load('Images/red_frame.png').convert_alpha(),(round(200*self.screen_width/1920),round(90*self.screen_width/1920)))
        else:
            self.lasers_surf = pygame.transform.scale(pygame.image.load('Images/quiver.png').convert_alpha(),(round(50*self.screen_height/1080),round(50*self.screen_height/1080)))
            #self.no_lasers_surf = pygame.transform.scale(pygame.image.load('Images/no_arrows_quiver.png').convert_alpha(),(round(55*self.screen_height/1080),round(55*self.screen_height/1080)))
            #self.red_frame_surf = pygame.transform.scale(pygame.image.load('Images/red_frame.png').convert_alpha(),(round(200*self.screen_width/1080),round(90*self.screen_width/1080)))

            
        self.lives = 3
        
        if (self.screen_width/1920 < self.screen_height/1080):
            self.live_surf = pygame.transform.scale(pygame.image.load('Images/heart.png').convert_alpha(),(round(45*self.screen_width/1920),round(45*self.screen_width/1920)))
        else:
            self.live_surf = pygame.transform.scale(pygame.image.load('Images/heart.png').convert_alpha(),(round(45*self.screen_height/1080),round(45*self.screen_height/1080)))
            
        
        self.live_x_start_pos = screen_width - round(48*self.screen_width/1920)
        self.score = 0
        
        
        if (self.screen_width/1920 < self.screen_height/1080):
            self.font = pygame.font.Font('Font/Pixeled.ttf',int(round(32*self.screen_width/1920)))
        else:
            self.font = pygame.font.Font('Font/Pixeled.ttf',int(round(32*self.screen_height/1080)))
        
            
        # Obstacle setup
        self.shape = shape
        
        if (self.screen_width/1920 < self.screen_height/1080):
            self.block_size = round(10*self.screen_width/1920)
        else:
            self.block_size = round(10*self.screen_height/1080)
            
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (screen_width / self.obstacle_amount + (48*self.screen_width/1920)) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_positions, x_start = round(screen_width / (16*self.screen_width/1920)), y_start = round(750*self.screen_height/1080) + self.camera_height)

        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        if(self.difficulty == 0):
            self.alien_direction = 3*round(self.screen_width/1920) 
            self.alien_lasers_speed = 8 * round(screen_width/1920)
        elif(self.difficulty == 1):
            self.alien_direction = 6*round(self.screen_width/1920)
            self.alien_lasers_speed = 9 * round(screen_width/1920) 
        elif(self.difficulty == 2):
            self.alien_direction = 9*round(self.screen_width/1920) 
            self.alien_lasers_speed = 10 * round(screen_width/1920)
        else:
            self.alien_direction = 3*round(self.screen_width/1920)  
            self.alien_lasers_speed = 8 * round(screen_width/1920)

        # Drops
        self.powerups = pygame.sprite.Group()

        # Extra setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(40,80)

        # Audio
        self.sound = sound
        
        self.ammobox_sound = pygame.mixer.Sound('Sounds/quiver_pickup.wav')
        self.ammobox_sound.set_volume(0.5)

        self.game_music = pygame.mixer.Sound('Sounds/otherside.wav')
        self.game_music.set_volume(0.1)
        self.game_music.play(loops = -1)

        self.eat_sound = pygame.mixer.Sound('Sounds/minecraft_eating_sound_effect.wav')
        self.eat_sound.set_volume(0.3)
        self.drink_sound = pygame.mixer.Sound('Sounds/minecraft_drinking_sound_effect.wav')
        self.drink_sound.set_volume(0.3)

        self.laser_sound = pygame.mixer.Sound('Sounds/bow.wav')
        self.laser_sound.set_volume(0.08)
        if(self.difficulty == 0):
            self.tier3_sound = pygame.mixer.Sound('Sounds/chicken_death.wav')
            self.tier3_sound.set_volume(0.3)
            
            self.tier2_sound = pygame.mixer.Sound('Sounds/pig_death.wav')
            self.tier2_sound.set_volume(0.3)
            
            self.tier1_sound = pygame.mixer.Sound('Sounds/sheep_death.wav')
            self.tier1_sound.set_volume(0.3)
        elif(self.difficulty == 1):
            self.tier3_sound = pygame.mixer.Sound('Sounds/zombie_death.wav')
            self.tier3_sound.set_volume(0.3)
            
            self.tier2_sound = pygame.mixer.Sound('Sounds/spider_death.wav')
            self.tier2_sound.set_volume(0.3)
            
            self.tier1_sound = pygame.mixer.Sound('Sounds/slime_death.wav')
            self.tier1_sound.set_volume(0.3)
        elif(self.difficulty == 2):
            self.tier3_sound = pygame.mixer.Sound('Sounds/blaze_death.wav')
            self.tier3_sound.set_volume(0.3)
            
            self.tier2_sound = pygame.mixer.Sound('Sounds/skeleton_death.wav')
            self.tier2_sound.set_volume(0.3)
            
            self.tier1_sound = pygame.mixer.Sound('Sounds/creeper_death.wav')
            self.tier1_sound.set_volume(0.3)
        else:
            self.tier3_sound = pygame.mixer.Sound('Sounds/chicken_death.wav')
            self.tier3_sound.set_volume(0.3)
            
            self.tier2_sound = pygame.mixer.Sound('Sounds/pig_death.wav')
            self.tier2_sound.set_volume(0.3)
            
            self.tier1_sound = pygame.mixer.Sound('Sounds/sheep_death.wav')
            self.tier1_sound.set_volume(0.3)

        self.player_hurt = pygame.mixer.Sound('Sounds/steve_hurt.wav')
        self.player_hurt.set_volume(0.3)
        
        self.dragon_sound = pygame.mixer.Sound('Sounds/dragon_death.wav')
        self.dragon_sound.set_volume(0.2)

        #If False, MUTE THE SOUND
        if(self.sound == False):
            self.game_music.set_volume(0)
            self.eat_sound.set_volume(0)
            self.ammobox_sound.set_volume(0)
            self.drink_sound.set_volume(0)
            self.laser_sound.set_volume(0)
            self.tier3_sound.set_volume(0)
            self.tier2_sound.set_volume(0)
            self.tier1_sound.set_volume(0)
            self.player_hurt.set_volume(0)
            self.dragon_sound.set_volume(0)
            self.player.sprite.muteSound()


    def create_obstacle(self, x_start, y_start,offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index,col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    if row_index == 0:
                        #green
                        block = Block(self.block_size,(0,128,0),x,y)
                    elif row_index == 1:
                        #brown
                        block = Block(self.block_size,(139,69,19),x,y)
                    else:
                        #grey
                        block = Block(self.block_size,(128,128,128),x,y)
                        #block = Block(self.block_size,(241,79,80),x,y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self,*offset,x_start,y_start):
        for offset_x in offset:
            self.create_obstacle(x_start,y_start,offset_x)

    def alien_setup(self,rows,cols):
        
        x_distance = 120 * self.screen_width/1920
        y_distance = 70 * self.screen_height/1080
        x_offset = 80 * self.screen_width/1920
        y_offset = 150 * self.screen_height/1080
        
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * (y_distance) + y_offset
                if(self.difficulty == 0):
                    if row_index == 0: alien_sprite = Alien('tier3',x,y,"Images/chicken.png", self.screen_height, self.screen_width, self.camera_height)
                    elif 1 <= row_index <= 2: alien_sprite = Alien('tier2',x,y,"Images/pig.png", self.screen_height, self.screen_width, self.camera_height)
                    else: alien_sprite = Alien('tier1',x,y,"Images/sheep.png", self.screen_height, self.screen_width, self.camera_height)
                    self.aliens.add(alien_sprite)
                elif(self.difficulty == 1):
                    if row_index == 0: alien_sprite = Alien('tier3',x,y,"Images/zombie.png", self.screen_height, self.screen_width, self.camera_height)
                    elif 1 <= row_index <= 2: alien_sprite = Alien('tier2',x,y,"Images/spider.png", self.screen_height, self.screen_width, self.camera_height)
                    else: alien_sprite = Alien('tier1',x,y,"Images/slime.png", self.screen_height, self.screen_width, self.camera_height)
                    self.aliens.add(alien_sprite)
                elif(self.difficulty == 2):
                    if row_index == 0: alien_sprite = Alien('tier3',x,y,"Images/blaze.png", self.screen_height, self.screen_width, self.camera_height)
                    elif 1 <= row_index <= 2: alien_sprite = Alien('tier2',x,y,"Images/skeleton.png", self.screen_height, self.screen_width, self.camera_height)
                    else: alien_sprite = Alien('tier1',x,y,"Images/creeper.png", self.screen_height, self.screen_width, self.camera_height)
                    self.aliens.add(alien_sprite)
                else:
                    if row_index == 0: alien_sprite = Alien('tier3',x,y,"Images/sheep.png", self.screen_height, self.screen_width, self.camera_height)
                    elif 1 <= row_index <= 2: alien_sprite = Alien('tier2',x,y,"Images/pig.png", self.screen_height, self.screen_width, self.camera_height)
                    else: alien_sprite = Alien('tier1',x,y,"Images/chicken.png", self.screen_height, self.screen_width, self.camera_height)
                    self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= self.screen_width:
                if(self.difficulty == 0):
                    self.alien_direction = -3*round(self.screen_width/1920)
                    self.alien_move_down(round(4*self.screen_height/1080))
                elif(self.difficulty == 1):
                    self.alien_direction = -6*round(self.screen_width/1920)
                    self.alien_move_down(round(5*self.screen_height/1080))
                elif(self.difficulty == 2):
                    self.alien_direction = -8*round(self.screen_width/1920)
                    self.alien_move_down(round(4*self.screen_height/1080))
                else:
                    self.alien_direction = -1
                    self.alien_move_down(round(4*self.screen_height/1080))
            elif alien.rect.left <= 0:
                if(self.difficulty == 0):
                    self.alien_direction = 3*round(self.screen_width/1920)
                    self.alien_move_down(round(5*self.screen_height/1080))
                elif(self.difficulty == 1):
                    self.alien_direction = 6*round(self.screen_width/1920)
                    self.alien_move_down(round(4*self.screen_height/1080))
                elif(self.difficulty == 2):
                    self.alien_direction = 8*round(self.screen_width/1920)
                    self.alien_move_down(round(4*self.screen_height/1080))
                else:
                    self.alien_direction = 1
                    self.alien_move_down(round(4*self.screen_height/1080))

    def alien_move_down(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def get_all_X(self):
        all_aliens = self.aliens.sprites()
        X = []
        for alien in all_aliens:
            if alien.rect.x not in X:
                X.append(alien.rect.x)
        return X
    
    def alien_shoot(self):
        columns = self.get_all_X()
        all_aliens = self.aliens.sprites()
        number_aliens = len(all_aliens)
        bottom_aliens = []

        sublists = [[alien for alien in all_aliens if alien.rect.x == col] for col in columns]

        for sublist in sublists: 
            sublist.sort(reverse = True, key=get_y)
            bottom_aliens.append(sublist[0])

        #Chance to shoot
        if(self.tick.getTick() >600):
            shooting_chance = round(-0.0069*number_aliens + 1,2)
            rd_number = random()
            if bottom_aliens and shooting_chance > rd_number:
                #Choose the alien to shoot, using a gaussian
                alien_pos_x = [0]
                player_pos_x = self.player.sprite.rect.center[0]/self.screen_width
                player_pos_section = 0
                for alien in bottom_aliens:
                    alien_pos_x.append(alien.rect.center[0]/self.screen_width)

                alien_pos_x.append(1)
                for section in range(0,len(alien_pos_x)-1):
                    if(player_pos_x >= alien_pos_x[section] and player_pos_x < alien_pos_x[section + 1]):
                        player_pos_section = section            
                
                distribution = np.random.normal(player_pos_section,1)
                clipped_distribution = np.clip(distribution,0,len(bottom_aliens) - 1)
                random_choice = int(round(clipped_distribution))
                random_alien = bottom_aliens[random_choice]
                laser_sprite = Laser(random_alien.rect.center,self.alien_lasers_speed,self.screen_height, self.screen_width, self.camera_height)

                laser_sprite.image = pygame.transform.flip(laser_sprite.image, False, True)
                self.alien_lasers.add(laser_sprite)
                self.laser_sound.play()

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0 and not self.won and not self.lost:
            if(self.difficulty == 0):
                self.extra.add(Extra(choice(["right","left"]), 0.8, self.screen_width,self.camera_height, self.screen_height))
            elif(self.difficulty == 1):
                self.extra.add(Extra(choice(["right","left"]), 1.5, self.screen_width,self.camera_height, self.screen_height))
            elif(self.difficulty == 2):
                self.extra.add(Extra(choice(["right","left"]), 2, self.screen_width,self.camera_height, self.screen_height))
            else:
                self.ammobox_timeout = 100
            
            self.extra_spawn_time = randint(round((self.screen_width+100)/ round((0.8 * 3 * self.screen_width/1920))),round((self.screen_width+100)/ round((0.8 * 3 * self.screen_width/1920)) + 200))
    
    def ammobox_timer(self):
        self.ammobox_spawn_time -= 1
        if self.ammobox_spawn_time <= 0 and not self.won:
            self.ammobox.add(Ammobox(round(0.98*self.screen_height + self.camera_height),self.screen_width,self.camera_height,self.screen_height, self.player_user))
            self.ammobox_spawn_time = randint(700,1000)
            
            self.ammobox_exists = True
            
        if self.ammobox_exists:
            self.ammobox_timeout -= 1
            if self.ammobox_timeout <= 0 and not self.won:
                self.ammobox_exists = False
                
                if(self.difficulty == 0):
                    self.ammobox_timeout = 450
                elif(self.difficulty == 1):
                    self.ammobox_timeout = 225
                elif(self.difficulty == 2):
                    self.ammobox_timeout = 125
                else:
                    self.ammobox_timeout = 450
                    
                for box in self.ammobox:
                    box.kill()
            
    def collision_checks(self):

        # player lasers 
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                    

                # alien collisions
                aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,False)
                if aliens_hit:
                    for alien in aliens_hit:
                        #check for kill
                        alien.life = alien.life - 1
                        if(alien.life <= 0):

                            Rnum = randint(0,100)
                            if(self.difficulty == 0):
                                if Rnum <= 12:
                                    powerup = Powerups(alien.rect.center,5,self.screen_height, self.screen_width, self.camera_height)
                                    self.powerups.add(powerup)
                            if(self.difficulty == 1):
                                if Rnum <= 7:
                                    powerup = Powerups(alien.rect.center,5,self.screen_height, self.screen_width, self.camera_height)
                                    self.powerups.add(powerup)
                            if(self.difficulty == 3):
                                if Rnum <= 5:
                                    powerup = Powerups(alien.rect.center,5,self.screen_height, self.screen_width, self.camera_height)
                                    self.powerups.add(powerup)


                            self.score += alien.value
                            if alien.value == 100:
                                self.tier1_sound.play()
                            elif alien.value == 200:
                                self.tier2_sound.play()
                            else:
                                self.tier3_sound.play()
                            alien.kill()
                    laser.kill()

                # extra collision
                if pygame.sprite.spritecollide(laser,self.extra,False):
                    self.score += 500
                    self.dragon_sound.play()         
                    laser.kill()
                    powerup = Powerups(self.extra.sprite.rect.center,5,self.screen_height,self.screen_width, self.camera_height)
                    self.extra.sprite.kill()
                    self.powerups.add(powerup)
                    

        # alien lasers 
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    self.lives -= 1
                    self.player_hurt.play()
                    if self.lives <= 0 and not self.won:
                        # pygame.quit()
                        # sys.exit()
                        self.lost = True

        #Powerups
        if(self.powerups):
            for powerup in self.powerups:
                if pygame.sprite.spritecollide(powerup,self.player,False):
                    if(powerup.name == "plus_1_life"):
                        powerup.kill()
                        self.eat_sound.play()
                        if self.lives < 5:
                            self.lives +=1
                        elif self.lives >= 5:
                            self.score += 300
                            
                    elif(powerup.name == "plus_1_arrow"):
                        powerup.kill()
                        self.drink_sound.play()
                        if(self.player.sprite.number_lasers < 3):
                            self.player.sprite.number_lasers += 1
                        elif (self.player.sprite.number_lasers >= 3):
                            self.score += 300
                            
                            
                    elif(powerup.name == "slow_alien_lasers"):
                        powerup.kill()
                        self.drink_sound.play()
                        if(self.alien_lasers_speed > 5*self.screen_height/1080):
                            self.alien_lasers_speed -=2*self.screen_height/1080
                            #Thread(target = self.alien_laser_speed_timer).start()
                        else:
                            #self.alien_lasers_speed = 4
                            self.score += 300
                            #Thread(target = self.alien_laser_speed_timer).start()
        # ammo
        if(self.ammobox):
            for box in self.ammobox:
                if pygame.sprite.spritecollide(box, self.player, False):
                    box.kill()
                    self.player.sprite.lasers_quiver += 12
                    self.ammobox_sound.play()

                        
        # aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)

                if pygame.sprite.spritecollide(alien,self.player,False) and not self.won:
                    # pygame.quit()
                    # sys.exit()
                    self.lost = True
    
    def display_lives(self):
        for live in range(self.lives):
            x = self.live_x_start_pos - (live * round((self.live_surf.get_size()[0]*1.5 - 5)*self.screen_width/1920))
            self.screen.blit(self.live_surf,(x,round(10*self.screen_height/1080) + self.camera_height))
    
    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}',False,'white')
        score_rect = score_surf.get_rect(midtop = (round(960*self.screen_width/1920),round(-10*self.screen_height/1080) + self.camera_height))
        self.screen.blit(score_surf,score_rect)

    def display_lasers(self):
        laser_rect = self.lasers_surf.get_rect(topleft = (round(10*self.screen_width/1920),round(10*self.screen_height/1080) + self.camera_height))
        self.screen.blit(self.lasers_surf,laser_rect)
        if(self.lasers_quiver > 0):
            lasers_surf = self.font.render(f'x {self.lasers_quiver}',False,'white')
            laser_rect = lasers_surf.get_rect(topleft = (round(65*self.screen_width/1920),round(-10*self.screen_height/1080) + self.camera_height))
            self.screen.blit(lasers_surf,laser_rect)
        else:
            lasers_surf = self.font.render(f'x {self.lasers_quiver}',False,'red')
            laser_rect = lasers_surf.get_rect(topleft = (round(65*self.screen_width/1920),round(-10*self.screen_height/1080) + self.camera_height))
            self.screen.blit(lasers_surf,laser_rect)
            #frame_rect = self.red_frame_surf.get_rect(topleft = (round(-80*self.screen_width/1920),round(-70*self.screen_height/1080) + self.camera_height))
            #self.screen.blit(self.red_frame_surf,frame_rect)
            #laser_rect = self.no_lasers_surf.get_rect(topleft = (round(10*self.screen_width/1920),round(10*self.screen_height/1080) + self.camera_height))
            #self.screen.blit(self.no_lasers_surf,laser_rect)
            """laser_rect = self.lasers_surf.get_rect(topleft = (round(10*self.screen_width/1920),round(10*self.screen_height/1080) + self.camera_height))
            self.screen.blit(self.lasers_surf,laser_rect)
            no_lasers_surf = self.font.render(f'x {self.lasers_quiver}',False,'red')
            laser_rect = no_lasers_surf.get_rect(topleft = (round(65*self.screen_width/1920),round(-10*self.screen_height/1080) + self.camera_height))
            self.screen.blit(no_lasers_surf,laser_rect)
            #print(laser_rect)"""
        self.lasers_quiver = self.player.sprite.lasers_quiver
    
    
    def victory_message(self):
        if not self.aliens.sprites() and not self.lost:
            if(self.extra):
                for dragon in self.extra:
                    dragon.kill()

            if(self.difficulty == 0):
                diff_string="Easy"
            elif(self.difficulty == 1):
                diff_string="Medium"
            elif(self.difficulty == 2):
                diff_string="Hard"
            else:
                diff_string="ERROR"

            victory_surf = self.font.render('Name: ' + self.name, False ,'white')
            victory_rect = victory_surf.get_rect(center = (self.screen_width / 2, self.screen_height / 2 + self.camera_height - 170*self.screen_height/1080))
            self.screen.blit(victory_surf,victory_rect)

            victory_surf = self.font.render('Score: ' + str(self.score) + '; Difficulty: ' + diff_string,False,'white')
            victory_rect = victory_surf.get_rect(center = (self.screen_width / 2, self.screen_height / 2 + self.camera_height - 120*self.screen_height/1080))
            self.screen.blit(victory_surf,victory_rect)

            victory_surf = self.font.render('YOU WON',False,'white')
            victory_rect = victory_surf.get_rect(center = (self.screen_width / 2, self.screen_height / 2 + self.camera_height - 60*self.screen_height/1080))
            self.screen.blit(victory_surf,victory_rect)

            self.won = True
            self.game_music.stop()
    
    def leaderboardSave(self):
        if(self.leaderboard_to_save and self.won):
            conn = sqlite3.connect(self.leaderboard_path)
            conn.execute('''CREATE TABLE IF NOT EXISTS leaderboard_table
                (id INTEGER PRIMARY KEY,
                name TEXT,
                score INTEGER,
                difficulty TEXT)''')
            if(self.difficulty == 0):
                diff_string="Easy"
            elif(self.difficulty == 1):
                diff_string="Medium"
            elif(self.difficulty == 2):
                diff_string="Hard"
            else:
                diff_string="ERROR"

            conn.execute("INSERT INTO leaderboard_table (name,score,difficulty) VALUES (?,?,?)",(self.name,self.score,diff_string))
            conn.commit()
            conn.close()
            self.leaderboard_to_save = False
            
            
    def lose_message(self):
        if(self.lost and not self.won):
            self.game_music.stop()
            lose_surf = self.font.render('YOU LOST',False,'white')
            lose_rect = lose_surf.get_rect(center = (self.screen_width/2, self.screen_height / 2 + self.camera_height - 30*self.screen_height/1080))
            self.screen.blit(lose_surf,lose_rect)

            if self.aliens:
                for alien in self.aliens:
                    alien.kill()
    
    # def alien_laser_speed_timer(self):
    #     time.sleep(10)
    #     self.alien_lasers_speed +=2*self.screen_height/1080
    
    
    def run(self, user):
        self.player.update(user)
        self.alien_lasers.update()
        self.powerups.update()
        self.extra.update()
        self.ammobox.update()
        
        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.extra_alien_timer()
        self.ammobox_timer()
        self.collision_checks()
        
        self.player.sprite.lasers.draw(self.screen)
        self.player.draw(self.screen)
        self.blocks.draw(self.screen)
        self.aliens.draw(self.screen)
        self.ammobox.draw(self.screen)
        self.alien_lasers.draw(self.screen)
        self.powerups.draw(self.screen)
        
        if not self.won and not self.lost:
            self.extra.draw(self.screen)
        self.display_lives()
        self.display_score()
        self.display_lasers()
        self.victory_message()
        self.lose_message()
        self.leaderboardSave()

def get_y(alien):
    return alien.rect.y