import pygame
import sys

import main

pygame.init()

pygame.display.set_caption("The Jungle Maze - Runtime Terrors")

icon_image = pygame.image.load("sources/images/icon.jpeg")
pygame.display.set_icon(icon_image)

# Game constants
TILE_SIZE = 50
NUM_ROWS = 12
NUM_COLS = 24
WIDTH = TILE_SIZE * NUM_COLS
HEIGHT = TILE_SIZE * NUM_ROWS

tiles = ['empty', 'wall', 'goal', 'door', 'key', 'trap', 'heal', 'slow_down']

unlock = False

maze = [
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
    [0, 1, 0, 5, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
    [0, 1, 4, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 5, 0, 0, 5, 0, 0, 4, 1, 0, 7, 1],
    [0, 1, 1, 1, 0, 1, 4, 5, 1, 5, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1],
    [0, 0, 1, 1, 0, 1, 1, 0, 1, 4, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0],
    [1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0],
    [1, 1, 0, 1, 0, 0, 0, 5, 4, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 3],
    [1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2]
]

total_keys = sum(row.count(4) for row in maze)

player1_image = pygame.image.load('sources/images/L7/player1.png')
player2_image = pygame.image.load('sources/images/L7/player2.png')
enemy_image = pygame.image.load('sources/images/L7/enemy.png')
trap_image = pygame.image.load('sources/images/L7/trap.png')
heal_image = pygame.image.load('sources/images/L7/heal.png')
slow_down_image = pygame.image.load('sources/images/L7/slow_down.png')
after_trap_image = pygame.image.load('sources/images/L7/After_Trap.png')
tile_images = [pygame.image.load(f'sources/images/L7/tile_{i}.png') for i in range(1, 7)]

key_collected_sound = pygame.mixer.Sound('sources/sounds/key_collected.wav')
door_opened_sound = pygame.mixer.Sound('sources/sounds/door_opened.wav')
player_dies_sound = pygame.mixer.Sound('sources/sounds/player_dies.wav')
heal_sound = pygame.mixer.Sound('sources/sounds/heal.wav')
trap_sound = pygame.mixer.Sound('sources/sounds/trap.wav')
slow_down_sound = pygame.mixer.Sound('sources/sounds/slow_down.wav')
speed_up_sound = pygame.mixer.Sound('sources/sounds/speed_up.wav')

pygame.mixer.music.load('sources/sounds/background_music.mp3')
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

paused = False
j_pressed = False
slow_down_enemy = False
slow_down_duration = 10
slow_down_counter = 0

player1 = player1_image.get_rect(topleft=(TILE_SIZE * 2, TILE_SIZE * 10))
player2 = player2_image.get_rect(topleft=(TILE_SIZE * 2, TILE_SIZE * 11))  # Position the second player

enemy1 = enemy_image.get_rect(topleft=(TILE_SIZE * 4, TILE_SIZE * 1))
enemy2 = enemy_image.get_rect(topleft=(TILE_SIZE * 9, TILE_SIZE * 3))
enemy3 = enemy_image.get_rect(topleft=(TILE_SIZE * 18, TILE_SIZE * 8))
enemy4 = enemy_image.get_rect(topleft=(TILE_SIZE * 21, TILE_SIZE * 5))
enemy5 = enemy_image.get_rect(topleft=(TILE_SIZE * 19, TILE_SIZE * 5))
enemy6 = enemy_image.get_rect(topleft=(TILE_SIZE * 1, TILE_SIZE * 8))
enemy7 = enemy_image.get_rect(topleft=(TILE_SIZE * 12, TILE_SIZE * 8))
enemy8 = enemy_image.get_rect(topleft=(TILE_SIZE * 4, TILE_SIZE * 10))

enemy1_direction = (0, -1)
enemy2_direction = (0, -1)
enemy3_direction = (0, -1)
enemy4_direction = (0, -1)
enemy5_direction = (-1, 0)
enemy6_direction = (-1, 0)
enemy7_direction = (-1, 0)
enemy8_direction = (-1, 0)

clock = pygame.time.Clock()

keys_pressed = set()

all_keys_collected = False

move_delay = 5
move_counter = 0

current_player = 1


def draw_tile(x, y, tile):
    if tile == 'trap':
        screen.blit(trap_image, (x, y))
    elif tile == 'heal':
        screen.blit(heal_image, (x, y))
    elif tile == 'slow_down':
        screen.blit(slow_down_image, (x, y))
    else:
        screen.blit(tile_images[tiles.index(tile)], (x, y))


def draw_maze():
    for row in range(NUM_ROWS):
        for column in range(NUM_COLS):
            x = column * TILE_SIZE
            y = row * TILE_SIZE
            tile = tiles[maze[row][column]]
            draw_tile(x, y, tile)


def draw_actors():
    screen.blit(player1_image, player1)
    screen.blit(player2_image, player2)  # Draw the second player
    screen.blit(enemy_image, enemy1)
    screen.blit(enemy_image, enemy2)
    screen.blit(enemy_image, enemy3)
    screen.blit(enemy_image, enemy4)
    screen.blit(enemy_image, enemy5)
    screen.blit(enemy_image, enemy6)
    screen.blit(enemy_image, enemy7)
    screen.blit(enemy_image, enemy8)


def draw():
    screen.fill((0, 0, 0))
    draw_maze()
    draw_actors()


interpolation_steps = 10
interpolation_counter = 0
interpolation_target = None


def handle_key_down(key):
    global current_player
    global unlock
    global all_keys_collected
    global move_counter
    global interpolation_counter
    global interpolation_target
    global paused
    global j_pressed
    global slow_down_enemy
    global move_delay
    global slow_down_duration
    global slow_down_counter

    if key == pygame.K_k and not slow_down_enemy:
        slow_down_enemy = True
    if key == pygame.K_l and slow_down_enemy:
        slow_down_enemy = False

    if key == pygame.K_TAB:  # Switch between players
        current_player = 2 if current_player == 1 else 1
        return  # Exit early to prevent unnecessary movement updates

    # Determine which player to move based on the current active player
    player = player1 if current_player == 1 else player2

    row = int(player.y / TILE_SIZE)
    column = int(player.x / TILE_SIZE)

    movement_factor = 1

    if move_counter == 0 and interpolation_counter == 0:
        if key == pygame.K_UP or key == pygame.K_w:
            row = max(0, row - movement_factor)
        elif key == pygame.K_DOWN or key == pygame.K_s:
            row = min(NUM_ROWS - 1, row + movement_factor)
        elif key == pygame.K_LEFT or key == pygame.K_a:
            column = max(0, column - movement_factor)
        elif key == pygame.K_RIGHT or key == pygame.K_d:
            column = min(NUM_COLS - 1, column + movement_factor)
        elif key == pygame.K_ESCAPE:
            paused = not paused
        elif key == pygame.K_BACKSPACE:
            main.main_function()
        elif key == pygame.K_1:
            restart_game()
        elif key == pygame.K_2:
            main.main_function()
        elif key == pygame.K_3:
            sys.exit()

        tile = tiles[maze[row][column]]

        if tile == 'empty':
            x = column * TILE_SIZE
            y = row * TILE_SIZE

            interpolation_target = (x, y)
            interpolation_counter = interpolation_steps
        elif tile == 'trap':
            if player == player1:
                maze[row][column] = 6
                trap_sound.play()
            else:
                maze[row][column] = 0
                trap_sound.play()
        elif tile == 'heal':
            if player == player2:
                maze[row][column] = 0
                heal_sound.play()
        elif tile == 'slow_down':
            slow_down_enemy = True
            slow_down_counter = slow_down_duration * 60
            maze[row][column] = 0
            slow_down_sound.play()

        if tile == 'goal':
            game_won()

        elif tile == 'key':
            if not unlock or not all_keys_collected:
                if player == player1:
                    unlock = True
                    maze[row][column] = 0
                    player.topleft = (column * TILE_SIZE, row * TILE_SIZE)
                    key_collected_sound.play()

                    all_keys_collected = all(4 not in row for row in maze)
                    if all_keys_collected:
                        unlock = True
                else:
                    maze[row][column] = 4
                    player.topleft = (column * TILE_SIZE, row * TILE_SIZE)

        elif tile == 'door' and unlock and all_keys_collected:
            maze[row][column] = 0
            player.topleft = (column * TILE_SIZE, row * TILE_SIZE)
            door_opened_sound.play()

        move_counter = move_delay

    keys_pressed.add(key)

    if paused:
        if key == pygame.K_ESCAPE:
            paused = not paused
    if key == pygame.K_j or key == pygame.K_f:
        j_pressed = True
        movement_factor = 2
        speed_up_sound.play()

    if not paused and not j_pressed:
        if key == pygame.K_j or key == pygame.K_f:
            j_pressed = True


def handle_key_up(key):
    global j_pressed
    if key == pygame.K_j or key == pygame.K_f:
        j_pressed = False
    if key in keys_pressed:
        keys_pressed.remove(key)


def update():
    global move_counter
    global interpolation_counter
    global interpolation_target
    global paused
    global j_pressed
    global slow_down_counter
    global slow_down_enemy
    global enemy1, enemy2, enemy3, enemy4, enemy5, enemy6, enemy7, enemy8

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
            else:
                handle_key_down(event.key)
        if event.type == pygame.KEYUP:
            handle_key_up(event.key)

    if paused:
        return

    if slow_down_enemy:
        if slow_down_counter > 0:
            slow_down_counter -= 1
        else:
            slow_down_enemy = False

    # Interpolation update
    if interpolation_counter > 0:
        interp_step = (TILE_SIZE * interpolation_steps) // interpolation_counter
        interp_x = (player1.x * (interpolation_counter - 1) + interpolation_target[0]) // interpolation_counter \
            if current_player == 1 else (player2.x * (interpolation_counter - 1) + interpolation_target[0]) // \
                                        interpolation_counter
        interp_y = (player1.y * (interpolation_counter - 1) + interpolation_target[1]) // interpolation_counter \
            if current_player == 1 else (player2.y * (interpolation_counter - 1) + interpolation_target[1]) // \
                                        interpolation_counter
        if current_player == 1:
            player1.topleft = (interp_x, interp_y)
        else:
            player2.topleft = (interp_x, interp_y)
        interpolation_counter -= 1

    for key in keys_pressed:
        handle_key_down(key)

    if player1.colliderect(enemy1) or player1.colliderect(enemy2) or player1.colliderect(enemy3) or player1.colliderect(
            enemy4) or player1.colliderect(enemy5) or player1.colliderect(enemy6) or player1.colliderect(
            enemy7) or player1.colliderect(enemy8):
        player_dies_sound.play()
        game_over()

    if player2.colliderect(enemy1) or player2.colliderect(enemy2) or player2.colliderect(enemy3) or player2.colliderect(
            enemy4) or player2.colliderect(enemy5) or player2.colliderect(enemy6) or player2.colliderect(
            enemy7) or player2.colliderect(enemy8):
        player_dies_sound.play()
        game_over()

    handle_enemy1_move()
    handle_enemy2_move()
    handle_enemy3_move()
    handle_enemy4_move()
    handle_enemy5_move()
    handle_enemy6_move()
    handle_enemy7_move()
    handle_enemy8_move()

    if move_counter > 0:
        move_counter -= 1


def handle_enemy1_move():
    global enemy1_direction
    global j_pressed
    global slow_down_enemy
    global move_delay
    global enemy1

    speed_factor = 2 if j_pressed else 1
    speed_factor *= 0.75 if slow_down_enemy else 1

    row = int(enemy1.y / TILE_SIZE)
    column = int(enemy1.x / TILE_SIZE)
    next_row = int(row + enemy1_direction[1] * speed_factor)
    next_column = int(column + enemy1_direction[0] * speed_factor)

    if 0 <= next_row < NUM_ROWS and 0 <= next_column < NUM_COLS:
        next_tile = tiles[maze[next_row][next_column]]
        if next_tile != 'wall':
            enemy1.move_ip(TILE_SIZE * enemy1_direction[0] * speed_factor // 16,
                           TILE_SIZE * enemy1_direction[1] * speed_factor // 16)
        else:
            enemy1_direction = (-enemy1_direction[0], -enemy1_direction[1])


def handle_enemy2_move():
    global enemy2_direction
    global j_pressed
    global slow_down_enemy
    global move_delay
    global enemy

    speed_factor = 2 if j_pressed else 1
    speed_factor *= 0.75 if slow_down_enemy else 1

    row = int(enemy2.y / TILE_SIZE)
    column = int(enemy2.x / TILE_SIZE)
    next_row = int(row + enemy2_direction[1] * speed_factor)
    next_column = int(column + enemy2_direction[0] * speed_factor)

    if 0 <= next_row < NUM_ROWS and 0 <= next_column < NUM_COLS:
        next_tile = tiles[maze[next_row][next_column]]
        if next_tile != 'wall':
            enemy2.move_ip(TILE_SIZE * enemy2_direction[0] * speed_factor // 11,
                           TILE_SIZE * enemy2_direction[1] * speed_factor // 11)
        else:
            enemy2_direction = (-enemy2_direction[0], -enemy2_direction[1])


def handle_enemy3_move():
    global enemy3_direction
    global j_pressed
    global slow_down_enemy
    global move_delay
    global enemy3

    speed_factor = 2 if j_pressed else 1
    speed_factor *= 0.75 if slow_down_enemy else 1

    row = int(enemy3.y / TILE_SIZE)
    column = int(enemy3.x / TILE_SIZE)
    next_row = int(row + enemy3_direction[1] * speed_factor)
    next_column = int(column + enemy3_direction[0] * speed_factor)

    if 0 <= next_row < NUM_ROWS and 0 <= next_column < NUM_COLS:
        next_tile = tiles[maze[next_row][next_column]]
        if next_tile != 'wall':
            enemy3.move_ip(TILE_SIZE * enemy3_direction[0] * speed_factor // 16,
                           TILE_SIZE * enemy3_direction[1] * speed_factor // 16)
        else:
            enemy3_direction = (-enemy3_direction[0], -enemy3_direction[1])


def handle_enemy4_move():
    global enemy4_direction
    global j_pressed
    global slow_down_enemy
    global move_delay
    global enemy4

    speed_factor = 2 if j_pressed else 1
    speed_factor *= 0.75 if slow_down_enemy else 1

    row = int(enemy4.y / TILE_SIZE)
    column = int(enemy4.x / TILE_SIZE)
    next_row = int(row + enemy4_direction[1] * speed_factor)
    next_column = int(column + enemy4_direction[0] * speed_factor)

    if 0 <= next_row < NUM_ROWS and 0 <= next_column < NUM_COLS:
        next_tile = tiles[maze[next_row][next_column]]
        if next_tile != 'wall':
            enemy4.move_ip(TILE_SIZE * enemy4_direction[0] * speed_factor // 12,
                           TILE_SIZE * enemy4_direction[1] * speed_factor // 12)
        else:
            enemy4_direction = (-enemy4_direction[0], -enemy4_direction[1])


def handle_enemy5_move():
    global enemy5_direction
    global j_pressed
    global slow_down_enemy
    global move_delay
    global enemy5

    speed_factor = 2 if j_pressed else 1
    speed_factor *= 0.75 if slow_down_enemy else 1

    row = int(enemy5.y / TILE_SIZE)
    column = int(enemy5.x / TILE_SIZE)
    next_row = int(row + enemy5_direction[1] * speed_factor)
    next_column = int(column + enemy5_direction[0] * speed_factor)

    if 0 <= next_row < NUM_ROWS and 0 <= next_column < NUM_COLS:
        next_tile = tiles[maze[next_row][next_column]]
        if next_tile != 'wall':
            enemy5.move_ip(TILE_SIZE * enemy5_direction[0] * speed_factor // 16,
                           TILE_SIZE * enemy5_direction[1] * speed_factor // 16)
        else:
            enemy5_direction = (-enemy5_direction[0], -enemy5_direction[1])


def handle_enemy6_move():
    global enemy6_direction
    global j_pressed
    global slow_down_enemy
    global move_delay
    global enemy6

    speed_factor = 2 if j_pressed else 1
    speed_factor *= 0.75 if slow_down_enemy else 1

    row = int(enemy6.y / TILE_SIZE)
    column = int(enemy6.x / TILE_SIZE)
    next_row = int(row + enemy6_direction[1] * speed_factor)
    next_column = int(column + enemy6_direction[0] * speed_factor)

    if 0 <= next_row < NUM_ROWS and 0 <= next_column < NUM_COLS:
        next_tile = tiles[maze[next_row][next_column]]
        if next_tile != 'wall':
            enemy6.move_ip(TILE_SIZE * enemy6_direction[0] * speed_factor // 16,
                           TILE_SIZE * enemy6_direction[1] * speed_factor // 16)
        else:
            enemy6_direction = (-enemy6_direction[0], -enemy6_direction[1])


def handle_enemy7_move():
    global enemy7_direction
    global j_pressed
    global slow_down_enemy
    global move_delay
    global enemy7

    speed_factor = 2 if j_pressed else 1
    speed_factor *= 0.75 if slow_down_enemy else 1

    row = int(enemy7.y / TILE_SIZE)
    column = int(enemy7.x / TILE_SIZE)
    next_row = int(row + enemy7_direction[1] * speed_factor)
    next_column = int(column + enemy7_direction[0] * speed_factor)

    if 0 <= next_row < NUM_ROWS and 0 <= next_column < NUM_COLS:
        next_tile = tiles[maze[next_row][next_column]]
        if next_tile != 'wall':
            enemy7.move_ip(TILE_SIZE * enemy7_direction[0] * speed_factor // 18,
                           TILE_SIZE * enemy7_direction[1] * speed_factor // 18)
        else:
            enemy7_direction = (-enemy7_direction[0], -enemy7_direction[1])


def handle_enemy8_move():
    global enemy8_direction
    global j_pressed
    global slow_down_enemy
    global move_delay
    global enemy8

    speed_factor = 2 if j_pressed else 1
    speed_factor *= 0.75 if slow_down_enemy else 1

    row = int(enemy8.y / TILE_SIZE)
    column = int(enemy8.x / TILE_SIZE)
    next_row = int(row + enemy8_direction[1] * speed_factor)
    next_column = int(column + enemy8_direction[0] * speed_factor)

    if 0 <= next_row < NUM_ROWS and 0 <= next_column < NUM_COLS:
        next_tile = tiles[maze[next_row][next_column]]
        if next_tile != 'wall':
            enemy8.move_ip(TILE_SIZE * enemy8_direction[0] * speed_factor // 16,
                           TILE_SIZE * enemy8_direction[1] * speed_factor // 16)
        else:
            enemy8_direction = (-enemy8_direction[0], -enemy8_direction[1])


def restart_game():
    global tiles, unlock, maze, player1, player2, enemy1, enemy2, enemy3, enemy4, enemy5, enemy6, enemy7, enemy8
    global enemy1_direction, enemy2_direction, enemy3_direction, enemy4_direction, enemy5_direction, enemy6_direction, enemy7_direction, enemy8_direction
    global keys_pressed, all_keys_collected, move_counter, interpolation_counter, interpolation_target, paused, j_pressed
    global slow_down_enemy, slow_down_duration, slow_down_counter, move_delay

    # Reset game variables to their initial state
    tiles = ['empty', 'wall', 'goal', 'door', 'key', 'trap', 'heal', 'slow_down']
    unlock = False

    maze = [
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
        [0, 1, 0, 5, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
        [0, 1, 4, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 5, 0, 0, 5, 0, 0, 4, 1, 0, 7, 1],
        [0, 1, 1, 1, 0, 1, 4, 5, 1, 5, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1],
        [0, 0, 1, 1, 0, 1, 1, 0, 1, 4, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0],
        [1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0],
        [1, 1, 0, 1, 0, 0, 0, 5, 4, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 3],
        [1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2]
    ]

    player1 = player1_image.get_rect(topleft=(TILE_SIZE * 2, TILE_SIZE * 10))
    player2 = player2_image.get_rect(topleft=(TILE_SIZE * 2, TILE_SIZE * 11))  # Position the second player

    enemy1 = enemy_image.get_rect(topleft=(TILE_SIZE * 4, TILE_SIZE * 1))
    enemy2 = enemy_image.get_rect(topleft=(TILE_SIZE * 9, TILE_SIZE * 3))
    enemy3 = enemy_image.get_rect(topleft=(TILE_SIZE * 18, TILE_SIZE * 8))
    enemy4 = enemy_image.get_rect(topleft=(TILE_SIZE * 21, TILE_SIZE * 5))
    enemy5 = enemy_image.get_rect(topleft=(TILE_SIZE * 19, TILE_SIZE * 5))
    enemy6 = enemy_image.get_rect(topleft=(TILE_SIZE * 1, TILE_SIZE * 8))
    enemy7 = enemy_image.get_rect(topleft=(TILE_SIZE * 12, TILE_SIZE * 8))
    enemy8 = enemy_image.get_rect(topleft=(TILE_SIZE * 4, TILE_SIZE * 10))

    enemy1_direction = (0, -1)
    enemy2_direction = (0, -1)
    enemy3_direction = (0, -1)
    enemy4_direction = (0, -1)
    enemy5_direction = (-1, 0)
    enemy6_direction = (-1, 0)
    enemy7_direction = (-1, 0)
    enemy8_direction = (-1, 0)

    keys_pressed = set()

    all_keys_collected = False

    move_counter = 0
    interpolation_counter = 0
    interpolation_target = None
    paused = False
    j_pressed = False
    slow_down_enemy = False
    slow_down_duration = 10
    slow_down_counter = 0

    # Restart the game loop
    start_screen()


def game_over():
    pygame.time.delay(1000)
    game_over_image = pygame.image.load('sources/images/L7/game_over.png')
    screen.blit(game_over_image, (0, 0))
    pygame.display.flip()
    pygame.time.delay(2000)

    restart_image=pygame.image.load('sources/images/main/restart_game.png')
    screen.blit(restart_image, (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    restart_game()
                elif event.key==pygame.K_BACKSPACE:
                    sys.exit()
                else:
                    main.main_function()


def game_won():
    game_won_image = pygame.image.load('sources/images/L7/game_won.jpg')
    screen.blit(game_won_image, (0, 0))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                main.main_function()


def start_screen():
    start_screen_image = pygame.image.load('sources/images/L7/game_start.jpg')
    screen.blit(start_screen_image, (0, 0))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                while True:
                    draw()
                    update()
                    pygame.display.flip()
                    clock.tick(60)

if __name__ == '__main__': (
    restart_game())





