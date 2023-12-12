import pygame
from math import floor, ceil

class Player:
    def __init__(self, game, pos:list, map_size:int, tile_size:int, guis):
        self.game = game
        self.pos = list(pos)
        self.cam = list(pos)
        
        self.map_size = map_size
        self.tile_size = tile_size
        self.rect = self.game.pimg.get_rect()
        self.rect.center = self.pos
        
        self.movement = [[False,False],[False,False],True,[False,False],[False,False]] #0-X, 1-Y, 2-Free cam toggle, 3-cam X, 4-cam Y
        self.vel = tile_size / 8
        self.cam_vel = tile_size / 2
        
        self.inventory_open = False
        self.inventory_x = -320
        self.guis = guis
        
    def update(self):
        #Movement
        self.pos[0] = round(self.pos[0] + ((self.vel / (abs((self.movement[1][0] - self.movement[1][1]) * 2**.5) + 1 - abs((self.movement[1][0] - self.movement[1][1])))) * (self.movement[0][0]*-1 + self.movement[0][1]*1)))
        self.pos[1] = round(self.pos[1] + ((self.vel / (abs((self.movement[0][0] - self.movement[0][1]) * 2**.5) + 1 - abs((self.movement[0][0] - self.movement[0][1])))) * (self.movement[1][0]*-1 + self.movement[1][1]*1)))
        
        if self.movement[2] == False: self.cam[0], self.cam[1] = round(self.cam[0] + ((self.pos[0] - self.cam[0]) / 5), 0), round(self.cam[1] + ((self.pos[1] - self.cam[1]) / 5), 0)
        else: self.cam[0], self.cam[1] = self.cam[0] + (self.cam_vel * (self.movement[3][0]*-1 + self.movement[3][1]*1)) , self.cam[1] + (self.cam_vel * (self.movement[4][0]*-1 + self.movement[4][1]*1))
        
        if self.cam[0] < 160: self.cam[0] = 160
        if self.cam[0] > self.map_size[0] * self.tile_size - 160: self.cam[0] = self.map_size[0] * self.tile_size - 160
        if self.cam[1] < 120: self.cam[1] = 120
        if self.cam[1] > self.map_size[1] * self.tile_size - 120: self.cam[1] = self.map_size[1] * self.tile_size - 120
        
        #Mouse
        mouse_buttons, mouse_pos = pygame.mouse.get_pressed(), pygame.mouse.get_pos()
        
        #Inventory
        self.inventory()
        
        return self.cam, self.pos, mouse_buttons, mouse_pos
    
    def inventory(self):
        if self.inventory_open == True:
            if self.inventory_x < -160: self.inventory_x += ceil((-160 - self.inventory_x) / 10)
        if self.inventory_open == False:
            if self.inventory_x > -320: self.inventory_x += floor((-320 - self.inventory_x) / 10)
    def render_inventory(self,surf):
        surf.blit(self.guis['inventory'][0], (self.inventory_x + 160, 0))
    
    def player_event(self, event):
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
                self.cam_vel = self.tile_size
            
            if event.key == pygame.K_a:
                self.movement[0][0], self.movement[2], self.movement[3][0] = True, False, False
            if event.key == pygame.K_d:
                self.movement[0][1], self.movement[2], self.movement[3][1] = True, False, False
            if event.key == pygame.K_w:
                self.movement[1][0], self.movement[2], self.movement[4][0] = True, False, False
            if event.key == pygame.K_s:
                self.movement[1][1], self.movement[2], self.movement[4][1] = True, False, False
                
            if event.key == pygame.K_e:
                if self.inventory_open == False:
                    self.inventory_open = True
                else:
                    self.inventory_open = False
                
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
                self.cam_vel = self.tile_size / 2
            
            if event.key == pygame.K_a:
                self.movement[0][0] = False
            if event.key == pygame.K_d:
                self.movement[0][1] = False
            if event.key == pygame.K_w:
                self.movement[1][0] = False
            if event.key == pygame.K_s:
                self.movement[1][1] = False
    
    def render(self, surf):
        surf.blit(self.game.pimg, (self.pos[0] + (160 - (self.tile_size / 2)) - self.cam[0], self.pos[1] + (120 - (self.tile_size / 2)) - self.cam[1]))