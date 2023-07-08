#chicken invaders
#import pygame
import pygame, sys
import pygame_menu
#import obstacle
from random import choice, randint
#packages for computer vision
import cv2
import sqlite3
from threading import Thread
import time

#SELF MADE CODE IMPORTS
from Game import Game
from human_user import human_user
from menuOptions import menuOptions




from screeninfo import get_monitors

def gameRun(menu_options, monitor_height, monitor_width, screen):
    menu_options.menu_music.stop()
    menu_options.menu_click.play()
    
    #screen_width = 700
    
    
    player_user = human_user(monitor_width)
    
    
    cap = cv2.VideoCapture(0)

    camera_thread = Thread(target=player_user.camera, args=[cap,])
    camera_thread.start()
    
    time.sleep(2)       
    
    
    #MUDAR AQUI A FREQUENCIA DOS LASERS DOS ALIENS
    if(menu_options.difficulty == 0):
        ALIENLASER = pygame.USEREVENT + 1
        pygame.time.set_timer(ALIENLASER,800)
    elif(menu_options.difficulty == 1):
        ALIENLASER = pygame.USEREVENT + 1
        pygame.time.set_timer(ALIENLASER,500)
    elif(menu_options.difficulty == 2):
        ALIENLASER = pygame.USEREVENT + 1
        pygame.time.set_timer(ALIENLASER,250)
    else:
        ALIENLASER = pygame.USEREVENT + 1
        pygame.time.set_timer(ALIENLASER,800)
    
    camera_height = 0
    
    
    #player_user.camera_height = camera_height
    #player_user.camera_width = camera_width
    
    

    clock = pygame.time.Clock()
    
    player_user.camera_on = True
    
    #Instruction page
    instruction_page_1 = pygame_menu.Menu('Loading...', monitor_width,total_height,theme=mine_invader_theme)
    instruction_page_1.add.image("Images/instruction_image_1.png")
    instruction_page_2 = pygame_menu.Menu('Loading...', monitor_width,total_height,theme=mine_invader_theme)
    instruction_page_2.add.image("Images/instruction_image_2.png")
    instruction_page_3 = pygame_menu.Menu('Loading...', monitor_width,total_height,theme=mine_invader_theme)
    instruction_page_3.add.image("Images/instruction_image_3.png")
    instruction_page_4 = pygame_menu.Menu('Loading...', monitor_width,total_height,theme=mine_invader_theme)
    instruction_page_4.add.image("Images/instruction_image_4.png")

    for i in range(1,3):
        
        instruction_page_1.mainloop(screen,disable_loop = True)
        time.sleep(0.75)
        
        instruction_page_2.mainloop(screen,disable_loop = True)
        time.sleep(0.75)
        
        instruction_page_3.mainloop(screen,disable_loop = True)
        time.sleep(0.75)
        
        instruction_page_4.mainloop(screen,disable_loop = True)
        time.sleep(1.75)

    game = Game(screen,monitor_width,monitor_height,camera_height,menu_options.name,menu_options.difficulty,menu_options.sound)
    
    
    
    while True:
           keys = pygame.key.get_pressed()

           if keys[pygame.K_r]:
             cap.release()
             gameRun(menu_options, monitor_height,monitor_width, screen)
             
           elif keys[pygame.K_m]:
             cap.release()
             game.game_music.stop()
             menu_options.menu_music.play(loops = -1)
             menu_inicial.mainloop(screen)
             
             
           screen.fill((30,30,30))
           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   cap.release()
                   pygame.display.quit()
                   pygame.quit()
                   sys.exit()
                   
               if event.type == ALIENLASER:
                   game.alien_shoot()
   
           game.run(player_user)
           #crt.draw()

           camera_image_surface = pygame.surfarray.make_surface(cv2.cvtColor(player_user.image_mat, cv2.COLOR_BGR2RGB))
            
           camera_image_surface_rotated = pygame.transform.rotate(camera_image_surface,270)
           #screen.blit(camera_image_surface_rotated,((screen_width-camera_width)/2,0))



           pygame.display.flip()
           

           clock.tick(30)
    

def showEasyLeaderboard(leaderboard_menu):
    menu_options.menu_click.play()
    # Connect to the database
    conn = sqlite3.connect('Database/MineInvader_Leaderboard.db')

    # Create a cursor object
    c = conn.cursor()

    conn.execute('''CREATE TABLE IF NOT EXISTS leaderboard_table
                (id INTEGER PRIMARY KEY,
                name TEXT,
                score INTEGER,
                difficulty TEXT)''')

    # Select the top three scores for each difficulty level
    c.execute('''SELECT name, score FROM leaderboard_table WHERE difficulty=? ORDER BY score DESC LIMIT 10''', ('Easy',))
    easy_scores = c.fetchall()      

    # Close the database connection
    conn.close()

    # Create a new menu to display the leaderboard
    leaderboard_easy_menu = pygame_menu.Menu('Leaderboard Easy', monitor_width, total_height, theme=mine_invader_theme)

    # Add the top scores for each difficulty level to the menu
    leaderboard_easy_menu.add.label('Easy Scores:')
    for name, score in easy_scores:
        leaderboard_easy_menu.add.label(f'{name}: {score}')

    # Add a button to return to the main menu
    leaderboard_easy_menu.add.button('Back', leaderboard_menu.mainloop,screen,accept_kwargs = True)

    # Display the leaderboard menu
    leaderboard_easy_menu.mainloop(screen) 



