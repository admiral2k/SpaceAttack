import pygame
import os

pygame.font.init()
pygame.mixer.init()

FPS = 60
WIDTH, HEIGHT = 900, 500
VELOCITY = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

MAX_HEALTH = 10
HEALTH_FONT = pygame.font.SysFont("arial", 40, True)
WINNER_FONT = pygame.font.SysFont("Arial", 100, True)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BULLET_VELOCITY = 7
MAX_BULLETS = 3
BULLET_WIDTH, BULLET_HEIGHT = 10, 6

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SpaceAttack!")
BARRIER = pygame.Rect((WIDTH - 10) / 2, 0, 10, HEIGHT)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
YELLOW_GLOW = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "yellow_glow.png")),
                                     (SPACESHIP_HEIGHT + 10, SPACESHIP_WIDTH + 10))

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)
RED_GLOW = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "red_glow.png")),
                                  (SPACESHIP_HEIGHT + 10, SPACESHIP_WIDTH + 10))

BACKGROUND = pygame.image.load(os.path.join("Assets", "space.png"))
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

WINNER_BLACKOUT = pygame.image.load(os.path.join("Assets", "black_alpha.png"))
WINNER_BLACKOUT = pygame.transform.scale(WINNER_BLACKOUT, (WIDTH, HEIGHT))

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))


def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    yellow_health_bar_backside = pygame.Rect(yellow.x, yellow.y + yellow.height + 5, yellow.width, 5)
    red_health_bar_backside = pygame.Rect(red.x, red.y + red.height + 5, red.width, 5)

    yellow_health_bar = pygame.Rect(yellow.x, yellow.y + yellow.height + 5, yellow.width / MAX_HEALTH * yellow_health, 5)
    red_health_bar = pygame.Rect(red.x, red.y + red.height + 5, red.width / MAX_HEALTH * red_health, 5)

    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, BLACK, BARRIER)

    red_health_text = HEALTH_FONT.render("Health:" + str(red_health), True, RED)
    yellow_health_text = HEALTH_FONT.render("Health:" + str(yellow_health), True, YELLOW)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(YELLOW_GLOW, (yellow.x - 10, yellow.y))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_GLOW, (red.x, red.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    pygame.draw.rect(WIN, BLACK, yellow_health_bar_backside)
    pygame.draw.rect(WIN, RED, yellow_health_bar)
    pygame.draw.rect(WIN, BLACK, red_health_bar_backside)
    pygame.draw.rect(WIN, RED, red_health_bar)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()


def return_to_positions(keys_pressed, yellow, red):
    if keys_pressed[pygame.K_r]:
        yellow.x, yellow.y = 100, 250
        red.x, red.y = 800, 250
    if keys_pressed[pygame.K_q]:
        yellow.x, yellow.y, red.x, red.y = red.x, red.y, yellow.x, yellow.y
        pygame.time.wait(100)


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY >= 0:
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + yellow.width + VELOCITY <= BARRIER.x:
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY >= 0:
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + yellow.height + VELOCITY <= HEIGHT:
        yellow.y += VELOCITY


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY >= BARRIER.x + BARRIER.width:
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width + VELOCITY <= WIDTH:
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY >= 0:
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + red.height + VELOCITY <= HEIGHT:
        red.y += VELOCITY


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    WIN.blit(WINNER_BLACKOUT, (0, 0))
    draw_text = WINNER_FONT.render(text, True, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2 - 50))
    if text.split()[0] == "YELLOW":
        WIN.blit(YELLOW_SPACESHIP, (WIDTH / 2 - SPACESHIP_WIDTH / 2, HEIGHT / 2 + 50))
    if text.split()[0] == "RED":
        WIN.blit(RED_SPACESHIP, (WIDTH/2 - SPACESHIP_WIDTH/2, HEIGHT/2 + 50))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    clock = pygame.time.Clock()
    run = True

    yellow = pygame.Rect(100, 250, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)
    red = pygame.Rect(800, 250, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)

    yellow_health, red_health = MAX_HEALTH, MAX_HEALTH

    yellow_bullets = []
    red_bullets = []

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height / 2 - BULLET_HEIGHT / 2, BULLET_WIDTH, BULLET_HEIGHT)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height / 2 - BULLET_HEIGHT / 2, BULLET_WIDTH, BULLET_HEIGHT)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = None
        if red_health <= 0:
            winner_text = "YELLOW WINS!"

        if yellow_health <= 0:
            winner_text = "RED WINS!"

        keys_pressed = pygame.key.get_pressed()
        return_to_positions(keys_pressed, yellow, red)
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)

        if winner_text:
            draw_winner(winner_text)
            break

    main()


if __name__ == "__main__":
    main()