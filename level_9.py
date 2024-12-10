import pygame
import sys
import pygame.key
import main

pygame.display.set_caption("The Jungle Maze - Runtime Terrors")

icon_image = pygame.image.load("sources/images/icon.jpeg")
pygame.display.set_icon(icon_image)

WIDTH = 1200
HEIGHT = 600

def restart_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    start_screen_image = pygame.image.load('sources/images/main/coming_soon.png')
    screen.blit(start_screen_image, (0, 0))
    pygame.display.flip()
    pygame.time.delay(500)


    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                main.main_function()

if __name__ == '__main__': (
    restart_game())
# RUNTIME TERRORS