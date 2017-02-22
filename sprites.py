# -*- coding: utf-8 -*-

import pygame
import settings as sett
import pytweening as tween
vec = pygame.math.Vector2


def collide_with_walls(sprite, group, direction):
    if direction == 'x':
        hits = pygame.sprite.spritecollide(sprite, group, False)
        if hits:
            if sprite.vel.x > 0:
                # sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2 IN ORIGINAL
                sprite.pos.x = hits[0].rect.left - sprite.rect.width
            elif sprite.vel.x < 0:
                # sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2 IN ORIGINAL
                sprite.pos.x = hits[0].rect.right
                
            # if we hit, then we stop
            sprite.vel.x = 0
            sprite.rect.x = sprite.pos.x
            
    if direction == 'y':
        hits = pygame.sprite.spritecollide(sprite, group, False)
        if hits:
            if sprite.vel.y > 0:
                # sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2 IN ORIGINAL
                sprite.pos.y = hits[0].rect.top - sprite.rect.height
            elif sprite.vel.y < 0:
                # sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2 IN ORIGINAL
                sprite.pos.y = hits[0].rect.bottom
                
            # if we hit, then we stop
            sprite.vel.y = 0
            sprite.rect.y = sprite.pos.y
            

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = sett.PLAYER_LAYER
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.image_right = self.image.copy()
        self.image_left = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.look_dir = "right"
        
        # Vectors
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        
    def get_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vel.x = -sett.PLAYER_SPEED
            self.look_dir = "left"
        if keys[pygame.K_RIGHT]:
            self.vel.x = sett.PLAYER_SPEED
            self.look_dir = "right"
        if keys[pygame.K_UP]:
            self.rect.y += 2
            hits = pygame.sprite.spritecollide(self, self.game.walls, False)
            self.rect.y -= 2
            if hits:
                self.game.sound_effects['jump'].play()
                self.vel.y = -7.2
            
    def update(self):
        self.calc_grav()
        self.get_keys()
        self.pos += self.vel
        self.rect.x = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.rect.y = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        
        if self.look_dir == "left":
            self.image = self.image_left
        elif self.look_dir == "right":
            self.image = self.image_right
            
        self.vel.x = 0
        
    def calc_grav(self):
        if self.vel.y == 0:
            self.vel.y = 1
        else:
            self.vel.y += .35
            
    
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        # Member of all sprites groups and walls groups (???)
        self.groups = game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
        
class Lava(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.lavas
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
        
class Item(pygame.sprite.Sprite):
    def __init__(self, game, pos, item_type):
        self._layer = sett.ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[item_type]
        self.rect = self.image.get_rect()
        self.item_type = item_type
        self.rect.center = pos
        self.pos = pos
        
        # Choose tween function
        self.tween = tween.easeInOutSine
        
        # Store where we are, range: [0, 1]
        self.step = 0
        self.direction = 1
        
    def update(self):
        # Bobbing motion
        # - 0.5 because we start from the center
        offset = sett.BOB_RANGE * (self.tween(self.step / sett.BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.direction
        self.step += sett.BOB_SPEED
        if self.step > sett.BOB_RANGE:
            self.step = 0
            self.direction *= -1
            
            
class Finish(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        
        
class FallingItem(pygame.sprite.Sprite):
    def __init__(self, game, x, y, item_type):
        self._layer = sett.EFFECTS_LAYER
        self.groups = game.all_sprites, game.fallings, game.lavas
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.item_images[item_type]
        tmp_image = self.image.copy()
        tmp_image = pygame.transform.rotozoom(tmp_image, 0, 0.62)
        self.rect = tmp_image.get_rect()
        self.item_type = item_type
        self.rect.right = x
        self.rect.bottom = y
        
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        
        self.fall = False
        
    def update(self):
        if self.fall:
            self.vel.y += .35
            self.pos += self.vel
            self.rect.topright = self.pos
            if self.rect.centery > sett.HEIGHT + 50:
                self.kill()
            
           
#class Mob(pygame.sprite.Sprite):
#    # MOB NEEDS TO BE CAREFULLY COMPLETED FROM SCRATCH
#    def __init__(self, game, x, y):
#        # Member of all sprites and mob groups
#        self._layer = sett.MOB_LAYER
#        self.groups = game.all_sprites, game.mobs
#        pygame.sprite.Sprite.__init__(self, self.groups)
#        self.game = game
#        self.image = game.mob_img
#        self.rect = self.image.get_rect()
#        self.rect.center = (x, y)
#        # self.hit_rect = MOB_HIT_RECT.copy() IN ORIGINAL
#        self.pos = vec(x, y)
#        self.vel = vec(0, 0)
#        self.rect.center = self.pos
#    #def update(self)