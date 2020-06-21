import logging
import xml.etree.ElementTree as ET

from typing import List
from collections import namedtuple
from os.path import dirname, join, sep

from pygame import Surface
from pygame.math import Vector2
from pygame.sprite import Group, Sprite
from pygame.transform import scale, flip
from pygame.image import load as pg_load

from plat.core.utils import *


Pos = namedtuple("Pos", "x y")


class SpriteXmlParser:
    @classmethod
    def parse(cls, path):
        tree = ET.parse(path)
        root = tree.getroot()
        source = root.get('imagePath')
        if not source:
            raise KeyError('imagePath')
        rowgen = (cls._parse_xml_row(r) for r in root)
        return source, rowgen

    @classmethod
    def _parse_xml_row(cls, row):
        return row.attrib


class SpriteManager:
    def __init__(self, game, maps, sprites_dir):
        self.game = game
        self.sprites_dir = sprites_dir
        self.sprites = {}
        self.sources = {}
        self.maps = maps

    def load(self):
        self._load(self.maps)

    def _load(self, map_, name=None):
        name = name.strip('.') if name else ""
        if isinstance(map_, dict):
            for category, next_ in map_.items():
                name += f".{category}"
                self._load(next_, name)

        elif isinstance(map_, str):
            path = join(
                self.sprites_dir, 
                name.replace('.', sep),
                map_,
            )
            self._load_atlas(name, path)

    def _load_atlas(self, name, path):
        self.sprites[name] = {}
        self.sources[name] = {}
        source, sprites = SpriteXmlParser.parse(path)
        for sprite in sprites:
            spritename = sprite['name']
            self.sprites[name][spritename] = sprite
        source = join(dirname(path), source)
        self._load_source(name, source)

    def _load_source(self, name, path):
        self.sources[name] = pg_load(path).convert()

    def get(self, path, name) -> Surface:
        data = self.sprites[path][name]
        x, y = int(data.get('x')), int(data.get('y')) 
        width, height = int(data.get('width')), int(data.get('height'))
        img = Surface((width, height))
        img.blit(self.sources[path], (0, 0), (x, y, width, height))
        img.set_colorkey(BLACK)
        height = 40 # self.game.state.grid.bheight if self.game.state else 16
        width = 40 # self.game.state.grid.bwidth if self.game.state else 16
        return scale(img, (height, width))


class AnimationManager:
    def __init__(self, animations, spritemanager):
        self.animations = animations
        self.spritemanager = spritemanager

    def get(self, name):
        return Animation(name, self.animations[name]).load(self.spritemanager)


class Animation:
    def __init__(self, name, frames=[], speed=200, flip=False):
        self.name = name
        self.flip = flip
        self.speed = speed
        self.current_frame = 0
        self.last_update = 0
        self.raw_frames = frames
        self.frames = []

    def load(self, spritemanager):
        for fdata in self.raw_frames:
            frame = spritemanager.get(*fdata)
            if self.flip:
                flip(frame)
            self.frames.append(frame)
        return self

    def reset(self):
        self.current_frame = 0
        self.last_update = 0

    def get_next_frame(self, time):
        print(self.name, self.current_frame, len(self.frames))
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.last_update = time
        return self.frames[self.current_frame]


class BaseComponent(Sprite):
    def __init__(self, game, children: List[Sprite] = None, grid=None):
        children = children or []
        Sprite.__init__(self)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.game = game
        self.grid = grid
        self.image, self.rect = self.get_attrs()
        self.children = SpriteGroup()
        for child in children:
            self.children.add(child) 
        self.new()

    @property
    def pos(self):
        return Pos(self.rect.midbottom[0], self.rect.midbottom[1])

    @pos.setter
    def pos(self, xypair):
        """ Pos will remain inside boundries of grid. Hitting an edge will stop the player. """
        x, y = xypair
        if x < 0 or self.game.state.grid.width < x:
            self.velocity.x = 0
        if y < 0 or self.game.state.grid.height < y:
            self.velocity.y = 0
        x = min(max(x, 0), self.game.state.grid.width)
        y = min(max(y, 0), self.game.state.grid.height)
        self.rect.midbottom = (x, y)

    def get_attrs(self):
        raise NotImplementedError()

    def new(self):
        pass

    def event(self, event):
        self.on_event(event)
        for child in self.children:
            child.event(event)

    def on_event(self, event):
        pass

    def update(self):
        self.on_update()
        if self.children:
            self.children.update()

    def on_update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if len(self.children):
            for child in self.children:
                child.draw(screen)

    def __repr__(self):
        return f"<{self.__class__.__name__}  pos={self.pos} acc={self.acceleration} vel={self.velocity}>"



class SpriteGroup:
    ALL_SPRITES = Group()

    def __init__(self):
        self.sprites = Group()

    @property
    def children(self):
        return self.sprites

    def add(self, sprite: Sprite):
        self.ALL_SPRITES.add(sprite)
        self.sprites.add(sprite)

    def remove(self, sprite: Sprite):
        self.ALL_SPRITES.remove(sprite)
        self.sprites.remove(sprite)

    def update(self):
        self.sprites.update()

    def draw(self, screen):
        for sprite in self.sprites:
            if hasattr(sprite, 'on_draw'):
                sprite.on_draw(screen)
            sprite.draw(screen)

    def empty(self):
        return self.sprites.empty()

    def __iter__(self):
        return self.sprites.__iter__()

    def __len__(self):
        return len(self.sprites)
