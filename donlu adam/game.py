import pygame
import sys
from math import floor

from scripts.entities import Player
from scripts.tiles import Tiles
from scripts.utils import SetSize, LoadImage, LoadImages

class Game:
    def __init__(self):
        pygame.init()
        
        pygame.display.set_caption('Testing stuff...')
        
        WIDTH, HEIGHT = 1280, 960
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.RESIZABLE)
        self.display = pygame.Surface((640 * 1, 480 * 1)) #you can increase the multipliers but this will reduce the render speed
        self.display_size = self.display.get_size()

        self.Clock = pygame.time.Clock()
        
        self.tile_size, self.zoom = SetSize(16, 2, 1) #(TILE_SIZE, RATIO, ZOOM)
        
        tile_assets = {
            'empty' : 'empty',
            'grass' : LoadImages('tiles/grass'),
            'water' : LoadImages('tiles/water'),
            'tree' : LoadImages('tiles/tree')
        }
        
        self.map_size = (100,100)
        
        Game.updateRD(self)
        
        self.tiles = Tiles(self, tile_assets, self.tile_size, self.zoom)
        self.tiles.make_map(self.map_size[0], self.map_size[1])

        self.guis = {
            'inventory' : LoadImage('gui\inventory\inventory.png'),
            'health' : LoadImages('gui/health')
        }
        print(tile_assets,self.guis)
        
        self.pimg = LoadImage('player/player.png')
        self.player = Player(self, ((self.tile_size * 20), (self.tile_size * 20)), self.map_size, self.tile_size, self.zoom, self.guis)
    
    def updateRD(self):
        self.RD = [floor((self.display_size[0] / (self.tile_size * self.zoom)) + (self.tile_size / 8) - 1),
                   floor((self.display_size[1] / (self.tile_size * self.zoom)) + (self.tile_size / 8) + 1)]
    
    def run(self):
        while True:
            self.display.fill((0,0,0))
            
            for event in pygame.event.get():
                scroll_wheel = self.player.player_event(event)
                if scroll_wheel != None:
                    if scroll_wheel == 'up' and self.zoom+0.5 <= 8:
                        self.zoom = round(self.zoom + 0.5, 1)
                    if scroll_wheel == 'down' and self.zoom-0.5 > 0:
                        self.zoom = round(self.zoom - 0.5, 1)
                    Game.updateRD(self)
                    print(self.zoom)
                    print(self.RD)
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print(self.p_cam, self.p_pos, self.RD)
                    if event.key == pygame.K_F1:
                        self.RD[0], self.RD[1] = self.RD[0] + 1, self.RD[1] + 1
                    if event.key == pygame.K_F2:
                        self.RD[0], self.RD[1] = self.RD[0] - 1, self.RD[1] - 1
            
            self.p_cam, self.p_pos = self.player.update()
            
            self.tiles.render(self.display, self.p_cam, self.p_pos, self.player, self.RD, self.zoom)
            
            self.player.render_inventory(self.display)
            
            self.screen.blit(pygame.transform.scale(self.display, (self.screen.get_size()[0],self.screen.get_size()[1])), (0, 0))
            pygame.display.update()
            self.Clock.tick(60)

if __name__ == '__main__':
    Game().run()