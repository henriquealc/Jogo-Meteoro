
import pygame
import random
import os
import sys

pygame.init()

LARGURA, ALTURA = 800, 600
janela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Chuva de Meteoros")

relogio = pygame.time.Clock()

fonte_titulo = pygame.font.SysFont("arial", 56)
fonte = pygame.font.SysFont("arial", 28)
fonte_pequena = pygame.font.SysFont("arial", 22)

# Localizar pasta do jogo
if getattr(sys, "frozen", False):
    PASTA = os.path.dirname(sys.executable)
else:
    PASTA = os.path.dirname(os.path.abspath(__file__))


def caminho(*partes):
    return os.path.join(PASTA, *partes)


PONTOS_VITORIA = 20
velocidade_nave = 5

TAMANHO_NAVE = 60
LARGURA_MISSIL = 20
ALTURA_MISSIL = 40
VELOCIDADE_MISSIL = 10


# Carregar imagens
try:
    imagem_nave = pygame.image.load(
        caminho("imagens", "nave.png")
    ).convert_alpha()

    imagem_nave = pygame.transform.scale(
        imagem_nave,
        (TAMANHO_NAVE, TAMANHO_NAVE)
    )

    imagens_meteoro = []

    for nome in ["meteoro1.png", "meteoro2.png"]:
        imagem = pygame.image.load(
            caminho("imagens", nome)
        ).convert_alpha()

        imagens_meteoro.append(imagem)

    imagem_missil = pygame.image.load(
        caminho("imagens", "missil.png")
    ).convert_alpha()

    imagem_missil = pygame.transform.scale(
        imagem_missil,
        (LARGURA_MISSIL, ALTURA_MISSIL)
    )

except (pygame.error, FileNotFoundError) as erro:
    print("Erro ao carregar imagens:", erro)
    pygame.quit()
    sys.exit()


# Música
try:
    pygame.mixer.music.load(
        caminho("sons", "musica.mp3")
    )

    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

except (pygame.error, FileNotFoundError):
    print("Nao foi possivel carregar a musica")


# Texto centralizado
def texto_centro(texto, fonte_usada, cor, y):
    imagem = fonte_usada.render(texto, True, cor)

    posicao = imagem.get_rect(
        center=(LARGURA // 2, y)
    )

    janela.blit(imagem, posicao)


# Reiniciar jogo
def novo_jogo():
    nave = pygame.Rect(
        LARGURA // 2 - TAMANHO_NAVE // 2,
        520,
        TAMANHO_NAVE,
        TAMANHO_NAVE
    )

    return nave, 3, 0, [], [], 0


estado = "menu"

nave, vidas, pontos, meteoros, tiros, contador_spawn = novo_jogo()

rodando = True

while rodando:

    # Eventos
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        elif evento.type == pygame.KEYDOWN:

            if estado == "menu" and evento.key == pygame.K_RETURN:
                nave, vidas, pontos, meteoros, tiros, contador_spawn = novo_jogo()
                estado = "jogando"

            elif estado == "jogando" and evento.key == pygame.K_SPACE:
                tiros.append(
                    pygame.Rect(
                        nave.centerx - LARGURA_MISSIL // 2,
                        nave.top,
                        LARGURA_MISSIL,
                        ALTURA_MISSIL
                    )
                )

            elif estado in ("vitoria", "derrota") and evento.key == pygame.K_RETURN:
                estado = "menu"

    # Lógica do jogo
    if estado == "jogando":

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            nave.x -= velocidade_nave

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            nave.x += velocidade_nave

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            nave.y -= velocidade_nave

        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            nave.y += velocidade_nave

        nave.clamp_ip(janela.get_rect())

        # Criar meteoros
        contador_spawn += 1

        if contador_spawn >= 40:
            contador_spawn = 0

            tamanho = random.randint(40, 70)
            x = random.randint(0, LARGURA - tamanho)
            velocidade = random.randint(3, 7)

            imagem = pygame.transform.scale(
                random.choice(imagens_meteoro),
                (tamanho, tamanho)
            )

            meteoros.append([
                pygame.Rect(x, -tamanho, tamanho, tamanho),
                velocidade,
                imagem
            ])

        # Movimentar meteoros
        for meteoro in meteoros[:]:

            meteoro[0].y += meteoro[1]

            if meteoro[0].colliderect(nave):
                vidas -= 1
                meteoros.remove(meteoro)

            elif meteoro[0].top > ALTURA:
                meteoros.remove(meteoro)

        # Movimentar mísseis
        for tiro in tiros[:]:

            tiro.y -= VELOCIDADE_MISSIL

            if tiro.bottom < 0:
                tiros.remove(tiro)
                continue

            for meteoro in meteoros[:]:

                if tiro.colliderect(meteoro[0]):
                    tiros.remove(tiro)
                    meteoros.remove(meteoro)
                    pontos += 1
                    break

        # Verificar resultado
        if vidas <= 0:
            estado = "derrota"

        elif pontos >= PONTOS_VITORIA:
            estado = "vitoria"

    # Desenhar fundo
    janela.fill((10, 10, 40))

    if estado == "menu":

        texto_centro(
            "CHUVA DE METEOROS",
            fonte_titulo,
            (0, 200, 255),
            130
        )

        texto_centro(
            "Destrua 20 meteoros sem perder suas 3 vidas",
            fonte,
            (255, 255, 255),
            220
        )

        texto_centro(
            "Controles",
            fonte,
            (255, 230, 80),
            300
        )

        texto_centro(
            "Setas ou W A S D - Mover a nave",
            fonte_pequena,
            (255, 255, 255),
            345
        )

        texto_centro(
            "Espaco - Atirar",
            fonte_pequena,
            (255, 255, 255),
            380
        )

        texto_centro(
            "Enter - Iniciar",
            fonte_pequena,
            (255, 255, 255),
            415
        )

        texto_centro(
            "Pressione ENTER para jogar",
            fonte,
            (200, 200, 200),
            520
        )

    elif estado == "jogando":

        janela.blit(imagem_nave, nave)

        for meteoro in meteoros:
            janela.blit(meteoro[2], meteoro[0])

        for tiro in tiros:
            janela.blit(imagem_missil, tiro)

        texto = fonte.render(
            f"Vidas: {vidas}   Pontos: {pontos}",
            True,
            (255, 255, 255)
        )

        janela.blit(texto, (10, 10))

    elif estado == "vitoria":

        texto_centro(
            "VOCE VENCEU!",
            fonte_titulo,
            (80, 220, 100),
            250
        )

        texto_centro(
            f"Pontos: {pontos}",
            fonte,
            (255, 255, 255),
            330
        )

        texto_centro(
            "Pressione ENTER para voltar ao menu",
            fonte_pequena,
            (200, 200, 200),
            450
        )

    elif estado == "derrota":

        texto_centro(
            "GAME OVER",
            fonte_titulo,
            (220, 70, 70),
            250
        )

        texto_centro(
            f"Pontos: {pontos}",
            fonte,
            (255, 255, 255),
            330
        )

        texto_centro(
            "Pressione ENTER para voltar ao menu",
            fonte_pequena,
            (200, 200, 200),
            450
        )

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
