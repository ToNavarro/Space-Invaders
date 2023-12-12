import pygame
import sys
import random
import math
from pygame import mixer
from button import Button

pygame.init()


class SpaceObjects:
    def __init__(self, img, x, y, x_movement=0, y_movement=0):
        self.img = pygame.image.load(img)
        self.x = x
        self.y = y
        self.x_movement = x_movement
        self.y_movement = y_movement

    def draw(self):
        screen.blit(self.img, (self.x, self.y))


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font/TriakisFont-Regular.otf", size)


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

# SCORE
score_value = 0
score_font = get_font(40)
score_xy = (10, 10)

# GAME OVER
over_font = get_font(80)
over_xy = (200, 250)
over_text = "GAME OVER"


def create_objects(enemy_num, enemy_speed, bullet_speed):
    # PLAYER -> Icon by FLATICON (https://www.flaticon.com/)
    player = SpaceObjects("images/player.png", 370, 480)

    # ENEMIES -> Icon by Icons8 (https://icons8.com)
    num_of_enemies = enemy_num
    enemies = [SpaceObjects("images/enemy3.png", random.randint(0, 736), random.randint(50, 150),
                            x_movement=random.choice([enemy_speed, -enemy_speed]),
                            y_movement=40) for _ in range(num_of_enemies)]

    # BULLET -> Icon by FLATICON (https://www.flaticon.com/)
    bullet = SpaceObjects("images/bullet.png", 0, 480, y_movement=bullet_speed)
    bullet.state = "ready"
    bullet.sound = mixer.Sound("sounds/laser.wav")
    bullet.collision_sound = mixer.Sound("sounds/explosion.wav")

    def fire_bullet(x, y):
        bullet.state = "fired"
        screen.blit(bullet.img, (x + 16, y + 10))

    return player, enemies, bullet, fire_bullet


def get_score_text():
    return f"Score: {score_value}"


def show_text(font, text, xy):
    formatted_text = font.render(text, True, (148, 0, 255))
    screen.blit(formatted_text, dest=xy)


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    if distance < 27:
        return True
    else:
        return False


# GAME LOOP
def main_loop(enemy_num, enemy_speed, bullet_speed, player_speed):

    player, enemies, bullet, fire_bullet = create_objects(enemy_num, enemy_speed, bullet_speed)

    global score_value
    run = True
    while run:
        screen.fill((0, 0, 0))
        screen.blit(background, (-100, 0))

        # Buttons
        play_mouse_pos = pygame.mouse.get_pos()
        menu_button = Button(image=None, pos=(100, 575),
                             text_input="MENU", font=get_font(60), base_color="#AED2FF", hovering_color="#27005D")
        menu_button.change_color(play_mouse_pos)
        menu_button.update(screen)

        quit_button = Button(image=None, pos=(700, 575),
                             text_input="QUIT", font=get_font(60), base_color="#AED2FF", hovering_color="#F90716")
        quit_button.change_color(play_mouse_pos)
        quit_button.update(screen)

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
                for enemy1 in enemies:
                    enemy1.y = 2000
                show_text(over_font, over_text, over_xy)
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.x_movement = -player_speed
                if event.key == pygame.K_RIGHT:
                    player.x_movement = player_speed
                if event.key == pygame.K_SPACE and bullet.state == "ready":
                    bullet.sound.play()
                    bullet.x = player.x
                    fire_bullet(bullet.x, bullet.y)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.x_movement = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.check_for_input(play_mouse_pos):
                    main_menu()
                if quit_button.check_for_input(play_mouse_pos):
                    pygame.quit()
                    sys.exit()

        player.x += player.x_movement
        for enemy in enemies:
            enemy.x += enemy.x_movement
        show_text(score_font, get_score_text(), score_xy)

        pygame.display.update()


def level_1():
    main_loop(enemy_num=6, enemy_speed=2, bullet_speed=15, player_speed=2.5)


def level_2():
    main_loop(enemy_num=8, enemy_speed=2.5, bullet_speed=15, player_speed=3)


def level_3():
    main_loop(enemy_num=10, enemy_speed=3, bullet_speed=20, player_speed=3.5)


def main_menu():
    while True:
        screen.blit(background, (-100, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        title_text = get_font(100).render("SPACE INVADERS", True, "#9400FF")
        title_rect = title_text.get_rect(center=(390, 75))

        level_1_btn = Button(image=pygame.image.load("images/level_rect2.png"), pos=(390, 175),
                             text_input="Level 1", font=get_font(70), base_color="#AED2FF", hovering_color="#27005D")
        level_2_btn = Button(image=pygame.image.load("images/level_rect2.png"), pos=(390, 275),
                             text_input="Level 2", font=get_font(70), base_color="#AED2FF", hovering_color="#27005D")
        level_3_btn = Button(image=pygame.image.load("images/level_rect2.png"), pos=(390, 375),
                             text_input="Level 3", font=get_font(70), base_color="#AED2FF", hovering_color="#27005D")
        quit_btn = Button(image=pygame.image.load("images/level_rect2.png"), pos=(390, 500),
                          text_input="QUIT", font=get_font(70), base_color="#AED2FF", hovering_color="#F90716")

        screen.blit(title_text, title_rect)

        for button in [level_1_btn, level_2_btn, level_3_btn, quit_btn]:
            button.change_color(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level_1_btn.check_for_input(menu_mouse_pos):
                    level_1()
                if level_2_btn.check_for_input(menu_mouse_pos):
                    level_2()
                if level_3_btn.check_for_input(menu_mouse_pos):
                    level_3()
                if quit_btn.check_for_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


main_menu()

pygame.quit()
sys.exit()
