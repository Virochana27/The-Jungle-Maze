import pygame
import sys
import pygame.key
import os
import level_1
import level_2
import level_3
import level_4
import level_5
import level_6
import level_7
import level_8
import level_9


pygame.display.set_caption("The Jungle Maze - Runtime Terrors")

icon_image = pygame.image.load("sources/images/icon.jpeg")
pygame.display.set_icon(icon_image)

WIDTH = 1200
HEIGHT = 600
MENU_FONT = pygame.font.Font(None, 36)
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 60
BUTTON_COLOR = (0, 180, 255)
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_RADIUS = 10
BUTTON_VERTICAL_SPACING = 30
BUTTON_ROW_SPACING = 40
VERTICAL_OFFSET = 120
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
start_screen_image = pygame.image.load('sources/images/main/Runtime_Terrors.png')
screen.blit(start_screen_image, (0, 0))
pygame.display.flip()
pygame.time.delay(500)


def main_function():
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("The Jungle Maze - Runtime Terrors")

    background_img = pygame.image.load('sources/images/main/background.jpg')
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

    button_bg_img = pygame.image.load('sources/images/main/button.png')
    button_bg_img = pygame.transform.scale(button_bg_img, (BUTTON_WIDTH, BUTTON_HEIGHT))

    buttons = [
        ("Level 7", level_7.restart_game),
        ("Level 8", level_8.restart_game),
        ("Level 9", level_9.restart_game),
        ("Level 4", level_4.restart_game),
        ("Level 5", level_5.restart_game),
        ("Level 6", level_6.restart_game),
        ("Level 1", level_1.restart_game),
        ("Level 2", level_2.restart_game),
        ("Level 3", level_3.restart_game),
        ("Exit", None)
    ]

    button_rects = []

    buttons_per_row = 3

    for i, (button_text, _) in enumerate(buttons):
        row = i // buttons_per_row
        col = i % buttons_per_row

        button_rect = pygame.Rect(WIDTH // 2 - BUTTON_WIDTH * 1.65 + col * (BUTTON_WIDTH + BUTTON_ROW_SPACING),
                                  HEIGHT // 2 - BUTTON_HEIGHT // 2 - row * (
                                          BUTTON_HEIGHT + BUTTON_VERTICAL_SPACING) + VERTICAL_OFFSET,
                                  BUTTON_WIDTH, BUTTON_HEIGHT)
        button_rects.append(button_rect)

    exit_button_rect = button_rects[-1]
    exit_button_rect.centerx = WIDTH // 2
    exit_button_rect.y = HEIGHT-100

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for i, button_rect in enumerate(button_rects):
                    if button_rect.collidepoint(mouse_pos):
                        if buttons[i][1] is not None:
                            buttons[i][1]()  # Call the function to start the level
                            return  # Return from the main function after starting the level
                        else:
                            pygame.quit()
                            sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_1:
                    level_1.restart_game()
                if event.key == pygame.K_2:
                    level_2.restart_game()
                if event.key == pygame.K_3:
                    level_3.restart_game()
                if event.key == pygame.K_4:
                    level_4.restart_game()
                if event.key == pygame.K_5:
                    level_5.restart_game()
                if event.key == pygame.K_6:
                    level_6.restart_game()
                if event.key == pygame.K_7:
                    level_7.restart_game()
                if event.key == pygame.K_8:
                    level_8.restart_game()
                if event.key == pygame.K_9:
                    level_9.restart_game()

        screen.blit(background_img, (0, 0))

        for i, (button_text, _) in enumerate(buttons):
            button_rect = button_rects[i]
            # Blit button background image
            screen.blit(button_bg_img, button_rect)
            draw_text(screen, button_text, MENU_FONT, BUTTON_TEXT_COLOR, button_rect.centerx, button_rect.centery)

        pygame.display.flip()


def draw_text(surface, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)


if __name__ == '__main__': (
    main_function())
# RUNTIME TERRORS
