import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1180, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_RADIUS = 10
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SPEED = 5
PADDLE_SPEED = 7
GAME_FONT = pygame.font.Font(None, 36)

# Load sound effects
pygame.mixer.init()
hit_sound = pygame.mixer.Sound("./Sound Effects/metal-hit-5-193273.mp3")
game_over_sound = pygame.mixer.Sound("./Sound Effects/game-over-arcade-6435.mp3")

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Add a level variable and define a list of levels with corresponding ball speeds
level = 1
LEVELS = {
    1: 5,
    2: 7,
    3: 9
}

# Create paddles
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = PADDLE_SPEED

    def move_up(self):
        self.rect.y -= self.speed
        if self.rect.top < 0:
            self.rect.top = 0

    def move_down(self):
        self.rect.y += self.speed
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Create ball
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = LEVELS[level] * random.choice([1, -1])
        self.speed_y = LEVELS[level] * random.choice([1, -1])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Collision detection with paddles
        if self.rect.colliderect(player_paddle.rect) or self.rect.colliderect(ai_paddle.rect):
            self.speed_x *= -1
            hit_sound.play()

        # Collision detection with top and bottom walls
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

# Add a power-up class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 0, 0))  # Power-up color (red)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.duration = 5000  # Duration of power-up effect (in milliseconds)

    def apply_power_up(self, paddle):
        paddle.rect.inflate_ip(0, 20)  # Increase paddle height by 20 pixels

# Create a power-up sprite group
power_ups = pygame.sprite.Group()

# Create sprites
player_paddle = Paddle(50, HEIGHT // 2)
ai_paddle = Paddle(WIDTH - 50, HEIGHT // 2)
ball = Ball()

all_sprites = pygame.sprite.Group()
all_sprites.add(player_paddle, ai_paddle, ball)

# Score variables
player_score = 0
ai_score = 0

# Game over notification
def show_game_over(winner):
    game_over_sound.play()
    text = GAME_FONT.render(f"Game Over! {winner} wins!", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    # Display scores
    score_text = GAME_FONT.render(f"Player: {player_score}  AI: {ai_score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(score_text, score_rect)

    restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)
    pygame.draw.rect(screen, WHITE, restart_button)
    restart_text = GAME_FONT.render("Restart", True, BLACK)
    restart_text_rect = restart_text.get_rect(center=restart_button.center)
    screen.blit(restart_text, restart_text_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    return True

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    game_over = False
    ball.rect.center = (WIDTH // 2, HEIGHT // 2)
    ball.speed_x = LEVELS[level] * random.choice([1, -1])
    ball.speed_y = LEVELS[level] * random.choice([1, -1])

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_paddle.move_up()
        if keys[pygame.K_DOWN]:
            player_paddle.move_down()

        # AI paddle movement with simple predictive behavior
        if ball.rect.centery < ai_paddle.rect.centery:
            ai_paddle.move_up()
        elif ball.rect.centery > ai_paddle.rect.centery:
            ai_paddle.move_down()

        if random.random() < 0.005:
            power_up = PowerUp()
            power_ups.add(power_up)

        # Update power-ups
        power_ups.update()

        for power_up in pygame.sprite.spritecollide(player_paddle, power_ups, True):
            power_up.apply_power_up(player_paddle)
            pygame.time.set_timer(pygame.USEREVENT, power_up.duration)

        # Check for timer event to reset paddle size after power-up duration expires
        if event.type == pygame.USEREVENT:
            player_paddle.rect.inflate_ip(0, -20)  # Reset paddle size

        # Update
        all_sprites.update()

        # Ball misses the paddle
        if ball.rect.right < 0:
            game_over = True
            ai_score += 1
            winner = "AI"
        elif ball.rect.left > WIDTH:
            game_over = True
            player_score += 1
            winner = "Player"

        # Draw
        screen.fill(BLACK)
        pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
        all_sprites.draw(screen)

        # Display scores during gameplay
        score_text = GAME_FONT.render(f"Player: {player_score}  AI: {ai_score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    if show_game_over(winner):
        player_score = 0
        ai_score = 0
        continue

pygame.quit()