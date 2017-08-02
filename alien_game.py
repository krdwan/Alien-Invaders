import sys
import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from star import Star
from game_stats import GameStats
from button import Button
#from alien import Alien
import game_functions as gf
from scoreboard import Scoreboard

def run_game():
    #initialize game and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    #set the background color
    bg_color = (230,230,230)

    #create Play button (start button)
    play_button = Button(ai_settings,screen,"Play")

    #create stats
    stats = GameStats(ai_settings)

    #make a ship
    ship = Ship(ai_settings,screen)

    #make a single star
    star = Star(ai_settings,screen)

    #make an instance of the scoreboard
    sb = Scoreboard(ai_settings,screen,stats)

    #make a group to store bullets and a group for aliens
    bullets = Group()
    aliens = Group()
    stars = Group()
    
    gf.create_fleet(ai_settings,screen,ship,aliens)
    gf.create_stars(ai_settings,screen,stars)
    
    #Start the main loop for the game.
    
    while True:
        #Watch for keyboard and mouse events.

        gf.check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)

        if stats.game_active:	
        	ship.update()
        	gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
        	gf.update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets)

        #redraw the screen during each pass through the loop.
       	gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,stars,play_button)

run_game()