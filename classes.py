import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy
import pathlib

pygame.init()
virtual_width, virtual_height = 320, 180
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
screen = pygame.display.set_mode((0, 0), pygame.OPENGL | pygame.DOUBLEBUF)
virtual_screen = pygame.Surface((virtual_width, virtual_height))
texture = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texture)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, virtual_width, virtual_height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
vertices = [
    -1,  1, 0.0, 1.0,
    -1, -1, 0.0, 0.0,
     1, -1, 1.0, 0.0,
     1,  1, 1.0, 1.0,
]
indices = [0, 1, 2, 2, 3, 0]
vertices = numpy.array(vertices)
indices = numpy.array(indices)

VAO = glGenVertexArrays(1)
VBO = glGenBuffers(1)
EBO = glGenBuffers(1)

glBindVertexArray(VAO)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.itemsize * len(vertices), vertices, GL_STATIC_DRAW)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.itemsize * len(indices), indices, GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * vertices.itemsize, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * vertices.itemsize, ctypes.c_void_p(2 * vertices.itemsize))
clock = pygame.time.Clock()


def load_shader(vertex_path, fragment_path):
    with open(vertex_path, 'r') as file:
        vertex_src = file.read()
    with open(fragment_path, 'r') as file:
        fragment_src = file.read()
    return compileProgram(
        compileShader(vertex_src, GL_VERTEX_SHADER),
        compileShader(fragment_src, GL_FRAGMENT_SHADER),
    )


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
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2

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
            self.image = pygame.transform.scale(self.image, (64, 64))


def start_game():
    running = True
    while running:
        dt = clock.tick(60)
        keys = pygame.key.get_pressed()
        virtual_screen.fill((0, 0, 0))
        player.update(keys, dt)
        player.draw(virtual_screen)
        glBindTexture(GL_TEXTURE_2D, texture)
        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(shader)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


player = Hero(virtual_width//2, virtual_height//2)
shader = load_shader("shaders/vertex_shader.glsl", "shaders/fragment_shader.glsl")
