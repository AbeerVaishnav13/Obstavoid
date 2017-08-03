import pygame
import random
from time import sleep
from settings import *
from sprites import *

class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.total_frames = 0
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)

    def new(self):
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.backgrounds = pygame.sprite.Group()

        self.player = Player(self, "images/lam_top.png")
        self.all_sprites.add(self.player)

        for obs in OBSTACLE_LIST:
            o = Obstacle(*obs)
            self.obstacles.add(o)

        self.bg = Background(0, 0)
        self.backgrounds.add(self.bg)

        self.paused = False
        self.win_score = random.randint(5, 11) * 10
        self.run()

    def run(self):
        #Game Loop
        self.playing = True
        self.win = False
        while self.playing:
            self.clock.tick(FPS)
            if self.total_frames <= 60:
                self.total_frames += 1
            else:
                self.total_frames = 0
            # print(self.total_frames)
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def update(self):
        #Game Loop - Update
        self.all_sprites.update()

        #Score Update / sec
        if self.total_frames % 30 == 0:
            self.score += 1

        #spawn random obstacles
        while len(self.obstacles) < 4:

            o = Obstacle(random.randint(0, WIDTH),
                         CONSTANT_OBSTACLE_DISTANCE + random.randint(-100, -20),
                         random.randint(100, 160),
                         random.randint(40, 60),
                         OBSTACLE_IMAGES[random.randint(0, 1)])

            self.obstacles.add(o)

        #spawn new background
        while len(self.backgrounds) <= 3:
            b = Background(0, -700)
            self.backgrounds.add(b)

        #scroll camera
        if self.player.rect.top <= HEIGHT/2:
            self.player.pos.y += abs(self.player.vel.y)
            for obst in self.obstacles:
                if obst.active:
                    obst.rect.y += abs(self.player.vel.y)
                elif not obst.active:
                    obst.rect.y += abs(3 * self.player.vel.y)
                if obst.rect.top >=  5/4 * HEIGHT:
                    obst.kill()
                    # if obst.active:
                    #     self.score += 1
            for bg in self.backgrounds:
                bg.rect.y += abs(self.player.vel.y)
                if bg.rect.top >= 5/4 * HEIGHT:
                    bg.kill()

        #collision detection
        for obs in self.obstacles:
            hits = pygame.sprite.collide_rect(self.player, obs)
            if hits:
                if obs.active and self.player.lives > 0:
                    self.player.lives -= 1
                    obs.de_activate()
                    self.score -= 5

                if self.player.lives <= 0:
                    self.player.vel.y = 0
            if  not obs.active and obs.rect.y > HEIGHT and self.player.lives <= 0:
                self.playing = False

        #Win condition
        if self.score >= self.win_score:
            self.playing = False
            self.win = True


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused


    def draw(self):
        #Game Loop - Draw
        self.backgrounds.draw(self.screen)
        #Display score
        self.draw_text("Score: {0}".format(self.score), 20, WHITE, WIDTH/6, 10)
        if self.player.lives > 1:
            self.draw_text("Lives: {0}".format(self.player.lives), 20, WHITE, WIDTH * 5/6, 10)
        else:
            self.draw_text("Life: {0}".format(self.player.lives), 40, RED, WIDTH * 3/4, 10)
        self.draw_text("Win Score: {0}".format(self.win_score), 20, WHITE, WIDTH/2, HEIGHT-30)

        if self.player.lives < 5:
            for i in range(0, 5 - self.player.lives):
                self.draw_text("-5", 25, RED, 10, 175 + (i*25))

        self.obstacles.draw(self.screen)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def show_start_screen(self):
        #Game start screen
        self.screen.fill(ORANGE)
        self.draw_text("OBSTAVOID", 65, BLACK, WIDTH/2, HEIGHT/6)
        self.draw_text("Use left and right", 30, BLUE, WIDTH/2, HEIGHT/2)
        self.draw_text("arrow keys to play!!", 30, BLUE, WIDTH/2, HEIGHT/2 + 40)
        self.draw_text("Press SPACE to start...", 30, BROWN, WIDTH/2, HEIGHT * 3/4)
        pygame.display.flip()
        self.wait_for_key()

    def show_game_over_screen(self):
        # Game over
        if not self.running:
            return
        self.screen.fill(RED)
        self.draw_text("GAME OVER!! :'(", 50, BLACK, WIDTH/2, HEIGHT/4)
        self.draw_text("Your Score: {0}".format(self.score), 30, YELLOW, WIDTH/2, HEIGHT/2)
        self.draw_text("Press SPACE to play again...", 30, GREEN, WIDTH/2, HEIGHT * 3/4)
        pygame.display.flip()
        self.wait_for_key()

    def show_win_screen(self):
        if not self.running:
            return
        self.screen.fill(LIGHTBLUE)
        self.draw_text("YOU WIN!! :D", 50, BLACK, WIDTH/2, HEIGHT/4)
        self.draw_text("Your Score: {0}".format(self.score), 30, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press SPACE to go to Home Screen...", 23, GREEN, WIDTH/2, HEIGHT * 3/4)
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    if not g.win:
        g.show_game_over_screen()
    elif g.win:
        g.show_win_screen()
        g.show_start_screen()

pygame.quit()
