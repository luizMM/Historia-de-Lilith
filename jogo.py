import pygame
import math
from mapa import mapa

pygame.init()

FPS = 70
WIDTH = 800
HEIGHT = 700

janela = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Histora de Lilith')

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50

#Carrega todos os assets
def load_assets():
    assets = {}
    assets['esquerda'] = pygame.image.load('assets/img/parede esquerda-1.png.png').convert()
    assets['esquerda'] = pygame.transform.scale(assets['esquerda'], (50,50))
    assets['direita'] = pygame.image.load('assets/img/parede direita-1.png.png').convert()
    assets['cima'] = pygame.image.load('assets/img/cima-1.png.png').convert()
    assets['baixo'] = pygame.image.load('assets/img/baixo-1.png.png').convert()
    return assets

#classe jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.animation = []
        self.animation.append(pygame.image.load('assets/img/animacao player/Lilith_animacao-1.png.png').convert_alpha())
        self.animation.append(pygame.image.load('assets/img/animacao player/Lilith_animacao-2.png.png').convert_alpha())
        self.animation.append(pygame.image.load('assets/img/animacao player/Lilith_animacao-3.png.png').convert_alpha())
        self.animation.append(pygame.image.load('assets/img/animacao player/Lilith_animacao-4.png.png').convert_alpha())
        self.animation.append(pygame.image.load('assets/img/animacao player/Lilith_animacao-5.png.png').convert_alpha())
        self.animation.append(pygame.image.load('assets/img/animacao player/Lilith_animacao-6.png.png').convert_alpha())
        self.animation.append(pygame.image.load('assets/img/animacao player/Lilith_animacao-7.png.png').convert_alpha())
        self.frame = 0
        self.image = self.animation[self.frame]
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH,PLAYER_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.bottom = HEIGHT/2
        self.rect.centerx = WIDTH/2

    def update(self):
        self.frame += 0.12
        if self.frame  >= len(self.animation):
               self.frame = 0
        self.image = self.animation[int(self.frame)]
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH,PLAYER_HEIGHT))

    def shoot(self):
        mouse_pos = pygame.mouse.get_pos()
        nova_bala = BalaJogador(self.rect.bottom, self.rect.centerx, mouse_pos[0], mouse_pos[1])
        self.groups['all_sprites'].add(nova_bala)
        self.groups['all_bullets'].add(nova_bala)

class BalaJogador(pygame.sprite.Sprite):
    def __init__(self, x, y, mouse_x, mouse_y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/img/Bala-1.png.png')
        self.x = x
        self.y = y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 15
        self.angulo = math.atan2(x-mouse_x, y-mouse_y)
        self.speedx = math.cos(self.angulo)*self.speed
        self.speedy = math.sin(self.angulo)*self.speed
    def update(self):
        self.x -= self.speedx
        self.y -= self.speedy

#carrega todas as imagens e informacoes na tela
def game_screen(janela):
    clock = pygame.time.Clock()

    all_balas = pygame.sprite.Group()
    all_sprite = pygame.sprite.Group()
    groups = {}
    groups['all_sprite'] = all_sprite
    groups['all_balas'] = all_balas

    player = Player()
    all_sprite.add(player)

    keys_down = {}
    janela_mexe = [0, 0]


    ACABOU = 0 
    JOGANDO = 1
    state = JOGANDO

    while state != ACABOU:
        clock.tick(FPS)

        teclas = pygame.key.get_pressed()
        #mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            #verifica evento de fechar janela
            if event.type == pygame.QUIT:
                state = ACABOU
        if state == JOGANDO:
            if teclas[pygame.K_w]:
                janela_mexe[1] -= 5
            if teclas[pygame.K_s]:
                janela_mexe[1] += 5
            if teclas[pygame.K_a]:
                janela_mexe[0] -= 5
            if teclas[pygame.K_d]:
                janela_mexe[0] += 5
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.shoot()


                    
        #atualiza todas sprites
        all_sprite.update() 

        #pinta a janela de uma cor
        janela.fill((99,32,61))

        #desenha tas as sprite na tela
        pygame.draw.rect(janela, (255, 255, 255), (100-janela_mexe[0], 100-janela_mexe[1], 16, 16))
        all_sprite.draw(janela)

        #atualiza a tela
        pygame.display.update()

game_screen(janela)

pygame.quit()