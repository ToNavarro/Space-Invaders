import pygame
import random
import math
from pygame import mixer

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
player_img = pygame.image.load("images/player.png")  # Icon by FLATICON (https://www.flaticon.com/)
player_x = 370
player_y = 480
player_x_movement = 0

# ENEMIES
ENEMY_IMG = pygame.image.load("images/enemy3.png")  # Enemy Icon by Icons8 (https://icons8.com)
enemy_x = []
enemy_y = []
enemy_x_movement = []
ENEMY_Y_MOVEMENT = 40
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemy_x_movement.append(random.choice([1.5, -1.5]))


# BULLET
bullet_img = pygame.image.load("images/bullet.png")  # Icon by FLATICON (https://www.flaticon.com/)
bullet_sound = mixer.Sound("sounds/laser.wav")
collision_sound = mixer.Sound("sounds/explosion.wav")
bullet_x = 0
bullet_y = 480
bullet_x_movement = 0
bullet_y_movement = 10
# states = ["ready", "fired"]
bullet_state = "ready"

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


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y):
    screen.blit(ENEMY_IMG, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fired"
    screen.blit(bullet_img, (x + 16, y + 10))


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
    if player_x <= 0:
        player_x = 0
    if player_x >= 736:
        player_x = 736
    player(player_x, player_y)

    # Enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        if enemy_x[i] <= 0 or enemy_x[i] >= 736:
            enemy_x_movement[i] *= -1
            enemy_y[i] += ENEMY_Y_MOVEMENT
        enemy(enemy_x[i], enemy_y[i])

    # if enemy_x <= 0 or enemy_x >= 736:
    #     enemy_x_movement *= -1
    #     enemy_y += enemy_y_movement
    # enemy(enemy_x, enemy_y)
        # Collision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            collision_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1

            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)

    # Bullet Movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fired":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_movement

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
                player_x_movement = -2
            if event.key == pygame.K_RIGHT:
                player_x_movement = 2
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_sound.play()
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_movement = 0

    player_x += player_x_movement
    for i in range(num_of_enemies):
        enemy_x[i] += enemy_x_movement[i]
    show_score(text_x, text_y)

    pygame.display.update()

pygame.quit()
