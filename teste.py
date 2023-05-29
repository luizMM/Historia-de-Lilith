import pygame
import math
import random

pygame.init()

janela = pygame.display.set_mode((800,600))
pygame.display.set_caption('So pra testar')

clock = pygame.time.Clock()

animation = []
animation.append(pygame.image.load('assets/img/animacao player/Lilith_animacao-1.png.png').convert_alpha())
animation.append(pygame.image.load('assets/img/animacao player/Lilith_animacao-2.png.png').convert_alpha())
animation.append(pygame.image.load('assets/img/animacao player/Lilith_animacao-3.png.png').convert_alpha())
animation.append(pygame.image.load('assets/img/animacao player/Lilith_animacao-4.png.png').convert_alpha())
animation.append(pygame.image.load('assets/img/animacao player/Lilith_animacao-5.png.png').convert_alpha())
animation.append(pygame.image.load('assets/img/animacao player/Lilith_animacao-6.png.png').convert_alpha())
animation.append(pygame.image.load('assets/img/animacao player/Lilith_animacao-7.png.png').convert_alpha())

inimigo_image = pygame.image.load('assets/img/amogus-1.png.png').convert_alpha()
inimigo_image = pygame.transform.scale(inimigo_image, (32,32))

arma = pygame.image.load('assets/img/Arma-1.png.png').convert_alpha()
arma = pygame.transform.scale(arma, (45,45))


class Jogador:
    def __init__(self, x, y, largura, altura):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.frame = 0
        self.moverEsquerda = False
        self.moverDireita = False

    def arma_mao(self, janela):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - jogador.x, mouse_y - jogador.y
        angulo = (180 / math.pi) * -math.atan2(rel_y, rel_x)

        arma_copia = pygame.transform.rotate(arma, int(angulo))

        janela.blit(arma_copia,(self.x+32-int(arma_copia.get_width()/2), self.y+16-int(arma_copia.get_height()/2)))
        
                    
    def main(self, janela):
        if self.frame + 0.3 >= 16:
            self.frame = 0
        self.frame += 0.3
        if self.moverDireita:
            janela.blit(pygame.transform.scale(animation[int(self.frame)//4], (42, 42)), (self.x, self.y))
        elif self.moverEsquerda:
            janela.blit(pygame.transform.flip(pygame.transform.scale(animation[int(self.frame)//4], (42, 42)), True, False), (self.x, self.y))
        else:
            janela.blit(pygame.transform.scale(animation[int(self.frame)//4], (42, 42)), (self.x, self.y))

        self.arma_mao(janela)

        self.moverEsquerda = False
        self.moverDireita = False

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

class Inimigo:
    def __init__(self, x, y):
        self.image = inimigo_image
        self.x = x
        self.y = y
        self.offset_reset = 0
        self.offset_x = random.randrange(-150, 150)
        self.offset_y = random.randrange(-150, 150)


    def main(self, janela):
        if jogador.x > self.x - janela_mexe[0]:
            self.x += 0.7
            #janela.blit(pygame.transform.scale(pygame.transform.flip(self.image, True, False) (32,32)), (int(self.x)-janela_mexe[0], int(self.y)-janela_mexe[1]))
        elif jogador.x < self.x - janela_mexe[0]:
            self.x -= 0.7
            #janela.blit(pygame.transform.scale(self.image, (32,32)), (int(self.x)-janela_mexe[0], int(self.y)-janela_mexe[1]))
        if jogador.y > self.y - janela_mexe[1]:
            self.y += 0.7
        elif jogador.y < self.y - janela_mexe[1]:
            self.y -= 0.7

        janela.blit(pygame.transform.scale(self.image, (32,32)), (int(self.x)-janela_mexe[0], int(self.y)-janela_mexe[1]))

jogador = Jogador(400, 300, 32, 32)

janela_mexe = [0,0]

balas_lista = []

inimigo_lista = []
for i in range(12):
    x = random.randint(-800, 800)
    y = random.randint(-600, 600)
    inimigo = Inimigo(x, y)
    inimigo_lista.append(inimigo)

JOGANDO = True
while JOGANDO:
    janela.fill((90,32,61))

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                balas_lista.append(BalaJogador(jogador.x+32, jogador.y+19, mouse_x, mouse_y))
        
    teclas = pygame.key.get_pressed()

    pygame.draw.rect(janela, (255, 255, 255), (100-janela_mexe[0], 100-janela_mexe[1], 16, 16))

    if teclas[pygame.K_a]:
        janela_mexe[0] -= 5
        jogador.moverEsquerda = True
    if teclas[pygame.K_d]:
        janela_mexe[0] += 5
        jogador.moverDireita = True
    if teclas[pygame.K_w]:
        janela_mexe[1] -= 5
    if teclas[pygame.K_s]:
        janela_mexe[1] += 5

    jogador.main(janela)

    for balas in balas_lista:
        balas.main(janela)

    for inimigo in inimigo_lista:
        inimigo.main(janela)

    clock.tick(60)
    pygame.display.update()
