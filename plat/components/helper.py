from plat.core.components import BaseComponent
from pygame import Surface, SRCALPHA

class PlayerStats(BaseComponent):

	def get_attrs(self):
		player = self.game.player
		image = self.get_image(player)
		rect = image.get_rect()
		rect.x = 300
		return image, rect 

	def on_update(self):
		player = self.game.player
		self.image = self.get_image(player)

	def get_image(self, component):
		surf = Surface((400, 400), SRCALPHA)
		surf = surf.convert_alpha()
		font = self.game.font
		
		text = str(component.pos) if component else 'Uninitialized'
		text = font.render(f"pos:{text}", True, (0, 0, 0))
		surf.blit(text, (0, 0))
		
		text = str(component.velocity) if component else 'Uninitialized'
		text = font.render(f"vel:{text}", True, (0, 0, 0))
		surf.blit(text, (0, self.game.font_size))

		text = str(component.acceleration) if component else 'Uninitialized'
		text = font.render(f"acc:{text}", True, (0, 0, 0))
		surf.blit(text, (0, self.game.font_size * 2))

		text = str(component.beforefic) if component else 'Uninitialized'
		text = font.render(f"bef_fric:{text}", True, (0, 0, 0))
		surf.blit(text, (0, self.game.font_size * 3))

		text = str(component.baseacc) if component else 'Uninitialized'
		text = font.render(f"base_acc:{text}", True, (0, 0, 0))
		surf.blit(text, (0, self.game.font_size * 4))

		text = str(component.joyinput) if component else 'Uninitialized'
		text = font.render(f"joy_in:{text}", True, (0, 0, 0))
		surf.blit(text, (0, self.game.font_size * 5))
		
		return surf