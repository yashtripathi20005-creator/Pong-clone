import pygame

class Score:
    def __init__(self):
        self.left_score = 0
        self.right_score = 0
        
    def reset(self):
        self.left_score = 0
        self.right_score = 0
        
    def draw(self, screen, font):
        left_text = font.render(str(self.left_score), True, (255, 255, 255))
        right_text = font.render(str(self.right_score), True, (255, 255, 255))
        
        # Position scores
        left_rect = left_text.get_rect(center=(800//4, 50))
        right_rect = right_text.get_rect(center=(800*3//4, 50))
        
        screen.blit(left_text, left_rect)
        screen.blit(right_text, right_rect)
