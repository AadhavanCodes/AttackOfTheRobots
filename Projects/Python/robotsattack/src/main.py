from enum import Enum

import pygame
import random
from player import Player
from projectile import WaterBalloon
from enemy import Enemy, Speedy, Bulky
from crate import Crate
from crate import ExplosiveCrate
from explosion import Explosion
from powerup import PowerUp
from hud import HUD
from cheat_codes import CheatCodeHandler

# Start the game
pygame.init()

pygame.mixer.pre_init(buffer=2048)
game_width = 1000
game_height = 650
screen = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()
running = True

background_img = pygame.image.load("../assets/BG_SciFi.png")
pygame.mixer.music.load("../assets/sfx/ingame.wav")
# pygame.mixer.music.play(-1)

playerGroup = pygame.sprite.Group()
projectilesGroup = pygame.sprite.Group()
enemiesGroup = pygame.sprite.Group()
cratesGroup = pygame.sprite.Group()
explosionsGroup = pygame.sprite.Group()
powerupsGroup = pygame.sprite.Group()

Player.containers = playerGroup
WaterBalloon.containers = projectilesGroup
Enemy.containers = enemiesGroup
Crate.containers = cratesGroup
Explosion.containers = explosionsGroup
PowerUp.containers = powerupsGroup

enemy_spawn_timer_max = 100
enemy_spawn_timer = 0
enemy_spawn_speedup_timer_max = 400
enemy_spawn_speedup_timer = enemy_spawn_speedup_timer_max

bulkenemy_spawn_timer_max = 400
bulkenemy_spawn_timer = 0

game_started = False


class GameMode(Enum):
    EASY = 1
    NORMAL = 2
    HARD = 3


def StartGameWithMode(gameMode):
    global game_started, hud, local_player, enemy_spawn_timer_max, enemy_spawn_timer, enemy_spawn_speedup_timer, bulkenemy_spawn_timer_max, bulkenemy_spawn_timer
    game_started = True
    hud.state = 'ingame'
    local_player.__init__(screen, game_width / 2, game_height / 2)
    if gameMode == GameMode.EASY:
        enemy_spawn_timer_max = 200
        bulkenemy_spawn_timer_max = 800
    elif gameMode == GameMode.NORMAL:
        enemy_spawn_timer_max = 100
        bulkenemy_spawn_timer_max = 400
    elif gameMode == GameMode.HARD:
        enemy_spawn_timer_max = 60
        bulkenemy_spawn_timer_max = 120

    enemy_spawn_timer = 0
    bulkenemy_spawn_timer = 0

    enemy_spawn_speedup_timer = enemy_spawn_speedup_timer_max
    for i in range(0, 10):
        ExplosiveCrate(screen, random.randint(0, game_width), random.randint(0, game_height), local_player)
        Crate(screen, random.randint(0, game_width), random.randint(0, game_height), local_player)


local_player = Player(screen, game_width / 2, game_height / 2)
hud = HUD(screen, local_player)
cheat_code_handler = CheatCodeHandler(local_player, hud, screen)

