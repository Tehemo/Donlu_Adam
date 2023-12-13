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
        self.display = pygame.Surface((320 * 2,240 * 2))
        self.display_size = self.display.get_size()

        self.Clock = pygame.time.Clock()
        
        self.tile_size, self.zoom = SetSize(16, 2) #(TILE_SIZE, ZOOM)
        
        tile_assets = {
            'empty' : 'empty',
            'grass' : LoadImages('tiles/grass'),
            'water' : LoadImages('tiles/water'),
            'tree' : LoadImages('tiles/tree')
        }
        
        self.map_size = (100,100)
        
        self.RD = [floor((self.display_size[0] / self.tile_size) + (self.tile_size / 8) - 1),
                   floor((self.display_size[1] / self.tile_size) + (self.tile_size / 8) + 1)]
        
        self.tiles = Tiles(self, tile_assets, self.tile_size, self.zoom)
        self.tiles.make_map(self.map_size[0], self.map_size[1])

        self.guis = {
            'inventory' : LoadImage('gui\inventory\inventory.png'),
            'health' : LoadImages('gui/health')
        }
        print(tile_assets,self.guis)
        
        self.pimg = LoadImage('player/player.png')
        self.player = Player(self, (0,0), self.map_size, self.tile_size, self.zoom, self.guis)
        
    def run(self):
        while True:
            self.display.fill((0,0,0))
            
            for event in pygame.event.get():
                self.player.player_event(event)
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print(self.p_cam, self.p_pos, self.RD, self.mouse_pos, self.RD)
                    if event.key == pygame.K_F1:
                        self.RD[0], self.RD[1] = self.RD[0] + 1, self.RD[1] + 1
                    if event.key == pygame.K_F2:
                        self.RD[0], self.RD[1] = self.RD[0] - 1, self.RD[1] - 1
            
            self.p_cam, self.p_pos, self.mouse_buttons, self.mouse_pos = self.player.update()
            
            self.tiles.render(self.display, self.p_cam, self.p_pos, self.player, self.RD)
            
            self.player.render_inventory(self.display)
            
            self.screen.blit(pygame.transform.scale(self.display, (self.screen.get_size()[0],self.screen.get_size()[1])), (0, 0))
            pygame.display.update()
            self.Clock.tick(60)

if __name__ == '__main__':
    Game().run()