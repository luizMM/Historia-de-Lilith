import pygame

pygame.init()

FPS = 60
WIDTH = 600
HEIGHT = 500

janela = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Histora de Lilith')

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50

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
        self.rect.topleft = 100,100
        self.rect.centerx = WIDTH/2
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.frame += 0.12
        if self.frame  >= len(self.animation):
               self.frame = 0
        self.image = self.animation[int(self.frame)]
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH,PLAYER_HEIGHT))

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

def game_screen(janela):
    clock = pygame.time.Clock()

    all_sprite = pygame.sprite.Group()
    groups = {}
    groups['all_sprite'] = all_sprite

    player = Player()
    all_sprite.add(player)

    keys_down = {}

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
        all_sprite.draw(janela)

        #atualiza a tela
        pygame.display.update()

game_screen(janela)

pygame.quit()