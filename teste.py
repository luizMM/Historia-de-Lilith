import pygame
import math

pygame.init()

janela = pygame.display.set_mode((800,600))
pygame.display.set_caption('So pra testar')

clock = pygame.time.Clock()

class Jogador:
    def __init__(self, x, y, largura, altura):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
    def main(self, janela):
        pygame.draw.rect(janela, (255, 0, 0), (self.x, self.y, self.largura, self.altura))

class BalaJogador:
    def __init__(self, x, y, mouse_x, mouse_y):
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 15
        self.angulo = math.atan2(y-mouse_y, x-mouse_x)
        self.speedx = math.cos(self.angulo) * self.speed
        self.speedy = math.sin(self.angulo) * self.speed
    def main(self, janela):
        self.x -= int(self.speedx)
        self.y -= int(self.speedy)

        pygame.draw.circle(janela, (0,0,0), (self.x, self.y), 5)

jogador = Jogador(400, 300, 32, 32)

janela_mexe = [0,0]

balas_lista = []

JOGANDO = True
while JOGANDO:
    janela.fill((90,32,61))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                balas_lista.append(BalaJogador(jogador.x, jogador.y, mouse_x, mouse_y))
        
    teclas = pygame.key.get_pressed()

    pygame.draw.rect(janela, (255, 255, 255), (100-janela_mexe[0], 100-janela_mexe[1], 16, 16))

    if teclas[pygame.K_a]:
        janela_mexe[0] -= 5
    if teclas[pygame.K_d]:
        janela_mexe[0] += 5
    if teclas[pygame.K_w]:
        janela_mexe[1] -= 5
    if teclas[pygame.K_s]:
        janela_mexe[1] += 5

    jogador.main(janela)

    for balas in balas_lista:
        balas.main(janela)

    clock.tick(60)
    pygame.display.update()
