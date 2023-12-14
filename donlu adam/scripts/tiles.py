import pygame
from random import randint
from math import floor

class Tiles:
    def __init__(self, game, assets, tile_size, zoom):
        self.game = game
        self.surf_size = game.display.get_size()
        
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
    
    def render(self, surf, p_cam, p_pos, player, render_distance):
        self.player_rendered = False

        self.RD = render_distance
        #Render Tiles
        self.count = floor((p_cam[0] * self.zoom) / (self.tile_size * self.zoom)) + ((self.RD[0]-1) / 2)
        self.count += (self.width * floor((p_cam[1] * self.zoom) / (self.tile_size * self.zoom) + 1)) + (self.width * floor((self.RD[1]) / 2))
        
        self.count = floor(self.count)
        
        for i in range(self.count - (self.RD[1] * self.width), self.count, 1 * self.width):
            for j in range(i, (i - self.RD[0]), -1):
                
                if j >= 0 and j < self.map_size:
                    find_tile_pos = ((self.map[j][0][0] * (self.tile_size * self.zoom)) + (self.surf_size[0] / 2) - (p_cam[0] * self.zoom),
                                    (self.map[j][0][1] * (self.tile_size * self.zoom)) + (self.surf_size[1] / 2) - (p_cam[1] * self.zoom))
                    img_size = self.assets[self.map[j][1]][self.map[j][2]].get_size()
                    img = pygame.transform.scale(self.assets[self.map[j][1]][self.map[j][2]], (img_size[0] * self.zoom, img_size[1] * self.zoom))
                    surf.blit(img, find_tile_pos)
        
        #Render Objects and Player
        self.count = floor((p_cam[0] * self.zoom) / (self.tile_size * self.zoom)) + ((self.RD[0]-1) / 2)
        self.count += (self.width * floor((p_cam[1] * self.zoom) / (self.tile_size * self.zoom) + 1)) + (self.width * floor((self.RD[1]) / 2))
        
        self.count = floor(self.count)
        
        for i in range(self.count - (self.RD[1] * self.width), self.count, 1 * self.width):
            for j in range(i, (i - self.RD[0]), -1):
                
                if j >= 0 and j < self.map_size:
                    if self.map[j][3] != 'empty':
                        img_size = self.assets[self.map[j][3]][self.map[j][4]].get_size()
                        img = pygame.transform.scale(self.assets[self.map[j][3]][self.map[j][4]], (img_size[0] * self.zoom, img_size[1] * self.zoom))
                    find_tile_pos = ((self.map[j][0][0] * (self.tile_size * self.zoom)) + (self.surf_size[0] / 2) - (p_cam[0] * self.zoom),
                                    (self.map[j][0][1] * (self.tile_size * self.zoom)) + ((self.surf_size[1] / 2) - (self.tile_size * self.zoom)) - (p_cam[1] * self.zoom))
                    
                    if ((p_pos[1] - (self.tile_size / 2) < (self.map[j][0][1] * self.tile_size) and p_pos[0] > self.map[j][0][0] * self.tile_size) or p_pos[0] < self.tile_size / 2 or p_pos[1] > (self.height * self.tile_size - self.tile_size / 2)) and self.player_rendered == False:
                        player.render(surf)
                        self.player_rendered = True
                        
                        if self.map[j][3] != 'empty': #If player stands behind an object make that object transparent and render that
                            img.set_alpha(80)
                            surf.blit(img, find_tile_pos)
                            img.set_alpha(255)
                    
                    else:
                        if self.map[j][3] != 'empty':
                            surf.blit(img, find_tile_pos)