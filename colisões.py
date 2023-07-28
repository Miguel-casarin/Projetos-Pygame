import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

fps = pygame.time.Clock()
# posição
x = int(640 / 2)
y = int(480 / 2)
# posição x y segundo quadrado
x_magenta = randint(40, 600)
y_magenta = randint(50, 430)

fonte =pygame.font.SysFont('arial',40,True,True)

tela = pygame.display.set_mode((640, 480))
pygame.display.set_caption('miguelzin studios')
pontos=0

while True:
    fps.tick(30)

    tela.fill((0, 0, 0))

    mensagem= f'pontos:{pontos}'
    textoformatado=fonte.render(mensagem, True,(40,80,150))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    if pygame.key.get_pressed()[K_a]:
        x = x - 20
    if pygame.key.get_pressed()[K_d]:
        x = x + 20
    if pygame.key.get_pressed()[K_w]:
        y = y - 20
    if pygame.key.get_pressed()[K_s]:
        y = y + 20

    quadradociano = pygame.draw.rect(tela, (0, 255, 255), (x, y, 50, 50))
    quadradomagenta = pygame.draw.rect(tela, (255, 0, 255), (x_magenta, y_magenta, 50, 50))

    if quadradociano.colliderect(quadradomagenta):
        x_magenta = randint(40, 600)
        y_magenta = randint(50, 430)

        pontos=pontos + 1

    tela.blit(textoformatado, (250,40))
    pygame.display.update()
