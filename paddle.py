import pygame

class Paddle:
    def __init__(self, x, y, speed, width=10, height=120):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.bounds = pygame.Rect(0, 0, 800, 600)  # Game window bounds
        
    def move_up(self):
        self.rect.y -= self.speed
        
    def move_down(self):
        self.rect.y += self.speed
        
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
