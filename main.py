import pygame
import os
from enum import Enum

FPS = 60
WIDTH, HEIGHT = 900, 500
VELOCITY = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SpaceAttack!")
BARRIER = pygame.Rect((WIDTH - 10) / 2, 0, 10, HEIGHT)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)

BACKGROUND = pygame.image.load(os.path.join("Assets", "space.png"))


def draw_window(yellow, red):
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, BLACK, BARRIER)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    pygame.display.update()


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


def return_to_positions(keys_pressed, yellow, red):
    if keys_pressed[pygame.K_r]:
        yellow.x, yellow.y = 100, 250
        red.x, red.y = 800, 250
    if keys_pressed[pygame.K_q]:
        yellow.x, yellow.y, red.x, red.y = red.x, red.y, yellow.x, yellow.y
        pygame.time.wait(100)


def main():
    clock = pygame.time.Clock()
    run = True

    yellow = pygame.Rect(100, 250, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)
    red = pygame.Rect(800, 250, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        return_to_positions(keys_pressed, yellow, red)
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        draw_window(yellow, red)

    pygame.quit()


if __name__ == "__main__":
    main()