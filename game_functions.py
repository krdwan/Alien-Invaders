import sys

import pygame
from bullet import Bullet
from alien import Alien
from star import Star
from random import randint
from time import sleep
from button import Button

def check_keydown_events(event,ai_settings,screen,ship,bullets):
	#respond to keypresses
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	elif event.key == pygame.K_q:
		sys.exit()


def fire_bullet(ai_settings,screen,ship,bullets):
	#fire a bullet if limit not reached yet
	if len(bullets) < ai_settings.bullets_allowed:
		#create a new bullet and add it to the bullets group
		new_bullet = Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)

def check_keyup_events(event,ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN and event.key!=pygame.K_RETURN:
			check_keydown_events(event,ai_settings,screen,ship,bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)
		elif event.type == pygame.KEYDOWN and event.key==pygame.K_RETURN:
			check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,
				play_button.rect.x,play_button.rect.y)

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
	#start a new game when the player clicks play
	button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
	if button_clicked and not stats.game_active:
		#reset the game settings
		ai_settings.initialize_dynamic_settings()

		#make mouse invisible
		pygame.mouse.set_visible(False)	
		stats.reset_status()

		stats.game_active = True

		#reset the scoreboard images
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()

		#empty the list of aliens and bullets
		aliens.empty()
		bullets.empty()

		#create a new fleet and center the ship
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()
			
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,stars,play_button):
	#update images on thes creen and flip to the new screen
	#redraw the screen during each pass through the loop

	screen.fill(ai_settings.bg_color)
	stars.draw(screen)
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	sb.show_score()

	if not stats.game_active:
		pygame.mouse.set_visible(True)
		play_button.draw_button()

		check_high_score(stats,sb)
		sb.show_score()

	#make the most recently drawn screen visible
	pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
	#update bullet positions
	bullets.update()

	#check for any bullets that have hit aliens
	#if so get rid of the bullet and the alien
	check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)

	if len(aliens) == 0:
		#destory existing bullets and create new fleet
		bullets.empty()
		ai_settings.increase_speed()

		#increase level
		stats.level += 1
		sb.prep_level()

		create_fleet(ai_settings,screen,ship,aliens)

	#get rid of extra bullets that have reached top of screen
	for bullet in bullets:
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
	collisions = pygame.sprite.groupcollide(bullets,aliens,not ai_settings.bullets_persist,True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
		sb.prep_score()

def check_high_score(stats,sb):
	if stats.score > stats.high_score:
		stats.high_score = stats.score
	stats.score = 0
	sb.prep_score()
	sb.prep_high_score()

def get_number_aliens_x(ai_settings,alien_width):
	#determine the number of aliens that fit in a row
	available_space_x = ai_settings.screen_width - 2*alien_width
	number_aliens_x = int(available_space_x / (2*alien_width))
	return number_aliens_x

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
	#create an alien and place it in the row
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2*alien_width * alien_number
	alien.rect.y=alien.rect.height + 2*alien.rect.height * row_number
	alien.rect.x = alien.x
	aliens.add(alien)

def get_number_rows(ai_settings,ship_height,alien_height):
	#determine the number of rows of aliens that fit on the screen
	available_space_y = (ai_settings.screen_height -(3*alien_height)-ship_height)
	number_rows = int(available_space_y / (2*alien_height))
	return number_rows

def create_fleet(ai_settings,screen,ship,aliens):
	#create a full fleet of aliens
	alien = Alien(ai_settings,screen) #### do we need this?
	number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

	#create the first row of aliens
	for row in xrange(number_rows):
		for alien_number in xrange(number_aliens_x):
			create_alien(ai_settings,screen,aliens,alien_number,row)

def update_aliens(ai_settings,screen,stats,sb,ship,aliens,bullets):
	#update the positions of all aliens in the fleet
	check_fleet_edges(ai_settings,aliens)
	aliens.update()

	#look for alien-ship colliions
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)

	check_aliens_bottom(ai_settings,stats,screen,sb,ship,aliens,bullets)

def ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets):
	#respond to ship being hit by alien
	
	if stats.ships_left > 0:
		#decrement ships left
		stats.ships_left -= 1

		#update the scoreboard
		sb.prep_ships()

		#empty the list of aliens and bullets
		aliens.empty()
		bullets.empty()

		#create a new fleet and center the ship
		create_fleet(ai_settings,screen,ship,aliens)
		ship.center_ship()

		#pause
		sleep(0.5)
	else:
		stats.game_active = False

def check_aliens_bottom(ai_settings,stats,screen,sb,ship,aliens,bullets):
	#check if any aliens have reached the bottom of the screen
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			#treat this the same as if the ship got hit
			ship_hit(ai_settings,stats,screen,sb,ship,aliens,bullets)
			break

def check_fleet_edges(ai_settings,aliens):
	#respond appropriately if any aliens have reached an edge
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings,aliens)
			break

def change_fleet_direction(ai_settings,aliens):
	#drop the entire fleet and change the fleet's direction
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def create_stars(ai_settings,screen,stars):
	star = Star(ai_settings,screen)
	for star_num in xrange(ai_settings.number_of_stars):
		star = Star(ai_settings,screen)
		star.rect.x = randint(0,ai_settings.screen_width) 
		star.rect.y = randint(0,ai_settings.screen_height)
		stars.add(star)