def showMediumLeaderboard(leaderboard_menu):
    menu_options.menu_click.play()
    # Connect to the database
    conn = sqlite3.connect('Database/MineInvader_Leaderboard.db')

    # Create a cursor object
    c = conn.cursor()

    conn.execute('''CREATE TABLE IF NOT EXISTS leaderboard_table
                (id INTEGER PRIMARY KEY,
                name TEXT,
                score INTEGER,
                difficulty TEXT)''')

    # Select the top three scores for each difficulty level
    c.execute('''SELECT name, score FROM leaderboard_table WHERE difficulty=? ORDER BY score DESC LIMIT 10''', ('Medium',))
    medium_scores = c.fetchall()     

    # Close the database connection
    conn.close()

    # Create a new menu to display the leaderboard
    leaderboard_medium_menu = pygame_menu.Menu('Leaderboard Medium', monitor_width, total_height, theme=mine_invader_theme)

    # Add the top scores for each difficulty level to the menu
    leaderboard_medium_menu.add.label('Medium Scores:')
    for name, score in medium_scores:
        leaderboard_medium_menu.add.label(f'{name}: {score}')

    # Add a button to return to the main menu
    leaderboard_medium_menu.add.button('Back', leaderboard_menu.mainloop,screen,accept_kwargs = True)

    # Display the leaderboard menu
    leaderboard_medium_menu.mainloop(screen) 


def showHardLeaderboard(leaderboard_menu):
    menu_options.menu_click.play()
    # Connect to the database
    conn = sqlite3.connect('Database/MineInvader_Leaderboard.db')

    # Create a cursor object
    c = conn.cursor()

    conn.execute('''CREATE TABLE IF NOT EXISTS leaderboard_table
                (id INTEGER PRIMARY KEY,
                name TEXT,
                score INTEGER,
                difficulty TEXT)''')

    # Select the top three scores for each difficulty level
    c.execute('''SELECT name, score FROM leaderboard_table WHERE difficulty=? ORDER BY score DESC LIMIT 10''', ('Hard',))
    hard_scores = c.fetchall()    

    # Close the database connection
    conn.close()

    # Create a new menu to display the leaderboard
    leaderboard_hard_menu = pygame_menu.Menu('Leaderboard Hard', monitor_width, total_height, theme=mine_invader_theme)

    # Add the top scores for each difficulty level to the menu
    leaderboard_hard_menu.add.label('Hard Scores:')
    for name, score in hard_scores:
        leaderboard_hard_menu.add.label(f'{name}: {score}')


    # Add a button to return to the main menu
    leaderboard_hard_menu.add.button('Back', leaderboard_menu.mainloop,screen,accept_kwargs = True)

    # Display the leaderboard menu
    leaderboard_hard_menu.mainloop(screen) 
          
def showLeaderboard():
    menu_options.menu_click.play()
    # Create a new menu to display the leaderboard
    leaderboard_menu = pygame_menu.Menu('Leaderboard', monitor_width, total_height, theme=mine_invader_theme)

    # Add buttons for Easy, Medium, Hard menus
    leaderboard_menu.add.button('Easy', showEasyLeaderboard,leaderboard_menu,accept_kwargs=True)
    leaderboard_menu.add.button('Medium', showMediumLeaderboard,leaderboard_menu,accept_kwargs=True)
    leaderboard_menu.add.button('Hard', showHardLeaderboard,leaderboard_menu,accept_kwargs=True)

    # Add a button to return to the main menu
    leaderboard_menu.add.button('Back', menu_inicial.mainloop,screen,accept_kwargs = True)

    # Display the leaderboard menu
    leaderboard_menu.mainloop(screen)        
          
                    
        

if __name__ == '__main__':
    pygame.init()

    #Theme Creation
    background_image = pygame_menu.BaseImage(image_path="Images/minecraft_background.png")
    font = pygame_menu.font.FONT_8BIT
    mine_invader_theme = pygame_menu.Theme(background_color = background_image,
                                           widget_font = font,
                                           widget_font_color = (0,0,0))


    
    
    all_monitor_height = []
    all_monitor_width = []
    
    for m in get_monitors():
        all_monitor_height.append(m.height)
        all_monitor_width.append(m.width)
        
    monitor_height= max(all_monitor_height)
    monitor_width= max(all_monitor_width)
    
    print(monitor_height)
    print(monitor_width)
    
    #camera_height = 450
    
    
    
    #print(monitor_height)
    total_height = monitor_height
    
    screen = pygame.display.set_mode((monitor_width,total_height),pygame.FULLSCREEN, pygame.SCALED)

    
    menu_inicial = pygame_menu.Menu('MineInvaders',monitor_width,total_height,theme=mine_invader_theme)

    menu_options = menuOptions()

    menu_inicial.add.text_input('Name  : ', default='Steve',onchange=menu_options.setName)
    menu_inicial.add.selector('Difficulty  ', [('Easy', 0), ('Medium', 1),('Hard',2)], onchange=menu_options.setDifficulty)
    menu_inicial.add.button('Play', gameRun,menu_options,monitor_height,monitor_width,screen,accept_kwargs=True)
    menu_inicial.add.button('Leaderboard', showLeaderboard)
    menu_inicial.add.selector('Sound ', [('ON',True),('OFF',False)],onchange=menu_options.setSound)
    menu_inicial.add.button('Quit', pygame_menu.events.EXIT)

    menu_options.menu_music.play(loops = -1)
    menu_inicial.mainloop(screen)