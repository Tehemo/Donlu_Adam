import pygame
import os

Base_Image_Path = 'donlu adam/data/images/'

def SetSize(size, zoom = 1):
    global TILE_SIZE
    global ZOOM
    TILE_SIZE = size
    ZOOM = zoom
    return size, zoom

def LoadImage(path):
    img = pygame.image.load(Base_Image_Path + path).convert_alpha()
    img.set_colorkey((0, 0, 0))
    img_size = img.get_size()
    return pygame.transform.scale(img, (img_size[0] * ZOOM, img_size[1] * ZOOM))

def LoadImages(path):
    images = []
    for img in os.listdir(Base_Image_Path + path):
        images.append(LoadImage(path + '/' + img))
    return images