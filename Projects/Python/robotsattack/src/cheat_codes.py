import pygame
from explosion import Explosion
from crate import Crate
from crate import ExplosiveCrate
from random import randint


class CheatCodeHandler:
    def __init__(self, player, hud, screen):
        self.player = player
        self.hud = hud
        self.screen = screen

    def _addAmmo(self):
        self.player.special_ammo += 100

    def _activate(self):
        self.player.cheat_activated = 'True'
        acttext = self.hud.hud_font.render('Cheat activated!', True, (255, 255, 255))
        self.screen.blit(acttext, (10, 50))

    def _shotcd(self):
        self.player.shoot_cooldown_max = 1

    def _burstCheat(self):
        self._addAmmo()
        self.player.shot_type = 'burst'
        self._activate()
        self._shotcd()

    def _infCheat(self):
        self._addAmmo()
        self.player.shot_type = 'inf'
        self._activate()
        self._shotcd()

    def _explodeCheat(self):
        explosion_images = [pygame.image.load("../assets/HugeExplosion1.png"),
                            pygame.image.load("../assets/HugeExplosion2.png"),
                            pygame.image.load("../assets/HugeExplosion3.png")]
        self._activate()
        Explosion(self.screen, self.player.x, self.player.y, explosion_images, 5, 100, True)

    def _crateCheat(self):
        self._activate()
        self.player.crate_ammo += 100
        self.player.explosive_crate_ammo += 100
        self.player.crate_cooldown_max = 0

    def _restore(self):
        self.player.crate_ammo, self.player.explosive_crate_ammo = 10, 10
        self.player.crate_cooldown_max = 10
        self.player.cheat_activated = False
        self.player.shot_type = 'normal'
        self.player.shoot_cooldown_max = 10
        self.player.health = 30
        self.player.invincible_bool = False
        restoredtext = self.hud.hud_font.render('Restored!', True, (255, 255, 255))
        self.screen.blit(restoredtext, (10, 50))
        for x in range(1, 10):
            Crate(self.screen, randint(1, 1000), randint(1, 650), self.player)
            ExplosiveCrate(self.screen, randint(1, 1000), randint(1, 650), self.player)

    def _healthCheat(self):
        self._activate()
        self.player.health += 1

    def _invincibleCheat(self):
        self._activate()
        self.player.invincible_bool = True

    def _scoreCheat(self):
        self._activate()
        self.player.score += 100

    def handle(self, keys):
        ctrl = keys[pygame.K_LCTRL]
        if ctrl and keys[pygame.K_f]:
            self._burstCheat()
        if ctrl and keys[pygame.K_c]:
            self._infCheat()
        if ctrl and keys[pygame.K_e]:
            self._explodeCheat()
        if ctrl and keys[pygame.K_z]:
            self._crateCheat()
        if self.player.cheat_activated:
            if keys[pygame.K_TAB]:
                self._restore()
        if ctrl and keys[pygame.K_q]:
            self._healthCheat()
        if ctrl and keys[pygame.K_1]:
            self._invincibleCheat()
        if ctrl and keys[pygame.K_2]:
            self._scoreCheat()
