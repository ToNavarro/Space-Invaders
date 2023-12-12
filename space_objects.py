import pygame


class SpaceObjects:
    def __init__(self, img, screen, x, y, x_movement=0, y_movement=0):
        self.img = pygame.image.load(img)
        self.x = x
        self.y = y
        self.x_movement = x_movement
        self.y_movement = y_movement
        self.screen = screen

    def draw(self):
        self.screen.blit(self.img, (self.x, self.y))
