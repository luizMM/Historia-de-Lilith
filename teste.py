import pygame
import math

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

class Jogador:
    def __init__(self, x, y, largura, altura):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.frame = 0
    def main(self, janela):
        if self.frame + 0.3 >= 16:
            self.frame = 0
        self.frame += 0.3
        janela.blit(pygame.transform.scale(animation[int(self.frame)//4], (42, 42)), (self.x, self.y))
        #pygame.draw.rect(janela, (255, 0, 0), (self.x, self.y, self.largura, self.altura))

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

JOGANDO = True
while JOGANDO:
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
                balas_lista.append(BalaJogador(jogador.x, jogador.y, mouse_x, mouse_y))
        
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

    clock.tick(60)
    pygame.display.update()
