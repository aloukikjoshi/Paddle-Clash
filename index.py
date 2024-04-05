import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1180, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_RADIUS = 10
BALL_SPEED = 5
PADDLE_SPEED = 7
GAME_FONT = pygame.font.Font(None, 36)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Create paddles
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 100))
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
        self.speed_x = BALL_SPEED * random.choice([1, -1])
        self.speed_y = BALL_SPEED * random.choice([1, -1])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1
        if pygame.sprite.collide_mask(ball, player_paddle) or pygame.sprite.collide_mask(ball, ai_paddle):
            self.speed_x *= -1

# Create sprites
player_paddle = Paddle(50, HEIGHT // 2)
ai_paddle = Paddle(WIDTH - 50, HEIGHT // 2)
ball = Ball()

all_sprites = pygame.sprite.Group()
all_sprites.add(player_paddle, ai_paddle, ball)

# Game over notification
def show_game_over(winner):
    text = GAME_FONT.render(f"Game Over! {winner} wins!", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
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
    ball.speed_x = BALL_SPEED * random.choice([1, -1])
    ball.speed_y = BALL_SPEED * random.choice([1, -1])

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

        # AI paddle movement
        if ball.rect.centery < ai_paddle.rect.centery:
            ai_paddle.move_up()
        elif ball.rect.centery > ai_paddle.rect.centery:
            ai_paddle.move_down()

        # Update
        all_sprites.update()

        # Ball misses the paddle
        if ball.rect.right < 0:
            game_over = True
            winner = "AI"
        elif ball.rect.left > WIDTH:
            game_over = True
            winner = "Player"

        # Draw
        screen.fill(BLACK)
        pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    if show_game_over(winner):
        continue

pygame.quit()
