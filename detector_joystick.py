import pygame
import sys
import os

def limpar_tela():
    """Limpa a tela do console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Inicializa o pygame
    pygame.init()
    
    # Configura a janela
    largura, altura = 800, 600
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Detector de Joystick")
    
    # Fonte para exibir texto
    fonte = pygame.font.SysFont(None, 24)
    
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
    for i in range(num_joysticks):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        joysticks.append(joystick)
        
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
        
        # Limpa a tela
        tela.fill((0, 0, 0))
        
        # Exibe informações de cada joystick
        y_pos = 10
        for i, joystick in enumerate(joysticks):
            # Informações básicas do joystick
            texto = fonte.render(f"Joystick {i}: {joystick.get_name()}", True, (255, 255, 255))
            tela.blit(texto, (10, y_pos))
            y_pos += 30
            
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
