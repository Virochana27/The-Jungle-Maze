import pygame
import sys

import main
import level_3

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
    [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 3, 0, 2, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 6, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 5, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 0, 4, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 4, 1, 0, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 7, 1, 0, 1, 0, 0, 4, 1, 1, 1, 1],
    [1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 0, 1, 0, 0, 0, 0, 0, 4, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

total_keys = sum(row.count(4) for row in maze)

player_image = pygame.image.load('sources/images/L2/player.png')
enemy_image = pygame.image.load('sources/images/L2/enemy.png')
second_enemy_image = pygame.image.load('sources/images/L2/enemy.png')
third_enemy_image = pygame.image.load('sources/images/L2/enemy.png')
fourth_enemy_image = pygame.image.load('sources/images/L2/enemy.png')
fifth_enemy_image = pygame.image.load('sources/images/L2/enemy.png')
trap_image = pygame.image.load('sources/images/L2/trap.png')
heal_image = pygame.image.load('sources/images/L2/heal.png')
slow_down_image = pygame.image.load('sources/images/L2/slow_down.png')
after_trap_image = pygame.image.load('sources/images/L2/After_Trap.png')
tile_images = [pygame.image.load(f'sources/images/L2/tile_{i}.png') for i in range(1, 7)]

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

player = player_image.get_rect(topleft=(TILE_SIZE * 2, TILE_SIZE * 9))
enemy = enemy_image.get_rect(topleft=(TILE_SIZE * 3, TILE_SIZE * 3))
second_enemy = second_enemy_image.get_rect(topleft=(TILE_SIZE * 9, TILE_SIZE * 7))
third_enemy = third_enemy_image.get_rect(topleft=(TILE_SIZE * 9, TILE_SIZE * 9))
fourth_enemy = fourth_enemy_image.get_rect(topleft=(TILE_SIZE * 15, TILE_SIZE * 6))
fifth_enemy = fifth_enemy_image.get_rect(topleft=(TILE_SIZE * 19, TILE_SIZE * 4))
enemy_direction = (0, -1)
second_enemy_direction = (1, 1)
third_enemy_direction = (-1, 0)
fourth_enemy_direction = (0, 1)
fifth_enemy_direction = (0, 1)

clock = pygame.time.Clock()

keys_pressed = set()

all_keys_collected = False

move_delay = 5
move_counter = 0


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
    screen.blit(player_image, player)
    screen.blit(enemy_image, enemy)
    screen.blit(second_enemy_image, second_enemy)
    screen.blit(third_enemy_image, third_enemy)
    screen.blit(fourth_enemy_image, fourth_enemy)
    screen.blit(fifth_enemy_image, fifth_enemy)


def draw():
    screen.fill((0, 0, 0))
    draw_maze()
    draw_actors()


interpolation_steps = 10
interpolation_counter = 0
interpolation_target = None


def handle_key_down(key):
    global player
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

    row = int(player.y / TILE_SIZE)
    column = int(player.x / TILE_SIZE)

    movement_factor = 1

    if key == pygame.K_k and not slow_down_enemy:
        slow_down_enemy = True
    if key == pygame.K_l and slow_down_enemy:
        slow_down_enemy = False

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
            move_delay = 30
            maze[row][column] = 1
            trap_sound.play()
        elif tile == 'heal':
            move_delay = 5
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
                unlock = True
                maze[row][column] = 0
                player.topleft = (column * TILE_SIZE, row * TILE_SIZE)
                key_collected_sound.play()

                all_keys_collected = all(4 not in row for row in maze)
                if all_keys_collected:
                    unlock = True
        elif tile == 'door' and unlock and all_keys_collected:
            unlock = False
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
        interp_x = (player.x * (interpolation_counter - 1) + interpolation_target[0]) // interpolation_counter
        interp_y = (player.y * (interpolation_counter - 1) + interpolation_target[1]) // interpolation_counter
        player.topleft = (interp_x, interp_y)
        interpolation_counter -= 1

    for key in keys_pressed:
        handle_key_down(key)

    handle_enemy_move()
    handle_second_enemy_move()
    handle_third_enemy_move()
    handle_fourth_enemy_move()
    handle_fifth_enemy_move()

    if move_counter > 0:
        move_counter -= 1


def handle_enemy_move():
    global enemy_direction
    global j_pressed
    global slow_down_enemy

    speed_factor = 2 if j_pressed else 1
    speed_factor *= 0.5 if slow_down_enemy else 1

    row = int(enemy.y / TILE_SIZE)
    column = int(enemy.x / TILE_SIZE)
    next_row = int(row + enemy_direction[1] * speed_factor)
    next_column = int(column + enemy_direction[0] * speed_factor)

    if 0 <= next_row < NUM_ROWS and 0 <= next_column < NUM_COLS:
        next_tile = tiles[maze[next_row][next_column]]
        if next_tile != 'wall':

            enemy.move_ip(TILE_SIZE * enemy_direction[0] * speed_factor // 20,
                          TILE_SIZE * enemy_direction[1] * speed_factor // 20)
        else:
            enemy_direction = (-enemy_direction[0], -enemy_direction[1])
        if enemy.colliderect(player):
            player_dies_sound.play()
            game_over()


def handle_second_enemy_move():
    global second_enemy_direction

    speed_factor = 2 if j_pressed else 1
    speed_factor *= 0.5 if slow_down_enemy else 1

    row = int(second_enemy.y / TILE_SIZE)
    column = int(second_enemy.x / TILE_SIZE)

    next_row = int(row + second_enemy_direction[1] * speed_factor)

    if 0 <= next_row < NUM_ROWS:
        next_tile = tiles[maze[next_row][column]]
        if next_tile != 'wall':
            dy = second_enemy_direction[1] * TILE_SIZE * speed_factor // 16
            second_enemy.move_ip(0, dy)
        else:
            second_enemy_direction = (-second_enemy_direction[0], -second_enemy_direction[1])

    if second_enemy.colliderect(player):
        player_dies_sound.play()
        game_over()


def handle_third_enemy_move():
    global third_enemy_direction

    speed_factor = 2 if j_pressed else 1
    speed_factor *= 0.5 if slow_down_enemy else 1
    row = int(third_enemy.y / TILE_SIZE)
    column = int(third_enemy.x / TILE_SIZE)
    next_column = int(column + third_enemy_direction[0] * speed_factor)

    if 0 <= row < NUM_ROWS and 0 <= next_column < NUM_COLS:
        next_tile = tiles[maze[row][next_column]]
        if next_tile != 'wall':

            dx = third_enemy_direction[0] * TILE_SIZE * speed_factor // 16
            third_enemy.move_ip(dx, 0)
        else:
            third_enemy_direction = (-third_enemy_direction[0], -third_enemy_direction[1])

    if third_enemy.colliderect(player):
        player_dies_sound.play()
        game_over()


def handle_fourth_enemy_move():
    global fourth_enemy_direction

    speed_factor = 2 if j_pressed else 1
    speed_factor *= 0.5 if slow_down_enemy else 1

    row = int(fourth_enemy.y / TILE_SIZE)
    column = int(fourth_enemy.x / TILE_SIZE)
    next_row = int(row + fourth_enemy_direction[1] * speed_factor)

    if 0 <= next_row < NUM_ROWS and 0 <= column < NUM_COLS:
        next_tile = tiles[maze[next_row][column]]
        if next_tile != 'wall':

            dy = fourth_enemy_direction[1] * TILE_SIZE * speed_factor // 18
            fourth_enemy.move_ip(0, dy)
        else:
            fourth_enemy_direction = (-fourth_enemy_direction[0], -fourth_enemy_direction[1])

    if fourth_enemy.colliderect(player):
        player_dies_sound.play()
        game_over()


def handle_fifth_enemy_move():
    global fifth_enemy_direction

    speed_factor = 2 if j_pressed else 1
    speed_factor *= 0.5 if slow_down_enemy else 1

    row = int(fifth_enemy.y / TILE_SIZE)
    column = int(fifth_enemy.x / TILE_SIZE)
    next_row = int(row + fifth_enemy_direction[1] * speed_factor)
    next_column = int(column + fifth_enemy_direction[0] * speed_factor)

    if 0 <= next_row < NUM_ROWS and 0 <= next_column < NUM_COLS:
        next_tile = tiles[maze[next_row][next_column]]
        if next_tile != 'wall':

            dx = fifth_enemy_direction[0] * TILE_SIZE * speed_factor // 18
            dy = fifth_enemy_direction[1] * TILE_SIZE * speed_factor // 18
            fifth_enemy.move_ip(dx, dy)
        else:
            fifth_enemy_direction = (-fifth_enemy_direction[0], -fifth_enemy_direction[1])

    if fifth_enemy.colliderect(player):
        player_dies_sound.play()
        game_over()


def restart_game():
    global tiles, unlock, maze, player, enemy, second_enemy, third_enemy, fourth_enemy, fifth_enemy
    global enemy_direction, second_enemy_direction, third_enemy_direction, fourth_enemy_direction, fifth_enemy_direction
    global keys_pressed, all_keys_collected, move_counter, interpolation_counter, interpolation_target, paused, j_pressed
    global slow_down_enemy, slow_down_duration, slow_down_counter, move_delay

    # Reset game variables to their initial state
    tiles = ['empty', 'wall', 'goal', 'door', 'key', 'trap', 'heal', 'slow_down']
    unlock = False

    maze = [
        [1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 3, 0, 2, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1],
        [1, 1, 1, 6, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 5, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 1, 0, 4, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 4, 1, 0, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 7, 1, 0, 1, 0, 0, 4, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 1, 0, 1, 0, 0, 0, 0, 0, 4, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

    player = player_image.get_rect(topleft=(TILE_SIZE * 2, TILE_SIZE * 9))
    enemy = enemy_image.get_rect(topleft=(TILE_SIZE * 3, TILE_SIZE * 3))
    second_enemy = second_enemy_image.get_rect(topleft=(TILE_SIZE * 9, TILE_SIZE * 7))
    third_enemy = third_enemy_image.get_rect(topleft=(TILE_SIZE * 9, TILE_SIZE * 9))
    fourth_enemy = fourth_enemy_image.get_rect(topleft=(TILE_SIZE * 15, TILE_SIZE * 6))
    fifth_enemy = fifth_enemy_image.get_rect(topleft=(TILE_SIZE * 19, TILE_SIZE * 4))
    enemy_direction = (0, -1)
    second_enemy_direction = (1, 1)
    third_enemy_direction = (-1, 0)
    fourth_enemy_direction = (0, 1)
    fifth_enemy_direction = (0, 1)

    keys_pressed = set()

    all_keys_collected = False

    move_counter = 0
    interpolation_counter = 0
    interpolation_target = None
    paused = False
    j_pressed = False
    slow_down_enemy = False
    slow_down_counter = 0
    move_delay = 5

    # Restart the game loop
    start_screen()


def game_over():
    pygame.time.delay(1000)
    game_over_image = pygame.image.load('sources/images/L2/game_over.png')
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
    game_won_image = pygame.image.load('sources/images/L2/game_won.png')
    screen.blit(game_won_image, (0, 0))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                level_3.restart_game()


def start_screen():
    start_screen_image = pygame.image.load('sources/images/L2/game_start.png')
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


if __name__ == '__main__':(
    restart_game())

# RUNTIME TERRORS
