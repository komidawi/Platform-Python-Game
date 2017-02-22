# -*- coding: utf-8 -*-

import pygame
import pytmx
import settings as sett

      
class TiledMap:
    def __init__(self, filename):
        # pixelalpha=True to make sure the transparency go on
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        
        # Width in tiles
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        
        # We will store all data in this variable
        self.tmxdata = tm
        
    def render(self, surface):
        # ti will be alias to this command  
        ti = self.tmxdata.get_tile_image_by_gid
        
        my_gid = self.tmxdata.get_layer_by_name("Image").gid
        my_tile = ti(my_gid)
        surface.blit(my_tile, (0, 0))
        
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))
                        
    def make_map(self):
        temp_surface = pygame.Surface([self.width, self.height])
        self.render(temp_surface)
        return temp_surface
    
        
class Camera:
    def __init__(self, width, height):
        # As we can see camera is just a Rectangle
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        
    # Apply offset to the entity
    def apply(self, entity):
        # move() gives new rectangle shifted by amount of an argument
        return entity.rect.move(self.camera.topleft)
        
    # Apply offset to the rectangle
    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)
        
    def update(self, target):
        # We wanted centered on the screen
        x = -target.rect.x + (sett.WIDTH // 2)
        y = -target.rect.y + (sett.HEIGHT // 2)
        
        # Limit scrolling to map size
        x = min(0, x) # left
        y = min(0, y) # top
        x = max(-(self.width - sett.WIDTH), x) # right
        y = max(-(self.height - sett.HEIGHT), y) # bottom
        self.camera = pygame.Rect(x, y, self.width, self.height)