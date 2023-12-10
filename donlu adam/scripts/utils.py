import pygame
import os

Base_Image_Path = 'my pygame projects/data/images/'

def LoadImage(path):
    img = pygame.image.load(Base_Image_Path + path).convert_alpha()
    img.set_colorkey((0, 0, 0))
    return img

def LoadImages(path):
    images = []
    for img in os.listdir(Base_Image_Path + path):
        images.append(LoadImage(path + '/' + img))
    return images