import pygame
import pathlib

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
screen_width, screen_height = pygame.display.get_window_size()
clock = pygame.time.Clock()


# def animated(dt, person1, person2, animation_type):
#     animation_timer = 0
#     current_frame = 0
#     animation_timer += dt
#
#     if animation_timer > 150:
#         if current_frame == 4:
#             current_frame = 0
#         current_frame += 1
#         animation_timer = 0
#         return pygame.image.load(f"img/{person1}/{person2}/{animation_type}/{person2}_{current_frame}.png")


class Hero(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.person1 = 'hero'
        self.person2 = 'cyber_night'
        self.animation_type = 'stable'
        self.animation_timer = 0
        self.current_frame = 0
        self.image = pygame.image.load(f"img/{self.person1}/{self.person2}/{self.animation_type}/{self.person2}_1.png")
        self.image = pygame.transform.scale(self.image, (256, 256))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self, keys, dt):
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.animation_type = 'moving'
        if keys[pygame.K_s]:
            self.rect.y += self.speed
            self.animation_type = 'moving'
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.animation_type = 'moving'
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.animation_type = 'moving'
        self.animation_timer += dt
        if self.animation_timer > 150:
            animation_folder = pathlib.Path(f"img/{self.person1}/{self.person2}/{self.animation_type}/")
            if self.current_frame == len(list(animation_folder.iterdir())):
                self.current_frame = 0
            self.current_frame += 1
            self.animation_timer = 0
            self.image = pygame.image.load(
                f"img/{self.person1}/{self.person2}/{self.animation_type}/{self.person2}_{self.current_frame}.png"
            )
            self.image = pygame.transform.scale(self.image, (256, 256))


def start_game():
    running = True
    while running:
        dt = clock.tick(60)
        keys = pygame.key.get_pressed()
        screen.fill((0, 0, 0))
        player.update(keys, dt)
        player.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


player = Hero(screen_width//2, screen_height//2)
