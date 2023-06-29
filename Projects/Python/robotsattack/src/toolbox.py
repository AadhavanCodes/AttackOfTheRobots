import pygame
import math

def getRotatedImage(image, rect, angle):
    new_image = pygame.transform.rotate(image, angle)
    new_rect = new_image.get_rect(center=rect.center)
    return new_image, new_rect

def angleBetweenPoints(x1, y1, x2, y2):
    x_diff = x2 - x1
    y_diff = y2 - y1
    angle = math.degrees(math.atan2(-y_diff, x_diff))
    return angle

def centeringCoords(item, screen):
    new_x = screen.get_width() / 2 - item.get_width() / 2
    new_y = screen.get_height() / 2 - item.get_height() / 2
    return new_x, new_y
    
