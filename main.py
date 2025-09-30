# BUTTON: rfzkk.itch.io/interface-buttons-pixel-art
# CHARACTER: 9e0.itch.io/chick-boy
import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1920, 1080
FPS = 60
TILE_SIZE = 65

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
CLOCK = pygame.time.Clock()

levels = [
    [
        "---------------------------------------",
        "---------------------------------------",
        "---------------------------------------",
        "---------------------------------------",
        "---------------------------------------",
        "---------------------------------------",
        "---------------------------------------",
        "---------------------------------------",
        "---------------------------------------",
        "-------------*------*------------------",
        "----------------##--------*------------",
        "---------*---#----------###------------",
        "------######---------------------------",
        "----------------------#-------------F--",
        "#######################################",
    ],
    [
        "----------------------------------------------",
        "----------------------------------------------",
        "----------------------------------------------",
        "----------------------------------------------",
        "----------------------------------------------",
        "----------------------------------------------",
        "----------------------------------------------",
        "---------------------------------*------------",
        "-----------------------*----------------------",
        "-------------*-------#----------#-#---*-------",
        "---*----#-#--#--##-#------*-#-#---------------",
        "------#--*--------------#-#-------------------",
        "-----#----------------------------------------",
        "----#-----------------#--------------------F--",
        "##############################################",
    ],
    [
        "-----------------------------------------------------",
        "-----------------------------------------------------",
        "-----------------------------------------------------",
        "-----------------------------------------------------",
        "-----------------------------------------------------",
        "-----------------------------------------------------",
        "-----------------------------------------------------",
        "---------------------------------##------------------",
        "---------------------------*--#----------------------",
        "-------#------------*--------#--*--------------------",
        "----------------------#----#-------------------------",
        "------#--*--------------#-#--------*-------*---------",
        "---------------------------------------*-------------",
        "-------#--------------#--------------------#------F--",
        "#####################################################",
    ],
    [
        "--------------------------------------------------------------",
        "----------------*-----*---------------------------------------",
        "-------*------#---------------------------------*-------------",
        "---------*--#---------#-----------------------#-----------*---",
        "-------#--#------------------*--------------*-----------------",
        "--*---#---------------#--------#--------------#-----------#---",
        "---------------------------------*----------------------*-----",
        "#########################################################-----",
        "---------------------------*----------------------------------",
        "--------------------*-----------*------------------------#----",
        "----------------------#---*#--##------------------------------",
        "---*-----*-------------*#-#--------*-------*----------------#-",
        "---###--------------------#--------#---*-----------------#----",
        "F------#--------------#-----#--------------#------------------",
        "##############################################################",
    ],
]

current_level_index = 3

menu_music = "sprites/menu_music.flac"
game_music = "sprites/game_music.wav"

flag_sprite = pygame.image.load("sprites/flag.png")
flag_sprite = pygame.transform.scale(flag_sprite, (TILE_SIZE, TILE_SIZE))
flag_position = None

platform_sprite = pygame.image.load("sprites/tile106.png")
platform_sprite = pygame.transform.scale(platform_sprite, (TILE_SIZE, TILE_SIZE))

