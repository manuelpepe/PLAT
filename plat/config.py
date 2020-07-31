FPS = 60


ARROW_JOY_SPEED = (10, 10)
ARROW_FRICTION = -0.7

PLAYER_JOY_SPEED = (0.6, 0)
PLAYER_FRICTION = -0.09

PLAYER_MIN_JUMP = 1
PLAYER_JUMP_FORCE = 21
PLAYER_GRAVITY = 0.76


SPRITE_MAPS = {
	"characters": {
		"blue": "blue.xml",
	}
}


ANIMATIONS = {
	"playerStand": [
		('characters.blue', 'blue_01.png'),
		('characters.blue', 'blue_02.png'),
		('characters.blue', 'blue_03.png'),
	],
	"playerWalk": [
		('characters.blue', 'blue_04.png'),
		('characters.blue', 'blue_05.png'),
		('characters.blue', 'blue_06.png'),
		('characters.blue', 'blue_07.png'),
		('characters.blue', 'blue_08.png'),
	]
}