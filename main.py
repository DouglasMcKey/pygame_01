import sys

import pygame
import time
import random

# Initialize the font module.
pygame.init()

# Game window settings.
WIDTH, HEIGHT = 1000, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter 0.1")

MENU_FONT = pygame.font.SysFont("cosmicsans", 30)
GAME_FONT = pygame.font.SysFont("cosmicsans", 24)
BG = pygame.transform.scale(
    pygame.image.load("static/images/background_level_3.jpg"), (WIDTH, HEIGHT)
)
FPS = 60

# Player settings.
PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_VELOCITY = 40, 60, 6

# Bullet settings.
BULLET_WIDTH, BULLET_HEIGHT, BULLET_VELOCITY = 30, 5, -15
MAX_BULLET_COUNT = 10

# Star settings.
STAR_WIDTH, STAR_HEIGHT, = 10, 20

# Score settings.
LEVEL_ONE_SCORE = 200
LEVEL_TWO_SCORE = 400
LEVEL_THREE_SCORE = 600
LEVEL_FOUR_SCORE = 800
LEVEL_FIVE_SCORE = 1000
LEVEL_SIX_SCORE = 1250
LEVEL_SEVEN_SCORE = 1500
LEVEL_EIGHT_SCORE = 1750
LEVEL_NINE_SCORE = 2000
LEVEL_TEN_SCORE = 2500


def print_fonts():
    fonts = pygame.font.get_fonts()
    for f in fonts:
        print(f)


def draw_main_menu_options(start_game_surface, start_game_rect, exit_program_surface, exit_program_rect):
    SCREEN.blit(start_game_surface, start_game_rect)
    pygame.draw.rect(SCREEN, (255, 255, 255), start_game_rect, 1)
    SCREEN.blit(exit_program_surface, exit_program_rect)
    pygame.draw.rect(SCREEN, (255, 255, 255), exit_program_rect, 1)


def draw_game(player, elapsed_time, stars, bullets, player_score, level):
    SCREEN.blit(BG, (0, 0))

    time_text = GAME_FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    SCREEN.blit(time_text, (10, 10))

    player_score_text = GAME_FONT.render(f"SCORE: {player_score}", 1, "white")
    SCREEN.blit(player_score_text, (10, 50))

    level_text = GAME_FONT.render(f"Level: {level}", 1, "white")
    SCREEN.blit(level_text, (10, 90))

    pygame.draw.rect(SCREEN, "red", player)

    # Draw the falling stars.
    for star in stars:
        pygame.draw.rect(SCREEN, "white", star)

    # Draw the bullets.
    for bullet in bullets[:]:
        pygame.draw.rect(SCREEN, "green", bullet)

    pygame.display.update()


