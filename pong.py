import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 102, 0)
TABLE_LINE = (200, 255, 200)
ORANGE = (255, 165, 0)
PLAYER_WIDTH, PLAYER_HEIGHT = 10, 100
BALL_SIZE = 15
FPS = 60

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Paddle and Ball positions
player_paddle = pygame.Rect(30, HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
ai_paddle = pygame.Rect(WIDTH - 40, HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_speed_x, ball_speed_y = 5, 5

start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

# Score tracking
player_score = 0
ai_score = 0
font = pygame.font.SysFont(None, 36)
game_over_font = pygame.font.SysFont(None, 72)

# Game state flags
game_started = False
game_over = False
fast_shot_active = False
fast_shot_timer = 0


def draw_score():
    score_text = font.render(f"{player_score} : {ai_score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))


def check_game_over():
    global game_over
    if (player_score == 7 and ai_score == 0) or (ai_score == 7 and player_score == 0):
        game_over = True
    if (player_score >= 11 and ai_score < 10) or (ai_score >= 11 and player_score < 10):
        game_over = True


def reset_game():
    global player_score, ai_score, game_over, game_started, ball_speed_x, ball_speed_y, fast_shot_active, fast_shot_timer
    player_score = 0
    ai_score = 0
    game_over = False
    game_started = False
    ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
    ball_speed_x, ball_speed_y = 5, 5
    fast_shot_active = False
    fast_shot_timer = 0


def display_winner():
    if player_score > ai_score:
        winner_text = game_over_font.render("Player Wins!", True, WHITE)
    else:
        winner_text = game_over_font.render("AI Wins!", True, WHITE)
    screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2 - 40))


def draw_table():
    screen.fill(GREEN)
    pygame.draw.rect(screen, TABLE_LINE, (0, 0, WIDTH, HEIGHT), 8)
    for y in range(0, HEIGHT, 20):
        pygame.draw.line(screen, TABLE_LINE, (WIDTH // 2, y), (WIDTH // 2, y + 10), 2)


# Game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over and start_button.collidepoint(event.pos):
                game_started = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()

    if game_started and not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_paddle.top > 0:
            player_paddle.y -= 5
        if keys[pygame.K_DOWN] and player_paddle.bottom < HEIGHT:
            player_paddle.y += 5
        if keys[pygame.K_SPACE] and not fast_shot_active:
            fast_shot_active = True
            fast_shot_timer = 60  # 1 second at 60 FPS

        if ai_paddle.centery < ball.centery and ai_paddle.bottom < HEIGHT:
            ai_paddle.y += 4
        if ai_paddle.centery > ball.centery and ai_paddle.top > 0:
            ai_paddle.y -= 4

        # Ball movement with fast shot
        speed_x = ball_speed_x * 2 if fast_shot_active else ball_speed_x
        ball.x += speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y = -ball_speed_y

        # Ball collision with paddles
        if ball.colliderect(player_paddle):
            # Spin effect
            relative_intersect_y = (player_paddle.centery - ball.centery)
            normalized_relative_intersection_y = relative_intersect_y / (PLAYER_HEIGHT / 2)
            ball_speed_y = -normalized_relative_intersection_y * 7
            ball_speed_x = -ball_speed_x
        elif ball.colliderect(ai_paddle):
            ball_speed_x = -ball_speed_x

        if ball.left <= 0:
            ai_score += 1
            ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
            ball_speed_x = -ball_speed_x
            fast_shot_active = False
            fast_shot_timer = 0
        if ball.right >= WIDTH:
            player_score += 1
            ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
            ball_speed_x = -ball_speed_x
            fast_shot_active = False
            fast_shot_timer = 0

        # Update fast shot timer
        if fast_shot_active:
            fast_shot_timer -= 1
            if fast_shot_timer <= 0:
                fast_shot_active = False

        check_game_over()

    draw_table()
    pygame.draw.rect(screen, WHITE, player_paddle)
    pygame.draw.rect(screen, WHITE, ai_paddle)
    pygame.draw.ellipse(screen, ORANGE, ball)
    draw_score()

    if not game_started and not game_over:
        start_text = font.render("Click Start to Play", True, WHITE)
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 40))

    if not game_over and not game_started:
        button_text = font.render("Start", True, BLACK)
        pygame.draw.rect(screen, WHITE, start_button)
        screen.blit(button_text, (start_button.centerx - button_text.get_width() // 2,
                                  start_button.centery - button_text.get_height() // 2))

    if game_over:
        display_winner()
        info_text = font.render("Press R to Play Again", True, WHITE)
        screen.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()
    clock.tick(FPS)