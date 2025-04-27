import pygame
import sys
import os

def limpar_tela():
    """Limpa a tela do console"""
    os.system('cls' if os.name == 'nt' else 'clear')

class Botao:
    """Classe para criar botões interativos na interface"""
    def __init__(self, x, y, largura, altura, texto, cor_normal=(100, 100, 100), cor_hover=(150, 150, 150), cor_clique=(200, 200, 200)):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_normal = cor_normal
        self.cor_hover = cor_hover
        self.cor_clique = cor_clique
        self.cor_atual = cor_normal
        self.clicado = False
        self.acao_executada = False

    def desenhar(self, tela, fonte):
        # Desenha o retângulo do botão
        pygame.draw.rect(tela, self.cor_atual, self.rect, 0, 3)
        pygame.draw.rect(tela, (200, 200, 200), self.rect, 2, 3)

        # Renderiza o texto do botão
        texto_surface = fonte.render(self.texto, True, (255, 255, 255))
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        tela.blit(texto_surface, texto_rect)

    def verificar_evento(self, evento):
        # Verifica se o mouse está sobre o botão
        pos_mouse = pygame.mouse.get_pos()
        mouse_sobre = self.rect.collidepoint(pos_mouse)

        # Estado padrão
        self.cor_atual = self.cor_normal

        # Mouse sobre o botão
        if mouse_sobre:
            self.cor_atual = self.cor_hover

            # Clique no botão
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                self.cor_atual = self.cor_clique
                self.clicado = True
                self.acao_executada = False
                return False

            # Soltar o botão após clique
            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1 and self.clicado:
                self.clicado = False
                if not self.acao_executada:
                    self.acao_executada = True
                    return True

        # Mouse saiu do botão enquanto clicava
        elif self.clicado and evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            self.clicado = False

        return False

def main():
    # Inicializa o pygame
    pygame.init()

    # Configura a janela
    largura, altura = 800, 600
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Detector de Joystick")

    # Fontes para exibir texto
    fonte = pygame.font.SysFont(None, 24)
    fonte_titulo = pygame.font.SysFont(None, 28)

    # Inicializa o módulo de joystick
    pygame.joystick.init()

    # Verifica quantos joysticks estão conectados
    num_joysticks = pygame.joystick.get_count()

    if num_joysticks == 0:
        print("Nenhum joystick detectado. Conecte um joystick e execute novamente.")
        pygame.quit()
        return

    # Inicializa todos os joysticks detectados
    joysticks = []
    joystick_habilitado = []  # Lista para controlar quais joysticks estão habilitados
    botoes_habilitar = []     # Lista para armazenar os botões de habilitar/desabilitar

    for i in range(num_joysticks):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        joysticks.append(joystick)
        joystick_habilitado.append(True)  # Todos os joysticks começam habilitados

        # Cria botão para habilitar/desabilitar este joystick
        botao = Botao(650, 10 + i * 100, 120, 30, "Desabilitar",
                     cor_normal=(180, 0, 0), cor_hover=(220, 0, 0), cor_clique=(255, 0, 0))
        botoes_habilitar.append(botao)

        print(f"Joystick {i} detectado:")
        print(f"  Nome: {joystick.get_name()}")
        print(f"  ID: {joystick.get_instance_id()}")
        print(f"  Número de botões: {joystick.get_numbuttons()}")
        print(f"  Número de eixos: {joystick.get_numaxes()}")
        print(f"  Número de hats: {joystick.get_numhats()}")
        print()

    print("Pressione ESC para sair ou use o joystick para ver os eventos.")

    # Loop principal
    executando = True
    clock = pygame.time.Clock()

    while executando:
        # Processa eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    executando = False

            # Verifica eventos dos botões
            for i, botao in enumerate(botoes_habilitar):
                if botao.verificar_evento(evento):
                    # Alterna o estado do joystick (habilitado/desabilitado)
                    joystick_habilitado[i] = not joystick_habilitado[i]

                    # Atualiza o texto e a cor do botão
                    if joystick_habilitado[i]:
                        botao.texto = "Desabilitar"
                        botao.cor_normal = (180, 0, 0)
                        botao.cor_hover = (220, 0, 0)
                        botao.cor_clique = (255, 0, 0)
                    else:
                        botao.texto = "Habilitar"
                        botao.cor_normal = (0, 180, 0)
                        botao.cor_hover = (0, 220, 0)
                        botao.cor_clique = (0, 255, 0)

        # Limpa a tela
        tela.fill((20, 20, 30))

        # Título da aplicação
        titulo = fonte_titulo.render("DETECTOR DE JOYSTICK - Clique nos botões para habilitar/desabilitar", True, (255, 255, 255))
        tela.blit(titulo, (20, 10))
        pygame.draw.line(tela, (100, 100, 100), (10, 40), (790, 40), 2)

        # Exibe informações de cada joystick
        y_pos = 50
        for i, joystick in enumerate(joysticks):
            # Desenha o botão de habilitar/desabilitar
            botoes_habilitar[i].desenhar(tela, fonte)

            # Informações básicas do joystick
            status_texto = "HABILITADO" if joystick_habilitado[i] else "DESABILITADO"
            status_cor = (0, 255, 0) if joystick_habilitado[i] else (255, 0, 0)

            texto = fonte_titulo.render(f"Joystick {i}: {joystick.get_name()} - {status_texto}", True, status_cor)
            tela.blit(texto, (10, y_pos))
            y_pos += 30

            # Se o joystick estiver desabilitado, mostra apenas informações básicas
            if not joystick_habilitado[i]:
                texto = fonte.render("Este joystick está desabilitado. Clique em 'Habilitar' para ativá-lo.", True, (200, 200, 200))
                tela.blit(texto, (30, y_pos))
                y_pos += 60
                continue

            # Exibe estado dos botões
            texto = fonte.render("Botões:", True, (255, 255, 255))
            tela.blit(texto, (10, y_pos))
            y_pos += 25

            for b in range(joystick.get_numbuttons()):
                estado = joystick.get_button(b)
                cor = (0, 255, 0) if estado else (255, 0, 0)
                texto = fonte.render(f"Botão {b}: {'Pressionado' if estado else 'Solto'}", True, cor)
                tela.blit(texto, (30, y_pos))
                y_pos += 20

            # Exibe estado dos eixos
            y_pos += 5
            texto = fonte.render("Eixos:", True, (255, 255, 255))
            tela.blit(texto, (10, y_pos))
            y_pos += 25

            for a in range(joystick.get_numaxes()):
                valor = joystick.get_axis(a)
                texto = fonte.render(f"Eixo {a}: {valor:.2f}", True, (255, 255, 255))
                tela.blit(texto, (30, y_pos))
                y_pos += 20

            # Exibe estado dos hats (direcionais)
            y_pos += 5
            texto = fonte.render("Hats:", True, (255, 255, 255))
            tela.blit(texto, (10, y_pos))
            y_pos += 25

            for h in range(joystick.get_numhats()):
                valor = joystick.get_hat(h)
                texto = fonte.render(f"Hat {h}: {valor}", True, (255, 255, 255))
                tela.blit(texto, (30, y_pos))
                y_pos += 20

            y_pos += 20

        # Atualiza a tela
        pygame.display.flip()
        clock.tick(30)

    # Finaliza o pygame
    pygame.quit()

if __name__ == "__main__":
    main()