def start_program():
    program_running = True
    in_play = False

    # Text surfaces: where text will be typed.
    start_game_surface = MENU_FONT.render("<< Start Game >>", True, (255, 255, 255))
    exit_program_surface = MENU_FONT.render("<< Exit >>", True, (255, 255, 255))

    # Text rectangles: to place a border around the text.
    start_game_rect = start_game_surface.get_rect(topleft=(
        WIDTH / 2 - start_game_surface.get_width() / 2,
        HEIGHT / 2 - start_game_surface.get_height() / 2 - 30
    ))

    exit_program_rect = exit_program_surface.get_rect(topleft=(
        WIDTH / 2 - exit_program_surface.get_width() / 2,
        HEIGHT / 2 - (exit_program_surface.get_height() / 2) + 30
    ))

    # Game variables.
    # Set the game clock to assist in controlling the game speed.
    clock = pygame.time.Clock()

    # Set up the time tracking variables.
    start_time = time.time()

    # Instantiate the player.
    player = pygame.Rect(
        WIDTH / 2 - PLAYER_WIDTH / 2, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT
    )
    player_score = 0
    level = 1

    # Falling stars.
    star_add_increment = 2000
    star_count = 0
    stars = []
    star_value = 10
    star_velocity = 2
    star_n = 3
    play_hit = False

    # Player bullets.
    bullets = []

    while program_running:

        if in_play is True:
            # Player movement.
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x - PLAYER_VELOCITY >= 0:
                player.x -= PLAYER_VELOCITY
            if keys[pygame.K_RIGHT] and player.x + player.width <= WIDTH:
                player.x += PLAYER_VELOCITY

            # Generate falling stars.
            star_count += clock.tick(FPS)
            elapsed_time = time.time() - start_time

            if star_count > star_add_increment:
                for _ in range(star_n):
                    star_x = random.randint(0, WIDTH - STAR_WIDTH)
                    star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                    stars.append(star)

                star_add_increment = max(200, star_add_increment - 50)
                star_count = 0

            # Star movement.
            for star in stars[:]:
                star.y += star_velocity
                if star.y > HEIGHT:
                    stars.remove(star)
                elif star.y >= player.y and star.colliderect(player):
                    stars.remove(star)
                    play_hit = True
                    break

            # Star hits player.
            if play_hit is True:
                lost_text = MENU_FONT.render("You crashed into a star!", 1, "white")
                SCREEN.blit(lost_text, (
                    WIDTH / 2 - lost_text.get_width() / 2,
                    HEIGHT / 2 - lost_text.get_height() / 2
                ))
                pygame.display.update()
                pygame.time.delay(4000)
                start_program()

            # Generate player bullets.
            if keys[pygame.K_SPACE]:
                bullet_y = HEIGHT - PLAYER_HEIGHT + BULLET_HEIGHT  # Bullet fired from y location.
                bullet = pygame.Rect(
                    player.x + ((PLAYER_WIDTH - BULLET_WIDTH) / 2), bullet_y, BULLET_WIDTH, BULLET_HEIGHT
                )
                bullets.append(bullet)

            # Bullet movement.
            for bullet in bullets[:]:
                bullet.y += BULLET_VELOCITY
                if bullet.y > HEIGHT:
                    bullets.remove(bullet)

                # Bullet hits star.
                for star in stars[:]:
                    if bullet.colliderect(star):
                        try:
                            stars.remove(star)
                            bullets.remove(bullet)
                            player_score += star_value
                        except Exception:
                            pass

            # Difficulty progression.
            if player_score >= LEVEL_ONE_SCORE:
                star_velocity = 3
                level = 2

            if player_score >= LEVEL_TWO_SCORE:
                star_velocity = 6
                level = 3

            if player_score >= LEVEL_THREE_SCORE:
                star_value = 15
                star_velocity = 8
                star_n = 4
                level = 4

            if player_score >= LEVEL_FOUR_SCORE:
                star_velocity = 10
                level = 6

            if player_score >= LEVEL_FIVE_SCORE:
                star_velocity = 12
                level = 7

            if player_score >= LEVEL_SIX_SCORE:
                star_value = 20
                star_velocity = 14
                star_n = 5
                level = 8

            if player_score >= LEVEL_SEVEN_SCORE:
                star_velocity = 16
                level = 9

            if player_score >= LEVEL_EIGHT_SCORE:
                star_value = 25
                star_velocity = 18
                star_n = 6
                level = 10

            draw_game(player, elapsed_time, stars, bullets, player_score, level)

        else:
            if in_play is False:
                SCREEN.fill((0, 0, 0))
            draw_main_menu_options(
                start_game_surface, start_game_rect,
                exit_program_surface, exit_program_rect
            )

        for event in pygame.event.get():
            # Check for the event quit.
            if event.type == pygame.QUIT:
                program_running = False

            if not in_play:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_game_rect.collidepoint(event.pos):
                        in_play = True

                    if exit_program_rect.collidepoint(event.pos):
                        program_running = False

        pygame.display.update()

    pygame.quit()
    sys.exit()


def main():
    # print_fonts()
    start_program()

    print("Done!")


if __name__ == "__main__":
    main()
