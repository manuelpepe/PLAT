from plat.core.components import BaseComponent
from pygame import Surface, SRCALPHA

class PlayerStats(BaseComponent):
	ATTRS = [
		"pos",
		"center",
		"velocity",
		"acceleration",
		"beforefic",
		"baseacc",
		"joyinput",
		"JUMP_FORCE",
		"GRAVITY",
		"MIN_JUMP",
	]

	def get_attrs(self):
		player = self.game.player
		image = self.get_image(player)
		rect = image.get_rect()
		rect.x = 0
		rect.y = self.game.font_size
		return image, rect 

	def on_update(self):
		player = self.game.player
		self.image = self.get_image(player)

	def get_image(self, component):
		surf = Surface((400, 400), SRCALPHA)
		surf = surf.convert_alpha()
		return self.blit_on(component, surf)

	def blit_on(self, comp, surf):
		font = self.game.font
		rowsize = self.game.font_size
		for ix, attr in enumerate(self.ATTRS):
			try:
				value = str(getattr(comp, attr))
				text = value if comp else 'Uninitialized'
				text = font.render(f"{attr}: {text}", True, (0, 0, 0))
				surf.blit(text, (0, rowsize * ix))
			except AttributeError:
				pass
		return surf