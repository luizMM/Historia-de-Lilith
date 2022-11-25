import pygame
from mapa import mapa

pygame.init()

FPS = 60
WIDTH = 800
HEIGHT = 700

janela = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Histora de Lilith')

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50

def load_assets():
    assets = {}
    assets['esquerda'] = pygame.image.load('assets/img/parede esquerda-1.png.png').convert()
    assets['esquerda'] = pygame.transform.scale(assets['esquerda'], (50,50))
    assets['direita'] = pygame.image.load('assets/img/parede direita-1.png.png').convert()
    assets['cima'] = pygame.image.load('assets/img/cima-1.png.png').convert()
    assets['baixo'] = pygame.image.load('assets/img/baixo-1.png.png').convert()
    return assets

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
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.frame += 0.12
        if self.frame  >= len(self.animation):
               self.frame = 0
        self.image = self.animation[int(self.frame)]
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH,PLAYER_HEIGHT))

        bkpx = self.rect.x
        bkpy = self.rect.y
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        i = (self.rect.x + (PLAYER_WIDTH//2) - 100) // 50
        j = (self.rect.y + (PLAYER_HEIGHT//2) - 100) //  50
        if i >= 0 and i < len(mapa[0]) and j >= 0 and j < len(mapa[0]):
            if mapa[i][j] == 1:
                self.rect.x = bkpx
                self.rect.y = bkpy

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Parede(pygame.sprite.Sprite):
    def __init__(self,x,y,assets):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets['cima']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect= self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def game_screen(janela):
    clock = pygame.time.Clock()

    all_sprite = pygame.sprite.Group()
    all_bricks = pygame.sprite.Group()
    groups = {}
    groups['all_sprite'] = all_sprite
    groups['all_bricks'] = all_bricks

    player = Player()
    all_sprite.add(player)

    keys_down = {}

    assets = load_assets()
    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            if mapa[j][i] == 1:
                x = 100 + (j) * 50
                y = 100 + (i) * 50
                parede = Parede(x,y,assets)
                all_bricks.add(parede)

    ACABOU = 0 
    JOGANDO = 1
    state = JOGANDO

    while state != ACABOU:
        clock.tick(FPS)

        for event in pygame.event.get():
            #verifica evento de fechar janela
            if event.type == pygame.QUIT:
                state = ACABOU
            if state == JOGANDO:
                #verifica eventos de teclas
                if event.type == pygame.KEYDOWN:
                    keys_down[event.key] = True
                    if event.key == pygame.K_w:
                        player.speedy -= 4
                    if  event.key == pygame.K_s:
                        player.speedy += 4
                    if event.key == pygame.K_a:
                        player.speedx -= 4
                    if event.key == pygame.K_d:
                        player.speedx += 4
                if event.type == pygame.KEYUP:
                    if event.key in keys_down and keys_down[event.key]:
                        if event.key == pygame.K_w:
                            player.speedy += 4
                        if  event.key == pygame.K_s:
                            player.speedy -= 4
                        if event.key == pygame.K_a:
                            player.speedx += 4
                        if event.key == pygame.K_d:
                            player.speedx -= 4
        #atualiza todas sprites
        all_sprite.update()

        #pinta a janela de uma cor
        janela.fill((99,32,61))

        #desenha tas as sprite na tela
        all_bricks.draw(janela)
        all_sprite.draw(janela)

        #atualiza a tela
        pygame.display.update()

game_screen(janela)

pygame.quit()