# ***************** Loop Land Below *****************
# Everything under 'while running' will be repeated over and over again
while running:
    # Makes the game stop if the player clicks the X or presses esc
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()

    screen.blit(background_img, (0, 0))

    if not game_started:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                StartGameWithMode(GameMode.NORMAL)
                break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                StartGameWithMode(GameMode.EASY)
                break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                StartGameWithMode(GameMode.HARD)
                break
            elif event.type == pygame.KEYDOWN:
                hud.start_text = hud.hud_font.render("Invalid input, try again!"
                                                     " E - Easy, N - Normal, H - Hard", True, (255, 255, 255))

    # some comments
    if game_started:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            local_player.move(0, -1, cratesGroup)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            local_player.move(-1, 0, cratesGroup)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            local_player.move(0, 1, cratesGroup)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            local_player.move(1, 0, cratesGroup)
        if pygame.mouse.get_pressed()[0]:
            local_player.shoot()
        if keys[pygame.K_SPACE]:
            local_player.placeCrate()
        if pygame.mouse.get_pressed()[2]:
            local_player.placeExplosiveCrate()

        cheat_code_handler.handle(keys)

        enemy_spawn_speedup_timer -= 1
        if enemy_spawn_speedup_timer <= 0:
            if enemy_spawn_timer_max > 20 and bulkenemy_spawn_timer_max > 80:
                enemy_spawn_timer_max -= 10
                bulkenemy_spawn_timer_max -= 40
            enemy_spawn_speedup_timer = enemy_spawn_speedup_timer_max

        enemy_spawn_timer -= 1
        if enemy_spawn_timer <= 0:
            new_enemy = Enemy(screen, 0, 0, local_player)
            new_speedy = Speedy(screen, 0, 0, local_player)
            side_to_spawn = random.randint(0, 3)
            if side_to_spawn == 0:
                new_enemy.y = -new_enemy.image.get_height()
                new_enemy.x = random.randint(0, game_width)
                new_speedy.y = -new_speedy.image.get_height()
                new_speedy.x = random.randint(0, game_width)
            elif side_to_spawn == 1:
                new_enemy.x = random.randint(0, game_width)
                new_enemy.y = game_height + new_enemy.image.get_height()
                new_speedy.x = random.randint(0, game_width)
                new_speedy.y = game_height + new_speedy.image.get_height()
            elif side_to_spawn == 2:
                new_enemy.x = -new_enemy.image.get_width()
                new_enemy.y = random.randint(0, game_height)
                new_speedy.x = -new_speedy.image.get_width()
                new_speedy.y = random.randint(0, game_height)
            elif side_to_spawn == 3:
                new_enemy.x = game_width + new_enemy.image.get_width()
                new_enemy.y = random.randint(0, game_height)
                new_speedy.x = game_width + new_speedy.image.get_width()
                new_speedy.y = random.randint(0, game_height)
            enemy_spawn_timer = enemy_spawn_timer_max

        bulkenemy_spawn_timer -= 1
        if bulkenemy_spawn_timer <= 0:
            new_bulk_enemy = Bulky(screen, 0, 0, local_player)
            side_to_spawn = random.randint(0, 3)
            if side_to_spawn == 0:
                new_bulk_enemy.y = -new_bulk_enemy.image.get_height()
                new_bulk_enemy.x = random.randint(0, game_width)
            elif side_to_spawn == 1:
                new_bulk_enemy.x = random.randint(0, game_width)
                new_bulk_enemy.y = game_height + new_bulk_enemy.image.get_height()
            elif side_to_spawn == 2:
                new_bulk_enemy.x = -new_bulk_enemy.image.get_width()
                new_bulk_enemy.y = random.randint(0, game_height)
            elif side_to_spawn == 3:
                new_bulk_enemy.x = game_width + new_bulk_enemy.image.get_width()
                new_bulk_enemy.y = random.randint(0, game_height)
            bulkenemy_spawn_timer = bulkenemy_spawn_timer_max

        for powerup in powerupsGroup:
            powerup.update(local_player)

        for explosion in explosionsGroup:
            explosion.update()

        for projectile in projectilesGroup:
            projectile.update()

        for enemy in enemiesGroup:
            enemy.update(projectilesGroup, cratesGroup, explosionsGroup)

        for crate in cratesGroup:
            crate.update(projectilesGroup, explosionsGroup)

        local_player.update(enemiesGroup, explosionsGroup)

        if not local_player.alive:
            if hud.state == 'ingame':
                hud.state = 'gameover'
            elif hud.state == 'mainmenu':
                game_started = False
                playerGroup.empty()
                projectilesGroup.empty()
                enemiesGroup.empty()
                powerupsGroup.empty()
                cratesGroup.empty()
                explosionsGroup.empty()
                hud.start_text = hud.hud_font.render("Press E for Easy, N for Normal, and H for Hard!", True,
                                                     (255, 255, 255))

    hud.update()
    # Tell pygame to update the screen
    pygame.display.flip()
    clock.tick(40)
    pygame.display.set_caption("Attack Of The Robots fps: " + str(clock.get_fps()))
