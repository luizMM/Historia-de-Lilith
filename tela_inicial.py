import pygame

GAME = 1
QUIT = 0

def tela_inicial(janela):
    clock = pygame.time.Clock()

    rodando = True
    while rodando:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
                rodando = False
            
            if event.type == pygame.KEYUP:
                state = GAME
                rodando = False
        
        janela.fill((0,0,0))

        image = pygame.image.load('assets/img/Lilith_animacao-1.png.gif').convert_alpha()
        image = pygame.transform.scale(image, (50,50))
        janela.blit(image, (370,260))

        fonte = pygame.font.SysFont(None,32)
        prescione = fonte.render('Prescione uma tecla para iniciar', False, (255,255,255))
        prescione_rect = prescione.get_rect()
        prescione_rect.midbottom = (400, 400)
        janela.blit(prescione,prescione_rect)

        font = pygame.font.SysFont(None,32)
        cima = font.render('Cima - [W]', False, (255,255,255))
        baixo = font.render('Baixo - [S]', False, (255,255,255))
        esquerda = font.render('Esquerda - [A]', False, (255,255,255))
        direita = font.render('Direita - [D]', False, (255,255,255))
        vida = font.render('Dano - [SPACE]', False, (255,255,255))
        atirar = font.render('Atirar - Botão Mouse Esquerdo', False, (255,255,255))
        janela.blit(cima, (10,10))
        janela.blit(esquerda, (10,40))
        janela.blit(baixo, (10,70))
        janela.blit(direita, (10,100))
        janela.blit(vida, (10,130))
        janela.blit(atirar, (10,160))

        pygame.display.flip()
    return state