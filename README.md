# PLAT

PLAT is a side-scrolling paltforming game and level creation system. 

## Requirements
This projects requires python3.6+ and a joystick controller to play.

## Run

### Linux

	python3 -m venv venv
	source venv\bin\activate
	pip install -r requirements.txt
	python plat

### Windows

	python3 -m venv venv
	venv\Scripts\activate
	pip install -r requirements.txt
	python plat

## Controls

### General

* Left Stick: Movement
* Y: Change state from level creation to gameplay.
* B: breakpoint() (debugging)

### Level Creation

* X: Place block
* A: Remove block
* SHARE: Reset grid

### Gameplay

* A: Jump
