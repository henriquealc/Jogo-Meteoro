
import pygame
import random
import os
import sys

# Inicializa todos os módulos do Pygame
pygame.init()

# Define as dimensões da janela do jogo
LARGURA, ALTURA = 800, 600

# Cria a janela principal do jogo
janela = pygame.display.set_mode((LARGURA, ALTURA))

# Define o título que aparece na janela
pygame.display.set_caption("Chuva de Meteoros")

# Cria um relógio para controlar a velocidade do jogo
relogio = pygame.time.Clock()

# Cria as fontes utilizadas nos textos do jogo
fonte_titulo = pygame.font.SysFont("arial", 56)
fonte = pygame.font.SysFont("arial", 28)
fonte_pequena = pygame.font.SysFont("arial", 22)


# LOCALIZAÇÃO DA PASTA DO JOGO

# Verifica se o programa está sendo executado como um executável
if getattr(sys, "frozen", False):

    # Obtém a pasta onde está localizado o executável
    PASTA = os.path.dirname(sys.executable)

else:

    # Obtém a pasta onde está localizado o arquivo Python
    PASTA = os.path.dirname(os.path.abspath(__file__))


# Função que monta o caminho completo dos arquivos do jogo
def caminho(*partes):

    # Junta a pasta principal com as demais pastas e nomes de arquivos
    return os.path.join(PASTA, *partes)


# CONFIGURAÇÕES DO JOGO

# Quantidade de meteoros que precisam ser destruídos para vencer
PONTOS_VITORIA = 20

# Define a velocidade de movimentação da nave
velocidade_nave = 5

# Define as dimensões da nave
TAMANHO_NAVE = 60

# Define as dimensões dos mísseis
LARGURA_MISSIL = 20
ALTURA_MISSIL = 40

# Define a velocidade de movimentação dos mísseis
VELOCIDADE_MISSIL = 10


# CARREGAMENTO DAS IMAGENS

try:

    # Carrega a imagem da nave
    imagem_nave = pygame.image.load(
        caminho("imagens", "nave.png")
    ).convert_alpha()

    # Redimensiona a imagem da nave
    imagem_nave = pygame.transform.scale(
        imagem_nave,
        (TAMANHO_NAVE, TAMANHO_NAVE)
    )

    # Cria uma lista para armazenar as imagens dos meteoros
    imagens_meteoro = []

    # Percorre os nomes das imagens dos meteoros
    for nome in ["meteoro1.png", "meteoro2.png"]:

        # Carrega cada imagem de meteoro
        imagem = pygame.image.load(
            caminho("imagens", nome)
        ).convert_alpha()

        # Adiciona a imagem carregada à lista
        imagens_meteoro.append(imagem)

    # Carrega a imagem do míssil
    imagem_missil = pygame.image.load(
        caminho("imagens", "missil.png")
    ).convert_alpha()

    # Redimensiona a imagem do míssil
    imagem_missil = pygame.transform.scale(
        imagem_missil,
        (LARGURA_MISSIL, ALTURA_MISSIL)
    )

# Captura erros caso alguma imagem não seja encontrada ou carregada
except (pygame.error, FileNotFoundError) as erro:

    # Exibe a descrição do erro no terminal
    print("Erro ao carregar imagens:", erro)

    # Encerra o Pygame
    pygame.quit()

    # Finaliza a execução do programa
    sys.exit()


# CARREGAMENTO DA MÚSICA

try:

    # Carrega a música de fundo
    pygame.mixer.music.load(
        caminho("sons", "musica.mp3")
    )

    # Define o volume da música em 40%
    pygame.mixer.music.set_volume(0.4)

    # Inicia a música em repetição contínua
    pygame.mixer.music.play(-1)

# Captura erros caso a música não seja encontrada ou carregada
except (pygame.error, FileNotFoundError):

    # Informa que não foi possível carregar a música
    print("Nao foi possivel carregar a musica")


# FUNÇÃO PARA CENTRALIZAR TEXTOS NA TELA

