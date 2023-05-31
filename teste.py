import pygame
import math
import random
import time
from tela_inicial import tela_inicial

pygame.init()
pygame.mixer.init()

janela = pygame.display.set_mode((800,600))
pygame.display.set_caption('Historia de Lilith')

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
arma = pygame.transform.scale(arma, (50,50))

bala = pygame.image.load('assets/img/Bala-1.png.png').convert_alpha()

som_tiro = pygame.mixer.Sound('assets/snd/Star Wars Blaster Shot _ HD Sound Effect.mp3')
pygame.mixer.music.load('assets/snd/Vampire Survivors Soundtrack - Forest Night Fever_dxx6fvhf5Pc.mp3')
pygame.mixer.music.set_volume(0.4)

class Jogador:
    def __init__(self, x, y, largura, altura):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.frame = 0
        self.moverDireita = False
        self.moverEsquerda = False
        self.vida = 100

    def sombra(self, janela):
        pygame.draw.ellipse(janela, (51, 51, 51), (self.x+8, self.y+38, 30, 10))

    def arma_mao(self, janela):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x-jogador.x , mouse_y-jogador.y
        angulo = (180/math.pi)* -math.atan2(rel_y, rel_x)

        arma_copia = pygame.transform.rotate(arma, angulo)

        janela.blit(arma_copia, (self.x+32-int(arma_copia.get_width()/2), self.y+16-int(arma_copia.get_height()/2)))

    def tomaDano(self, amount):
        self.vida -= amount
        if self.vida < 0:
            self.vida = 0

    def barraVida(self, janela):
        width = 50
        height = 5
        x = self.x-1
        y = self.y-9
        pygame.draw.rect(janela, (158, 25, 25), (x, y, width, height, ), border_radius=4)
        barra_vida = int((self.vida/100)*width)
        pygame.draw.rect(janela, (0,255,0), (x, y, barra_vida, height), border_radius=4)

    def main(self, janela):
        if self.frame + 0.3 >= 16:
            self.frame = 0
        self.frame += 0.3

        if self.moverDireita:
            janela.blit(pygame.transform.scale(animation[int(self.frame)//4], (42, 42)), (self.x, self.y))
        elif self.moverEsquerda:
            janela.blit(pygame.transform.scale(pygame.transform.flip(animation[int(self.frame)//4], True, False), (42, 42)), (self.x, self.y))
        else:
            janela.blit(pygame.transform.scale(animation[int(self.frame)//4], (42, 42)), (self.x, self.y))

        self.arma_mao(janela)

        self.moverDireita = False
        self.moverEsquerda = False

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

        pygame.draw.circle(janela, (255,200,0), (self.x, self.y), 5)

class Inimigo:
    def __init__(self, x, y):
        self.image = inimigo_image
        self.x = x
        self.y = y
        self.offset_reset = 0
        self.offset_x = random.randrange(-150, 150)
        self.offset_y = random.randrange(-150, 150)
        self.vida = 100

    def sombra(self, janela):
        pygame.draw.ellipse(janela, (51, 51, 51), (self.x+3 - janela_mexe[0], self.y+37 - janela_mexe[1], 30, 10))

    def barraVida(self, janela):
        width = 30
        height = 3
        x = self.x+3
        y = self.y-9
        pygame.draw.rect(janela, (158, 25, 25), (x-janela_mexe[0], y-janela_mexe[1], width, height, ), border_radius=4)
        barra_vida = int((self.vida/100)*width)
        pygame.draw.rect(janela, (0,255,0), (x-janela_mexe[0], y-janela_mexe[1], barra_vida, height), border_radius=4)

    def main(self, janela):
        if jogador.x > self.x - janela_mexe[0]:
            self.x += 0.7
        elif jogador.x < self.x - janela_mexe[0]:
            self.x -= 0.7
        if jogador.y > self.y - janela_mexe[1]:
            self.y += 0.7
        elif jogador.y < self.y - janela_mexe[1]:
            self.y -= 0.7

        janela.blit(pygame.transform.scale(self.image, (32,32)), (int(self.x)-janela_mexe[0], int(self.y)-janela_mexe[1]))

# Gera o jogador
jogador = Jogador(400, 300, 32, 32)

#Contador de tempo em segundos
start_time = None
elapsed_time = 0
fonte = pygame.font.Font(None, 38)
def draw_time(time):
    text = fonte.render('Tempo: {} segundos'.format(time), True, (255,255,255))
    janela.blit(text, (10,10))

janela_mexe = [0,0]
# Lista de balas
balas_lista = []

# Gera e adiciona inimido na lista de inimigos
inimigo_lista = []
for i in range(20):
    x = random.randint(-800, 800)
    y = random.randint(-600, 600)
    inimigo = Inimigo(x, y)
    inimigo_lista.append(inimigo)

#JOGANDO = True
OVER = 3
INIT = 2
GAME = 1
QUIT = 0
state = INIT

# Tela inicial
if state == INIT:
    state = tela_inicial(janela)

# Inicia a música do jogo
pygame.mixer.music.play(loops=-1)
# Loop Principal
while state != QUIT:
    janela.fill((90,32,61))

    # Gera posições x e y do mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()         
    # Verifica todos os eventos 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            state = QUIT
            
        # Verifica evento de mouse clicado
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                balas_lista.append(BalaJogador(jogador.x+32, jogador.y+19, mouse_x, mouse_y))
                som_tiro.play()

    # Gera lista de teclas pressionadas
    teclas = pygame.key.get_pressed()
    # Desenha ponto de referência na tela
    pygame.draw.rect(janela, (255, 255, 255), (100-janela_mexe[0], 100-janela_mexe[1], 16, 16))
    # Eventos de tecla pressionada
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
    if teclas[pygame.K_SPACE]:
        jogador.tomaDano(1)
        if jogador.vida == 0:
            state = QUIT
    # Redenderiza jogador, sombra e barar de vida
    jogador.sombra(janela)
    jogador.main(janela)
    jogador.barraVida(janela)
    # Renderiza todas as balas
    for balas in balas_lista:
        balas.main(janela)

    # Renderiza todos os inimigos
    for inimigo in inimigo_lista:
        inimigo.main(janela)
        inimigo.sombra(janela)


    if start_time is None:
        start_time = time.time()
    else:
        tempo_atual = time.time()
        elapsed_time = int(tempo_atual - start_time)
    draw_time(elapsed_time)


    clock.tick(60)
    pygame.display.update()