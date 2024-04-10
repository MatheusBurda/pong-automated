import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LEFT_PADDLE_COLOR = (46, 149, 211)  # #2e95d3
RIGHT_PADDLE_COLOR = (116, 69, 90)  # #74455a
FONT_SIZE = 36
FONT_COLOR = WHITE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Set up the fonts
font = pygame.font.Font(None, FONT_SIZE)

# Set up the clock
clock = pygame.time.Clock()

# Set up the paddles
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 3

# Set up the ball
BALL_SIZE = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Set up initial positions
left_paddle_pos = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle_pos = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball_pos = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, random.randint(0, HEIGHT - BALL_SIZE), BALL_SIZE, BALL_SIZE)  # Random vertical spawn

# Set up scores
player1_score = 0
player2_score = 0

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Main game loop
running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()

    # Move paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        right_paddle_pos.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN]:
        right_paddle_pos.y += PADDLE_SPEED

    # Ensure paddles are within screen boundaries
    left_paddle_pos.y = min(max(left_paddle_pos.y, 0), HEIGHT - PADDLE_HEIGHT)
    right_paddle_pos.y = min(max(right_paddle_pos.y, 0), HEIGHT - PADDLE_HEIGHT)

    # Computer AI for left paddle
    if ball_pos.left < WIDTH / 2:
        if ball_pos.centery < left_paddle_pos.centery:
            left_paddle_pos.y -= PADDLE_SPEED
        elif ball_pos.centery > left_paddle_pos.centery:
            left_paddle_pos.y += PADDLE_SPEED

    # Computer AI for right paddle
    if ball_pos.right > WIDTH / 2:
        if ball_pos.centery < right_paddle_pos.centery:
            right_paddle_pos.y -= PADDLE_SPEED
        elif ball_pos.centery > right_paddle_pos.centery:
            right_paddle_pos.y += PADDLE_SPEED

    # Ball movement
    ball_pos.x += BALL_SPEED_X
    ball_pos.y += BALL_SPEED_Y

    # Collision detection with walls
    if ball_pos.top <= 0 or ball_pos.bottom >= HEIGHT:
        BALL_SPEED_Y *= -1
    if ball_pos.left <= 0:
        player2_score += 1
        ball_pos.x = WIDTH // 2 - BALL_SIZE // 2
        ball_pos.y = random.randint(0, HEIGHT - BALL_SIZE)  # Random vertical spawn
        BALL_SPEED_X = 5 * random.choice([-1, 1])
        BALL_SPEED_Y = 5 * random.choice([-1, 1])
    if ball_pos.right >= WIDTH:
        player1_score += 1
        ball_pos.x = WIDTH // 2 - BALL_SIZE // 2
        ball_pos.y = random.randint(0, HEIGHT - BALL_SIZE)  # Random vertical spawn
        BALL_SPEED_X = 5 * random.choice([-1, 1])
        BALL_SPEED_Y = 5 * random.choice([-1, 1])

    # Collision detection with paddles
    if ball_pos.colliderect(left_paddle_pos) or ball_pos.colliderect(right_paddle_pos):
        BALL_SPEED_X *= -1

    # Draw paddles and ball
    pygame.draw.rect(screen, LEFT_PADDLE_COLOR, left_paddle_pos)
    pygame.draw.rect(screen, RIGHT_PADDLE_COLOR, right_paddle_pos)
    pygame.draw.ellipse(screen, WHITE, ball_pos)

    # Draw score
    draw_text(str(player1_score), font, LEFT_PADDLE_COLOR, screen, WIDTH // 4, HEIGHT - FONT_SIZE)
    draw_text(str(player2_score), font, RIGHT_PADDLE_COLOR, screen, 3 * WIDTH // 4, HEIGHT - FONT_SIZE)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit pygame
pygame.quit()
sys.exit()
