import pygame
import random

class Ball:
    def __init__(self, x, y, speed_x, speed_y, size=10):
        self.rect = pygame.Rect(x - size//2, y - size//2, size, size)
        self.size = size
        self.dx = speed_x * random.choice([-1, 1])
        self.dy = speed_y * random.choice([-1, 1])
        self.base_speed = speed_x
        self.max_speed = 8
        
    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        
    def bounce_x(self):
        self.dx = -self.dx
        # Slight speed increase
        if abs(self.dx) < self.max_speed:
            self.dx *= 1.05
            
    def bounce_y(self):
        self.dy = -self.dy
        
    def adjust_angle(self, paddle_center_y):
        """Adjust ball angle based on where it hits the paddle"""
        # Calculate relative position (0 = center, 1 = top/bottom)
        relative_y = (self.rect.centery - paddle_center_y) / 60  # 60 = half paddle height
        # Clamp to avoid extreme angles
        relative_y = max(-1, min(1, relative_y))
        
        # Speed magnitude
        speed = (self.dx ** 2 + self.dy ** 2) ** 0.5
        # Keep speed consistent
        self.dy = relative_y * speed * 0.8
        # Ensure we don't lose horizontal speed
        self.dx = speed * 0.6 if self.dx > 0 else -speed * 0.6
        
    def reset(self, x, y):
        self.rect.center = (x, y)
        self.dx = self.base_speed * random.choice([-1, 1])
        self.dy = self.base_speed * random.choice([-1, 1])
        
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
