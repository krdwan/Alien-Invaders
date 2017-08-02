class GameStats():
	#track statistics for alien game
	def __init__(self,ai_settings):
		self.ai_settings=ai_settings

		#high score should never be reset
		self.high_score = 0
		self.reset_status()

		#status settings
		self.game_active = False

	def reset_status(self):
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1
