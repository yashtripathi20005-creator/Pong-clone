import pygame
import sys
from paddle import Paddle
from ball import Ball
from score import Score

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_SPEED = 5
BALL_SPEED_X = 4
BALL_SPEED_Y = 4

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pong Clone")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        
        # Create game objects
        self.left_paddle = Paddle(30, WINDOW_HEIGHT//2 - 60, PADDLE_SPEED)
        self.right_paddle = Paddle(WINDOW_WIDTH - 40, WINDOW_HEIGHT//2 - 60, PADDLE_SPEED)
        self.ball = Ball(WINDOW_WIDTH//2, WINDOW_HEIGHT//2, BALL_SPEED_X, BALL_SPEED_Y)
        self.score = Score()
        
        # Game state
        self.running = True
        self.paused = False
        self.winner = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                if event.key == pygame.K_r and self.winner:
                    self.reset_game()

    def reset_game(self):
        self.left_paddle.rect.y = WINDOW_HEIGHT//2 - 60
        self.right_paddle.rect.y = WINDOW_HEIGHT//2 - 60
        self.ball.reset(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
        self.score.reset()
        self.winner = None
        self.paused = False

    def update(self):
        if self.paused or self.winner:
            return
            
        # Get keyboard input
        keys = pygame.key.get_pressed()
        
        # Left paddle controls (W/S)
        if keys[pygame.K_w]:
            self.left_paddle.move_up()
        if keys[pygame.K_s]:
            self.left_paddle.move_down()
            
        # Right paddle controls (Arrow keys)
        if keys[pygame.K_UP]:
            self.right_paddle.move_up()
        if keys[pygame.K_DOWN]:
            self.right_paddle.move_down()
            
        # Keep paddles in bounds
        self.left_paddle.rect.clamp_ip(self.left_paddle.bounds)
        self.right_paddle.rect.clamp_ip(self.right_paddle.bounds)
        
        # Update ball
        self.ball.update()
        
        # Ball collision with top and bottom walls
        if self.ball.rect.top <= 0 or self.ball.rect.bottom >= WINDOW_HEIGHT:
            self.ball.bounce_y()
        
        # Ball collision with paddles
        if self.ball.rect.colliderect(self.left_paddle.rect) and self.ball.dx < 0:
            self.ball.bounce_x()
            # Add some angle based on where the paddle was hit
            self.ball.adjust_angle(self.left_paddle.rect.centery)
            
        if self.ball.rect.colliderect(self.right_paddle.rect) and self.ball.dx > 0:
            self.ball.bounce_x()
            self.ball.adjust_angle(self.right_paddle.rect.centery)
        
        # Scoring
        if self.ball.rect.left <= 0:
            self.score.right_score += 1
            self.ball.reset(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
            if self.score.right_score >= 5:
                self.winner = "Right Player"
                
        if self.ball.rect.right >= WINDOW_WIDTH:
            self.score.left_score += 1
            self.ball.reset(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
            if self.score.left_score >= 5:
                self.winner = "Left Player"

    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw center line
        pygame.draw.aaline(self.screen, WHITE, 
                          (WINDOW_WIDTH//2, 0), 
                          (WINDOW_WIDTH//2, WINDOW_HEIGHT))
        
        # Draw center circle
        pygame.draw.circle(self.screen, WHITE, 
                          (WINDOW_WIDTH//2, WINDOW_HEIGHT//2), 
                          75, 1)
        
        # Draw paddles and ball
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        
        # Draw score
        self.score.draw(self.screen, self.font)
        
        # Draw pause text
        if self.paused:
            pause_text = self.small_font.render("PAUSED - Press SPACE to resume", True, WHITE)
            text_rect = pause_text.get_rect(center=(WINDOW_WIDTH//2, 50))
            self.screen.blit(pause_text, text_rect)
        
        # Draw winner text
        if self.winner:
            win_text = self.font.render(f"{self.winner} Wins!", True, WHITE)
            text_rect = win_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
            self.screen.blit(win_text, text_rect)
            
            restart_text = self.small_font.render("Press R to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 20))
            self.screen.blit(restart_text, restart_rect)
        
        # Draw controls
        controls = self.small_font.render("W/S | UP/DOWN | SPACE:Pause | ESC:Quit", True, WHITE)
        controls_rect = controls.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 20))
        self.screen.blit(controls, controls_rect)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