def texto_centro(texto, fonte_usada, cor, y):

    # Transforma o texto em uma imagem que pode ser desenhada
    imagem = fonte_usada.render(texto, True, cor)

    # Calcula a posição para deixar o texto centralizado
    posicao = imagem.get_rect(
        center=(LARGURA // 2, y)
    )

    # Desenha o texto na janela do jogo
    janela.blit(imagem, posicao)


# FUNÇÃO PARA INICIAR UMA NOVA PARTIDA

def novo_jogo():

    # Cria o retângulo que representa a nave
    # A nave começa centralizada na parte inferior da tela
    nave = pygame.Rect(
        LARGURA // 2 - TAMANHO_NAVE // 2,
        520,
        TAMANHO_NAVE,
        TAMANHO_NAVE
    )

    # Retorna os valores iniciais da partida:
    # Nave, vidas, pontos, lista de meteoros,
    # lista de tiros e contador de criação de meteoros
    return nave, 3, 0, [], [], 0


# ESTADO INICIAL DO JOGO

# Define que o jogo começa mostrando o menu principal
estado = "menu"

# Inicializa as variáveis da partida
nave, vidas, pontos, meteoros, tiros, contador_spawn = novo_jogo()

# Controla se o jogo continuará em execução
rodando = True


# LOOP PRINCIPAL DO JOGO

while rodando:

    # VERIFICAÇÃO DOS EVENTOS DO TECLADO E DA JANELA

    for evento in pygame.event.get():

        # Verifica se o jogador clicou no botão de fechar a janela
        if evento.type == pygame.QUIT:

            # Encerra o loop principal
            rodando = False

        # Verifica se alguma tecla foi pressionada
        elif evento.type == pygame.KEYDOWN:

            # Se estiver no menu e pressionar ENTER, inicia uma partida
            if estado == "menu" and evento.key == pygame.K_RETURN:

                # Reinicia todas as variáveis da partida
                nave, vidas, pontos, meteoros, tiros, contador_spawn = novo_jogo()

                # Muda o estado para jogo em andamento
                estado = "jogando"

            # Se estiver jogando e pressionar ESPAÇO, dispara um míssil
            elif estado == "jogando" and evento.key == pygame.K_SPACE:

                # Cria um retângulo para representar o míssil
                # Ele aparece centralizado na parte superior da nave
                tiros.append(
                    pygame.Rect(
                        nave.centerx - LARGURA_MISSIL // 2,
                        nave.top,
                        LARGURA_MISSIL,
                        ALTURA_MISSIL
                    )
                )

            # Se estiver na tela de vitória ou derrota e pressionar ENTER,
            # retorna ao menu principal
            elif estado in ("vitoria", "derrota") and evento.key == pygame.K_RETURN:

                # Altera o estado para o menu
                estado = "menu"


    # LÓGICA PRINCIPAL DA PARTIDA

    # Executa a movimentação e as colisões somente durante o jogo
    if estado == "jogando":

        # Obtém as teclas que estão sendo pressionadas
        teclas = pygame.key.get_pressed()

        # Movimenta a nave para a esquerda usando a seta ou a tecla A
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            nave.x -= velocidade_nave

        # Movimenta a nave para a direita usando a seta ou a tecla D
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            nave.x += velocidade_nave

        # Movimenta a nave para cima usando a seta ou a tecla W
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            nave.y -= velocidade_nave

        # Movimenta a nave para baixo usando a seta ou a tecla S
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            nave.y += velocidade_nave

        # Impede que a nave saia dos limites da janela
        nave.clamp_ip(janela.get_rect())


        # CRIAÇÃO DOS METEOROS

        # Aumenta o contador a cada quadro do jogo
        contador_spawn += 1

        # Cria um novo meteoro quando o contador chega a 40
        if contador_spawn >= 40:

            # Zera o contador para iniciar uma nova contagem
            contador_spawn = 0

            # Escolhe aleatoriamente o tamanho do meteoro
            tamanho = random.randint(40, 70)

            # Escolhe uma posição horizontal aleatória
            x = random.randint(0, LARGURA - tamanho)

            # Escolhe aleatoriamente a velocidade do meteoro
            velocidade = random.randint(3, 7)

            # Escolhe uma imagem aleatória e redimensiona
            imagem = pygame.transform.scale(
                random.choice(imagens_meteoro),
                (tamanho, tamanho)
            )

            # Adiciona o meteoro à lista
            # Cada meteoro possui posição, velocidade e imagem
            meteoros.append([
                pygame.Rect(x, -tamanho, tamanho, tamanho),
                velocidade,
                imagem
            ])


        # MOVIMENTAÇÃO E COLISÃO DOS METEOROS

        # Percorre uma cópia da lista para permitir remover meteoros
        # durante a verificação
        for meteoro in meteoros[:]:

            # Faz o meteoro descer de acordo com sua velocidade
            meteoro[0].y += meteoro[1]

            # Verifica se o meteoro atingiu a nave
            if meteoro[0].colliderect(nave):

                # Diminui uma vida do jogador
                vidas -= 1

                # Remove o meteoro que atingiu a nave
                meteoros.remove(meteoro)

            # Verifica se o meteoro saiu pela parte inferior da tela
            elif meteoro[0].top > ALTURA:

                # Remove o meteoro que saiu da tela
                meteoros.remove(meteoro)


        # MOVIMENTAÇÃO E COLISÃO DOS MÍSSEIS

        # Percorre uma cópia da lista de tiros
        for tiro in tiros[:]:

            # Faz o míssil subir pela tela
            tiro.y -= VELOCIDADE_MISSIL

            # Verifica se o míssil saiu pela parte superior da tela
            if tiro.bottom < 0:

                # Remove o míssil que saiu da tela
                tiros.remove(tiro)

                # Pula para o próximo míssil
                continue

            # Verifica colisões entre o míssil e os meteoros
            for meteoro in meteoros[:]:

                # Verifica se o retângulo do míssil atingiu o meteoro
                if tiro.colliderect(meteoro[0]):

                    # Remove o míssil após o impacto
                    tiros.remove(tiro)

                    # Remove o meteoro atingido
                    meteoros.remove(meteoro)

                    # Adiciona um ponto ao jogador
                    pontos += 1

                    # Interrompe a verificação deste míssil
                    break


        # VERIFICAÇÃO DAS CONDIÇÕES DE VITÓRIA E DERROTA

        # Verifica se o jogador perdeu todas as vidas
        if vidas <= 0:

            # Altera o estado para a tela de derrota
            estado = "derrota"

        # Verifica se o jogador alcançou a pontuação necessária
        elif pontos >= PONTOS_VITORIA:

            # Altera o estado para a tela de vitória
            estado = "vitoria"


    # DESENHO DO FUNDO

    # Preenche toda a janela com uma cor azul-escura
    janela.fill((10, 10, 40))


    # EXIBIÇÃO DO MENU PRINCIPAL

    if estado == "menu":

        # Exibe o título do jogo
        texto_centro(
            "CHUVA DE METEOROS",
            fonte_titulo,
            (0, 200, 255),
            130
        )

        # Exibe o objetivo da partida
        texto_centro(
            "Destrua 20 meteoros sem perder suas 3 vidas",
            fonte,
            (255, 255, 255),
            220
        )

        # Exibe o título da seção de controles
        texto_centro(
            "Controles",
            fonte,
            (255, 230, 80),
            300
        )

        # Informa como movimentar a nave
        texto_centro(
            "Setas ou W A S D - Mover a nave",
            fonte_pequena,
            (255, 255, 255),
            345
        )

        # Informa como disparar os mísseis
        texto_centro(
            "Espaco - Atirar",
            fonte_pequena,
            (255, 255, 255),
            380
        )

        # Informa qual tecla inicia a partida
        texto_centro(
            "Enter - Iniciar",
            fonte_pequena,
            (255, 255, 255),
            415
        )

        # Exibe uma mensagem para iniciar o jogo
        texto_centro(
            "Pressione ENTER para jogar",
            fonte,
            (200, 200, 200),
            520
        )


    # EXIBIÇÃO DA PARTIDA

    elif estado == "jogando":

        # Desenha a imagem da nave na posição atual
        janela.blit(imagem_nave, nave)

        # Desenha todos os meteoros existentes na tela
        for meteoro in meteoros:
            janela.blit(meteoro[2], meteoro[0])

        # Desenha todos os mísseis existentes na tela
        for tiro in tiros:
            janela.blit(imagem_missil, tiro)

        # Cria o texto que mostra as vidas e a pontuação
        texto = fonte.render(
            f"Vidas: {vidas}   Pontos: {pontos}",
            True,
            (255, 255, 255)
        )

        # Desenha as informações no canto superior esquerdo
        janela.blit(texto, (10, 10))


    # EXIBIÇÃO DA TELA DE VITÓRIA

    elif estado == "vitoria":

        # Exibe a mensagem de vitória
        texto_centro(
            "VOCE VENCEU!",
            fonte_titulo,
            (80, 220, 100),
            250
        )

        # Exibe a pontuação final
        texto_centro(
            f"Pontos: {pontos}",
            fonte,
            (255, 255, 255),
            330
        )

        # Informa como voltar ao menu
        texto_centro(
            "Pressione ENTER para voltar ao menu",
            fonte_pequena,
            (200, 200, 200),
            450
        )


    # EXIBIÇÃO DA TELA DE DERROTA

    elif estado == "derrota":

        # Exibe a mensagem de fim de jogo
        texto_centro(
            "GAME OVER",
            fonte_titulo,
            (220, 70, 70),
            250
        )

        # Exibe a pontuação final
        texto_centro(
            f"Pontos: {pontos}",
            fonte,
            (255, 255, 255),
            330
        )

        # Informa como voltar ao menu
        texto_centro(
            "Pressione ENTER para voltar ao menu",
            fonte_pequena,
            (200, 200, 200),
            450
        )


    # ATUALIZAÇÃO DA TELA

    # Atualiza a janela para mostrar todos os elementos desenhados
    pygame.display.flip()

    # Limita o jogo a 60 quadros por segundo
    relogio.tick(60)


# ENCERRAMENTO DO JOGO

# Finaliza os módulos do Pygame ao sair do loop principal
pygame.quit()
