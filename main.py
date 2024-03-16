import pygame, random


pygame.init()


WINDOW_WIDTH = 945
WINDOW_HEIGHT = 600

display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Clown game")



# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set game values
PLAYER_STARTING_LIVES = 5
CLOWN_START_VELOCITY = 3
CLOWN_ACCELERATION = 0.5

score = 0
player_lives = PLAYER_STARTING_LIVES

clown_velocity = CLOWN_START_VELOCITY
clown_dx = random.choice([-1, 1])
clown_dy = random.choice([-1, 1])

# Set colors
WHITE = (255, 255, 255)
BLUE = (2, 176, 208)
YELLOW = (247, 232, 29)
GREEN = (0, 255, 0)

# Set fonts
font = pygame.font.Font("assets/Franxurter.ttf", 32)

# Set text
title_text = font.render("Catch this Clown", True, BLUE)
title_text_rect = title_text.get_rect()
title_text_rect.topleft = (50, 10)

score_text = font.render("Score: " + str(score), True, YELLOW)
score_text_rect = score_text.get_rect()
score_text_rect.topright = (WINDOW_WIDTH - 50, 10)

lives_text = font.render("Lives: " + str(player_lives), True, YELLOW)
lives_text_rect = lives_text.get_rect()
lives_text_rect.topright = (WINDOW_WIDTH - 50, 50)

game_over_text = font.render("GAME OVER", True, YELLOW, BLUE)
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Click to play again", True, BLUE, YELLOW)
continue_text_rect = continue_text.get_rect()
continue_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

# Set audio
click_sound = pygame.mixer.Sound("assets/click_sound.wav")
miss_sound = pygame.mixer.Sound("assets/miss_sound.wav")
pygame.mixer.music.load("assets/ctc_background_music.wav")

# Set img
bg_image = pygame.image.load("assets/background.png")
bg_image_rect = bg_image.get_rect()
bg_image_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

clown_image = pygame.image.load("assets/clown.png")
clown_image_rect = clown_image.get_rect()
clown_image_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

# main game loop

pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Click monitor
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x = event.pos[0]
            mouse_y = event.pos[1]

            # the clown clicked?
            if clown_image_rect.collidepoint(mouse_x, mouse_y):
                click_sound.set_volume(0.5)
                click_sound.play()
                score += 1
                clown_velocity += CLOWN_ACCELERATION

                # change direction
                prev_dx = clown_dx
                prev_dy = clown_dy
                while prev_dx == clown_dx and prev_dy == clown_dy:
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])

            else:
                miss_sound.play()
                player_lives -= 1

    # Move the clown
    clown_image_rect.x += clown_dx * clown_velocity
    clown_image_rect.y += clown_dy * clown_velocity

    # bounce
    if clown_image_rect.left <= 0 or clown_image_rect.right >= WINDOW_WIDTH:
        clown_dx = -1 * clown_dx
    if clown_image_rect.top <= 0 or clown_image_rect.bottom >= WINDOW_HEIGHT:
        clown_dy = -1 * clown_dy

    # Update texts
    score_text = font.render("Score: " + str(score), True, YELLOW)
    lives_text = font.render("Lives: " + str(player_lives), True, YELLOW)

    # Game over check
    if player_lives == 0:
        display_surface.blit(game_over_text, game_over_text_rect)
        display_surface.blit(continue_text, continue_text_rect)
        pygame.display.update()

        pygame.mixer.music.stop()
        in_pause = True
        while in_pause:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:

                    player_lives = PLAYER_STARTING_LIVES
                    clown_velocity = CLOWN_START_VELOCITY
                    score = 0
                    clown_image_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT //2)

                    pygame.mixer.music.play(-1, 0.0)
                    in_pause = False

                if event.type == pygame.QUIT:
                    in_pause = False
                    running = False


    # Blit bg
    display_surface.blit(bg_image, bg_image_rect)

    # Blit HUD
    display_surface.blit(title_text, title_text_rect)
    display_surface.blit(score_text, score_text_rect)
    display_surface.blit(lives_text, lives_text_rect)

    # Blit assets
    display_surface.blit(clown_image, clown_image_rect)

    # Update display and clock tick
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()