egg_sprite = pygame.image.load("sprites/egg.png")
egg_sprite = pygame.transform.scale(egg_sprite, (TILE_SIZE // 1.5, TILE_SIZE // 1.5))

play_button = pygame.transform.scale(
    pygame.image.load("sprites/play_button.png"), (300, 100)
)
play_button_rect = play_button.get_rect(center=(WIDTH // 2, HEIGHT // 1.3))

exit_button = pygame.transform.scale(
    pygame.image.load("sprites/quit_button.png"), (300, 100)
)
exit_button_rect = exit_button.get_rect(center=(WIDTH // 2, HEIGHT // 1.1))

help_button = pygame.transform.scale(
    pygame.image.load("sprites/info_button.png"), (100, 100)
)
help_button_rect = help_button.get_rect(center=(WIDTH - 710, HEIGHT // 1.2))

sound_on = pygame.transform.scale(pygame.image.load("sprites/sound_on.png"), (100, 100))
sound_off = pygame.transform.scale(
    pygame.image.load("sprites/sound_off.png"), (100, 100)
)

sound_button_rect = sound_on.get_rect(center=(710, HEIGHT // 1.2))

splash_frames = [
    pygame.transform.scale(
        pygame.image.load("sprites/logo_dyrhyrv.png").convert_alpha(), (400, 650)
    ),
    pygame.transform.scale(
        pygame.image.load("sprites/logo_pygame.png").convert_alpha(), (808, 320)
    ),
]
splash_timer = 0
splash_frame = 0

main_menu_background = pygame.transform.smoothscale(
    pygame.image.load("sprites/main_menu_background.png"), (WIDTH, HEIGHT)
)
help_background = pygame.transform.smoothscale(
    pygame.image.load("sprites/help_background.png"), (WIDTH, HEIGHT)
)

main_menu_font = pygame.font.Font(None, 74)

platforms = []
eggs = []

player_size = (TILE_SIZE, TILE_SIZE)


def load_level(level_index):
    global \
        level_map, \
        platforms, \
        eggs, \
        flag_position, \
        player, \
        collected_eggs, \
        total_eggs, \
        player, \
        map_width, \
        map_height

    level_map = levels[level_index]
    platforms = []
    eggs = []
    flag_position = None

    for row_index, row in enumerate(level_map):
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            if tile == "#":
                platforms.append((x, y))
            elif tile == "*":
                eggs.append((x + TILE_SIZE // 4, y + TILE_SIZE // 4))
            elif tile == "F":
                flag_position = (x, y)

    player = pygame.Rect(100, 840, TILE_SIZE, TILE_SIZE)

    map_width = len(level_map[0]) * TILE_SIZE
    map_height = len(level_map) * TILE_SIZE

    collected_eggs = 0
    total_eggs = len(eggs)


def load_sprites(folder, count):
    return [
        pygame.transform.scale(
            pygame.image.load(f"{folder}/{i}.png").convert_alpha(), (400, 400)
        )
        for i in range(1, count)
    ]


idle_sprites = load_sprites("sprites/idle", 6)
run_sprites = load_sprites("sprites/run", 10)

player_speed = 5
jump_power = 17
gravity = 1
velocity_y = 0
on_ground = False
camera_x = 0
state = "splash"
game_running = True
collected_eggs = 0
total_eggs = len(eggs)
current_frame = 0
animation_timer = 0
animation_speed = 100
current_sprites = idle_sprites
facing_right = True

volume = 1

background_far = pygame.image.load("sprites/2_clouds.png").convert_alpha()
background_far = pygame.transform.scale(background_far, (WIDTH, HEIGHT))

background_mid = pygame.image.load("sprites/3_city.png").convert_alpha()
background_mid = pygame.transform.scale(background_mid, (WIDTH, HEIGHT))

background = pygame.image.load("sprites/4_ground.png").convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_width = background.get_width()

load_level(current_level_index)

while game_running:
    if state == "main_menu":
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(menu_music)
            pygame.mixer.music.play(-1)
        screen.blit(main_menu_background, (0, 0))
        screen.blit(play_button, play_button_rect)
        screen.blit(exit_button, exit_button_rect)
        screen.blit(help_button, help_button_rect)
        screen.blit(sound_on if volume > 0 else sound_off, sound_button_rect)

        for event in pygame.event.get():
            if event.type == QUIT:
                game_running = False
            if event.type == MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    state = "game"
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.load(game_music)
                        pygame.mixer.music.play(-1)
                elif exit_button_rect.collidepoint(event.pos):
                    game_running = False
                elif help_button_rect.collidepoint(event.pos):
                    state = "help"
                elif sound_button_rect.collidepoint(event.pos):
                    volume = 0 if volume > 0 else 1
                    pygame.mixer.music.set_volume(volume)
    elif state == "game":
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(game_music)
            pygame.mixer.music.play(-1)
        for event in pygame.event.get():
            if event.type == QUIT:
                game_running = False

        keys = pygame.key.get_pressed()
        direction = "idle"

        if keys[K_a]:
            player.x -= player_speed
            direction = "run"
            facing_right = False
        if keys[K_d]:
            player.x += player_speed
            direction = "run"
            facing_right = True
        if keys[K_SPACE] and on_ground:
            velocity_y = -jump_power
            on_ground = False
            direction = "jump"
        if keys[K_ESCAPE]:
            state = "main_menu"

        player.x = max(0, min(player.x, map_width - player.width))

        velocity_y += gravity
        player.y += velocity_y
        on_ground = False

        for platform_x, platform_y in platforms:
            platform_rect = pygame.Rect(platform_x, platform_y, TILE_SIZE, TILE_SIZE)
            if (
                player.bottom >= platform_rect.top
                and player.bottom <= platform_rect.top + velocity_y
                and player.right > platform_rect.left
                and player.left < platform_rect.right
            ):
                player.bottom = platform_rect.top
                velocity_y = 0
                on_ground = True

        camera_x = player.x - WIDTH // 2
        camera_x = max(0, min(camera_x, map_width - WIDTH))

        for egg in eggs[:]:
            egg_rect = pygame.Rect(egg[0], egg[1], TILE_SIZE // 2, TILE_SIZE // 2)
            if player.colliderect(egg_rect):
                eggs.remove(egg)
                collected_eggs += 1

        if direction == "run":
            if current_sprites != run_sprites:
                current_sprites = run_sprites
                current_frame = 0
        else:
            if current_sprites != idle_sprites:
                current_sprites = idle_sprites
                current_frame = 0

        animation_timer += CLOCK.get_time()
        if animation_timer >= animation_speed:
            animation_timer = 0
            current_frame = (current_frame + 1) % len(current_sprites)

        screen.fill((135, 206, 235))
        bg_far_offset = -camera_x * 0.4 % background_width
        bg_mid_offset = -camera_x * 0.6 % background_width

        screen.blit(background_far, (bg_far_offset - background_width, 0))
        screen.blit(background_far, (bg_far_offset, 0))

        screen.blit(background_mid, (bg_mid_offset - background_width, 0))
        screen.blit(background_mid, (bg_mid_offset, 0))

        bg_offset = -camera_x % background_width
        screen.blit(background, (bg_offset - background_width, 0))
        screen.blit(background, (bg_offset, 0))

        for platform_x, platform_y in platforms:
            screen.blit(platform_sprite, (platform_x - camera_x, platform_y))

        for egg_x, egg_y in eggs:
            screen.blit(egg_sprite, (egg_x - camera_x, egg_y))

        if flag_position:
            flag_x, flag_y = flag_position
            screen.blit(flag_sprite, (flag_x - camera_x, flag_y))

        player_image = pygame.transform.scale(
            current_sprites[current_frame], player_size
        )
        if not facing_right:
            player_image = pygame.transform.flip(player_image, True, False)
        screen.blit(player_image, player.move(-camera_x, 0).topleft)

        font = pygame.font.SysFont(None, 58)
        text = font.render(
            f"Яиц собрано: {collected_eggs}/{total_eggs}", True, (255, 255, 255)
        )
        text_level = font.render(
            f"Уровень: {current_level_index + 1}", True, (255, 255, 255)
        )
        screen.blit(text, (10, 10))
        screen.blit(text_level, (10, 50))

        if collected_eggs == total_eggs and player.colliderect(
            pygame.Rect(flag_x, flag_y, TILE_SIZE, TILE_SIZE)
        ):
            if current_level_index + 1 < len(levels):
                current_level_index += 1
                load_level(current_level_index)
            else:
                win_text = main_menu_font.render(
                    "Ты прошел все уровни!", True, (255, 255, 0)
                )
                screen.blit(win_text, (WIDTH // 2 - 400, HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(3000)
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.load(menu_music)
                    pygame.mixer.music.play(-1)
                state = "main_menu"
                current_level_index = 0
                load_level(current_level_index)
    elif state == "help":
        screen.blit(help_background, (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                game_running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = "main_menu"
    elif state == "splash":
        screen.blit(
            splash_frames[splash_frame],
            (
                WIDTH // 2 - splash_frames[splash_frame].get_width() // 2,
                HEIGHT // 2 - splash_frames[splash_frame].get_height() // 2,
            ),
        )

        splash_timer += CLOCK.get_time()
        if splash_timer > 3000:
            splash_timer = 0
            splash_frame += 1
            screen.fill((0, 0, 0))
            if splash_frame >= len(splash_frames):
                state = "main_menu"

        pygame.display.flip()
    pygame.display.flip()
    CLOCK.tick(FPS)

pygame.quit()
