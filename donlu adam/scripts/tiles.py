import pygame
from random import randint
from math import floor

class Tiles(pygame.sprite.Sprite):
    def __init__(self, game, assets, tile_size, zoom):
        super().__init__()
        self.game = game
        self.surf_size = game.display.get_size()
        self.rect = None
        
        self.assets = assets
        self.map = []
        self.tile_size = tile_size
        self.zoom = zoom
        
    def make_map(self, width, height):
        #Make simple map for testing
        self.width, self.height = width, height
        self.map_size = width * height
        for i in range(0,height): 
            for j in range(0,width):
                self.map.append([(j,i), 'grass', randint(0, len(self.assets['grass'])-1)])
                if randint(0,10) == 0 or ((i * width) + j) == 1:
                    self.map[((i * width) + j)].append('tree')
                    self.map[((i * width) + j)].append(randint(0, len(self.assets['tree'])-1))
                else:
                    self.map[((i * width) + j)].append('empty')
                    self.map[((i * width) + j)].append(0)
    
    def update(self, p_cam, render_distance, zoom):
        self.cam = p_cam
        self.RD = render_distance
        self.zoom = zoom
    
    def render(self, surf):
        self.player_rendered = False

        #Render Tiles
        self.count = floor((self.cam[0] * self.zoom) / (self.tile_size * self.zoom)) + ((self.RD[0]-1) / 2)
        self.count += (self.width * floor((self.cam[1] * self.zoom) / (self.tile_size * self.zoom) + 1)) + (self.width * floor((self.RD[1]) / 2))
        
        self.count = floor(self.count)
        
        for i in range(self.count - (self.RD[1] * self.width), self.count, 1 * self.width):
            for j in range(i, (i - self.RD[0]), -1):
                
                if j >= 0 and j < self.map_size:
                    find_tile_pos = ((self.map[j][0][0] * (self.tile_size * self.zoom)) + (self.surf_size[0] / 2) - (self.cam[0] * self.zoom),
                                    (self.map[j][0][1] * (self.tile_size * self.zoom)) + (self.surf_size[1] / 2) - (self.cam[1] * self.zoom))
                    img_size = self.assets[self.map[j][1]][self.map[j][2]].get_size()
                    img = pygame.transform.scale(self.assets[self.map[j][1]][self.map[j][2]], (img_size[0] * self.zoom, img_size[1] * self.zoom))
                    surf.blit(img, find_tile_pos)
        
        #Render Objects and Player
        self.count = floor((self.cam[0] * self.zoom) / (self.tile_size * self.zoom)) + ((self.RD[0]-1) / 2)
        self.count += (self.width * floor((self.cam[1] * self.zoom) / (self.tile_size * self.zoom) + 1)) + (self.width * floor((self.RD[1]) / 2))
        
        self.count = floor(self.count)
        
        for i in range(self.count - (self.RD[1] * self.width), self.count, 1 * self.width):
            for j in range(i, (i - self.RD[0]), -1):
                
                if j >= 0 and j < self.map_size and self.map[j][3] != 'empty':
                    img_size = self.assets[self.map[j][3]][self.map[j][4]].get_size()
                    img = pygame.transform.scale(self.assets[self.map[j][3]][self.map[j][4]], (img_size[0] * self.zoom, img_size[1] * self.zoom))
                    self.rect = img.get_rect()
                    
                    find_tile_pos = ((self.map[j][0][0] * (self.tile_size * self.zoom)) + (self.surf_size[0] / 2) - (self.cam[0] * self.zoom),
                                (self.map[j][0][1] * (self.tile_size * self.zoom)) + ((self.surf_size[1] / 2) - (self.tile_size * self.zoom)) - (self.cam[1] * self.zoom))
                    
                    surf.blit(img, find_tile_pos)