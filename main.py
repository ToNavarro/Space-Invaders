import pygame
import random
import math
from pygame import mixer
from space_objects import SpaceObjects

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# SCREEN
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("images/ufo.png")  # Icon by FLATICON (https://www.flaticon.com/)
pygame.display.set_icon(icon)

# BACKGROUND
background = pygame.image.load("images/backg.png")  # image from FREEPIK (https://www.freepik.com/)
mixer.music.load("sounds/background.wav")
mixer.music.play(-1)

# PLAYER
# Icon by FLATICON (https://www.flaticon.com/)
player = SpaceObjects("images/player.png", screen, 370, 480)

# ENEMIES
# Enemy Icon by Icons8 (https://icons8.com)
num_of_enemies = 6
enemies = [SpaceObjects("images/enemy3.png", screen, random.randint(0, 736), random.randint(50, 150),
                        x_movement=random.choice([1.5, -1.5]), y_movement=40) for enemy in range(num_of_enemies)]

# BULLET
# Icon by FLATICON (https://www.flaticon.com/)
bullet = SpaceObjects("images/bullet.png", screen, 0, 480, y_movement=10)
bullet.state = "ready"
bullet.sound = mixer.Sound("sounds/laser.wav")
bullet.collision_sound = mixer.Sound("sounds/explosion.wav")


# SCORE
score_value = 0
font = pygame.font.Font("font/TriakisFont-Regular.otf", 40)
text_x = 10
text_y = 10

over_font = pygame.font.Font("font/TriakisFont-Regular.otf", 80)


def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, (148, 0, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render(f"GAME OVER", True, (148, 0, 255))
    screen.blit(over_text, (200, 250))


def fire_bullet(x, y):
    bullet.state = "fired"
    screen.blit(bullet.img, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    if distance < 27:
        return True
    else:
        return False


# GAME LOOP
run = True
while run:
    screen.fill((0, 0, 0))
    screen.blit(background, (-100, 0))

    # Player movement
    if player.x <= 0:
        player.x = 0
    if player.x >= 736:
        player.x = 736
    player.draw()

    # Enemy movement
    for enemy in enemies:
        # Game Over
        if enemy.y > 440:
            for enemy in enemies:
                enemy.y = 2000
            game_over_text()
            break

        if enemy.x <= 0 or enemy.x >= 736:
            enemy.x_movement *= -1
            enemy.y += enemy.y_movement
        enemy.draw()

        # Collision
        collision = is_collision(enemy.x, enemy.y, bullet.x, bullet.y)
        if collision:
            bullet.collision_sound.play()
            bullet.y = 480
            bullet.state = "ready"
            score_value += 1

            enemy.x = random.randint(0, 736)
            enemy.y = random.randint(50, 150)

    # Bullet Movement
    if bullet.y <= 0:
        bullet.y = 480
        bullet.state = "ready"

    if bullet.state == "fired":
        fire_bullet(bullet.x, bullet.y)
        bullet.y -= bullet.y_movement

    # key = pygame.key.get_pressed()
    #
    # if key[pygame.K_a]:
    #     player_x -= 0.5
    # if key[pygame.K_d]:
    #     player_x += 0.5
    # if key[pygame.K_w]:
    #     player_y -= 0.5
    # if key[pygame.K_s]:
    #     player_y += 0.5

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x_movement = -2
            if event.key == pygame.K_RIGHT:
                player.x_movement = 2
            if event.key == pygame.K_SPACE and bullet.state == "ready":
                bullet.sound.play()
                bullet.x = player.x
                fire_bullet(bullet.x, bullet.y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.x_movement = 0

    player.x += player.x_movement
    for enemy in enemies:
        enemy.x += enemy.x_movement
    show_score(text_x, text_y)

    pygame.display.update()

pygame.quit()
