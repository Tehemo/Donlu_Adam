import pygame
import sys
from math import floor

from scripts.entities import Player
from scripts.tiles import Tiles
from scripts.utils import SetSize, LoadImage, LoadImages
class CameraGroup(pygame.sprite.Group):
    def __init__(self, display):
        super().__init__()
        self.display_surface = display

    def custom_draw(self):
        for sprite in self.sprites():
            print(sprite)
            sprite.render(self.display_surface)
class Game:
    def __init__(self):
        pygame.init()
        
        pygame.display.set_caption('Testing stuff...')
        
        WIDTH, HEIGHT = 1280, 960
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT), pygame.RESIZABLE)
        self.display = pygame.Surface((640 * 2, 480 * 2)) #you can increase the multipliers but this will reduce the render speed
        self.display_size = self.display.get_size()

        self.Clock = pygame.time.Clock()
        
        self.tile_size, self.zoom = SetSize(16, 3, 1) #(TILE_SIZE, RATIO, ZOOM)
        
        self.camera_group = CameraGroup(self.display)
        self.all_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        
        tile_assets = {
            'empty' : [pygame.Surface((0,0))],
            'grass' : LoadImages('tiles/grass'),
            'water' : LoadImages('tiles/water'),
            'tree' : LoadImages('tiles/tree')
        }
        print(tile_assets)
        
        self.map_size = (100,100)
        
        Game.updateRD(self)
        
        self.tiles = Tiles(self, tile_assets, self.tile_size, self.zoom)
        self.tiles.make_map(self.map_size[0], self.map_size[1])

        self.guis = {
            'inventory' : LoadImage('gui\inventory\inventory.png'),
            'health' : LoadImages('gui/health')
        }
        print(tile_assets,self.guis)
        
        self.pimg = LoadImage('player/skin/skin.png')
        self.player = Player(self, ((self.tile_size * 20), (self.tile_size * 20)), self.map_size, self.tile_size, self.zoom)
        self.player_group.add(self.player)
        self.all_group.add(self.player)
        
        self.camera_group.add(self.player)
        self.camera_group.add(self.tiles)
        
    def updateRD(self):
        self.RD = [floor((self.display_size[0] / (self.tile_size * self.zoom)) + (self.tile_size / 8) - 1),
                   floor((self.display_size[1] / (self.tile_size * self.zoom)) + (self.tile_size / 8) + 1)]
    
    def game(self):
        self.display.fill((0,0,0))
            
        for event in pygame.event.get():
            self.player.event(event)    
            if event.type == pygame.MOUSEWHEEL:
                if event.y != None:
                    if event.y == 1 and self.zoom+0.5 <= 6: #up
                        self.zoom = round(self.zoom + 0.5, 1)
                    if event.y == -1 and self.zoom-0.5 > 0: #down
                        self.zoom = round(self.zoom - 0.5, 1)
                    Game.updateRD(self)
                    print(self.zoom)
                    print(self.RD)
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        #Update
        self.p_cam, self.p_pos = self.player.update(self.zoom)
        self.tiles.update(self.p_cam, self.RD, self.zoom)
        
        #Render
        self.camera_group.custom_draw()

    def main_menu(self):
        pass
    
    def run(self):
        while True:
            self.game()
            
            self.screen.blit(pygame.transform.scale(self.display, (self.screen.get_size()[0],self.screen.get_size()[1])), (0, 0))
            pygame.display.update()
            self.Clock.tick(60)

if __name__ == '__main__':
    Game().run()