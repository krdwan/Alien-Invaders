class Settings():
	# A class to sotre all settings for Alien Invasion
	def __init__(self):
		###static settings###

		#screen settings
		self.screen_width=1200
		self.screen_height=800
		self.bg_color = (230,230,230)
		#self.ship_speed_factor = 3.5

		#bullet settings
		#self.bullet_speed_factor = 3
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 60,60,60
		self.bullets_allowed = 15
		self.bullets_persist = False

		#star settings
		self.number_of_stars = 0

		#alien settings
		#self.alien_speed_factor = 3 #default 1
		self.fleet_drop_speed = 60 #default 10

		#self.fleet_direction = 1

		#ship settings (# of extra lives)
		self.ship_limit = 2

		#status settings
		self.game_active = True

		###dynamic settings###
		#how quickly the game speeds up
		self.speedup_scale = 2
		#how quickly the alien point values increase
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		#initialize settings that change throughout the game
		self.ship_speed_factor = 3.5
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 1
		self.alien_points = 50

		#fleet_direction of 1 represents right; -1 represents left
		self.fleet_direction = 1

	def increase_speed(self):
		#increase speed settings
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale

		self.alien_points = int(self.alien_points * self.score_scale)
		print(self.alien_points)