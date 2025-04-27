import pygame
import sys
import os
import time

def limpar_tela():
    """Limpa a tela do console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # Inicializa o pygame (apenas o módulo de joystick)
    pygame.init()
    pygame.joystick.init()
    
    # Verifica quantos joysticks estão conectados
    num_joysticks = pygame.joystick.get_count()
    
    if num_joysticks == 0:
        print("Nenhum joystick detectado. Conecte um joystick e execute novamente.")
        pygame.quit()
        return
    
    print(f"Número de joysticks detectados: {num_joysticks}")
    print("-" * 50)
    
    # Inicializa todos os joysticks detectados
    joysticks = []
    for i in range(num_joysticks):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        joysticks.append(joystick)
        
        print(f"Joystick {i}:")
        print(f"  Nome: {joystick.get_name()}")
        print(f"  ID: {joystick.get_instance_id()}")
        print(f"  Número de botões: {joystick.get_numbuttons()}")
        print(f"  Número de eixos: {joystick.get_numaxes()}")
        print(f"  Número de hats (direcionais): {joystick.get_numhats()}")
        print()
    
    print("Pressione Ctrl+C para sair ou use o joystick para ver os eventos em tempo real.")
    print("-" * 50)
    
    try:
        while True:
            # Processa eventos para atualizar o estado dos joysticks
            pygame.event.pump()
            
            limpar_tela()
            print("DETECTOR DE JOYSTICK - MODO CONSOLE")
            print("Pressione Ctrl+C para sair")
            print("-" * 50)
            
            # Exibe informações de cada joystick em tempo real
            for i, joystick in enumerate(joysticks):
                print(f"Joystick {i}: {joystick.get_name()}")
                
                # Exibe estado dos botões
                print("  Botões:")
                for b in range(joystick.get_numbuttons()):
                    estado = joystick.get_button(b)
                    print(f"    Botão {b}: {'PRESSIONADO' if estado else 'solto'}")
                
                # Exibe estado dos eixos
                print("  Eixos:")
                for a in range(joystick.get_numaxes()):
                    valor = joystick.get_axis(a)
                    print(f"    Eixo {a}: {valor:.2f}")
                
                # Exibe estado dos hats (direcionais)
                print("  Hats (direcionais):")
                for h in range(joystick.get_numhats()):
                    valor = joystick.get_hat(h)
                    print(f"    Hat {h}: {valor}")
                
                print()
            
            # Pequena pausa para não sobrecarregar a CPU
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nEncerrando o detector de joystick...")
    
    # Finaliza o pygame
    pygame.quit()

if __name__ == "__main__":
    main()
