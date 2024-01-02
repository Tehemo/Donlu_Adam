import pygame
from math import floor, ceil
from scripts import utils

class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos:list, map_size:int, tile_size:int, zoom):
        super().__init__()
        self.game = game
        self.img = self.game.pimg
        self.surf_size = game.display.get_size()
        
        self.pos = list(pos)
        self.cam = list(pos)
        
        self.map_size = map_size
        self.tile_size = tile_size
        self.zoom = zoom
        self.rect = self.game.pimg.get_rect()
        
        #Movement variables        
        self.movement = [[False,False],[False,False],True,[False,False],[False,False]] #0-X, 1-Y, 2-Free cam toggle, 3-cam X, 4-cam Y
        self.base_vel = [self.tile_size / 12, self.tile_size / 16] #[Running, Walking]
        self.vel = self.base_vel[1]
        self.cam_vel = self.base_vel[0]
        
        self.lastx, self.lasty = 0, 0
        
    def update(self, zoom):
        #Variable Assignment
        self.zoom = zoom
        
        #Movement
        factor_x = self.vel / (abs((self.movement[1][0] - self.movement[1][1]) * 2**.5) + 1 - abs((self.movement[1][0] - self.movement[1][1])))
        factor_y = self.vel / (abs((self.movement[0][0] - self.movement[0][1]) * 2**.5) + 1 - abs((self.movement[0][0] - self.movement[0][1])))
        
        if self.lastx != factor_x or self.lasty != factor_y: #*Debug
            print(f'Raw vel X:{factor_x}, Y:{factor_y}; rounded vel X:{round(factor_x)}, Y:{round(factor_y)}')
            self.lastx, self.lasty = factor_x, factor_y
        
        self.pos[0] = round(self.pos[0] + factor_x * (self.movement[0][1] - self.movement[0][0]))
        self.pos[1] = round(self.pos[1] + factor_y * (self.movement[1][1] - self.movement[1][0]))

        #Camera positioning
        if self.movement[2] == False: self.cam[0], self.cam[1] = round(self.cam[0] + ((self.pos[0] - self.cam[0]) / 5), 0), round(self.cam[1] + ((self.pos[1] - self.cam[1]) / 5), 0)
        else: self.cam[0], self.cam[1] = self.cam[0] + (self.cam_vel * (self.movement[3][0]*-1 + self.movement[3][1]*1)), self.cam[1] + (self.cam_vel * (self.movement[4][0]*-1 + self.movement[4][1]*1))
        
        self.cam[0] = max(self.surf_size[0] / (2 * self.zoom), min(self.cam[0], self.map_size[0] * (self.tile_size) - (self.surf_size[0] / (2 * self.zoom))))
        self.cam[1] = max(self.surf_size[1] / (2 * self.zoom), min(self.cam[1], self.map_size[1] * (self.tile_size) - (self.surf_size[1] / (2 * self.zoom))))
        
        return self.cam, self.pos
    
    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.movement[0][0], self.movement[2], self.movement[3][0] = False, True, True
            if event.key == pygame.K_RIGHT:
                self.movement[0][1], self.movement[2], self.movement[3][1] = False, True, True
            if event.key == pygame.K_UP:
                self.movement[1][0], self.movement[2], self.movement[4][0] = False, True, True
            if event.key == pygame.K_DOWN:
                self.movement[1][1], self.movement[2], self.movement[4][1] = False, True, True
            if event.key == pygame.K_LSHIFT:
                self.cam_vel = self.base_vel[0] * 4
                self.vel = self.base_vel[0]
            
            if event.key == pygame.K_a:
                self.movement[0][0], self.movement[2], self.movement[3][0] = True, False, False
            if event.key == pygame.K_d:
                self.movement[0][1], self.movement[2], self.movement[3][1] = True, False, False
            if event.key == pygame.K_w:
                self.movement[1][0], self.movement[2], self.movement[4][0] = True, False, False
            if event.key == pygame.K_s:
                self.movement[1][1], self.movement[2], self.movement[4][1] = True, False, False
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.movement[3][0] = False
            if event.key == pygame.K_RIGHT:
                self.movement[3][1] = False
            if event.key == pygame.K_UP:
                self.movement[4][0] = False
            if event.key == pygame.K_DOWN:
                self.movement[4][1] = False
            if event.key == pygame.K_LSHIFT:
                self.cam_vel = self.base_vel[0]
                self.vel = self.base_vel[1]
            
            if event.key == pygame.K_a:
                self.movement[0][0] = False
            if event.key == pygame.K_d:
                self.movement[0][1] = False
            if event.key == pygame.K_w:
                self.movement[1][0] = False
            if event.key == pygame.K_s:
                self.movement[1][1] = False
    
    def render(self, surf):
        img_size = self.game.pimg.get_size()
        self.img = pygame.transform.scale(self.game.pimg, (img_size[0] * self.zoom, img_size[1] * self.zoom))
        surf.blit(self.img, ((self.pos[0] * self.zoom) + ((self.surf_size[0] / 2) - ((self.tile_size * self.zoom) / 2)) - (self.cam[0] * self.zoom),
                        (self.pos[1] * self.zoom) + ((self.surf_size[1] / 2) - ((self.tile_size * self.zoom) / 2)) - (self.cam[1] * self.zoom)))