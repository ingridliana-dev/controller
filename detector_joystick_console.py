import pygame
import sys
import os
import time
import msvcrt  # Biblioteca para entrada de teclado no Windows

def limpar_tela():
    """Limpa a tela do console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def kbhit():
    """Verifica se uma tecla foi pressionada (Windows)"""
    return msvcrt.kbhit()

def getch():
    """Obtém o caractere pressionado sem bloquear (Windows)"""
    if kbhit():
        return msvcrt.getch().decode('utf-8', errors='ignore')
    return None

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
    joystick_habilitado = []  # Lista para controlar quais joysticks estão habilitados

    for i in range(num_joysticks):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        joysticks.append(joystick)
        joystick_habilitado.append(True)  # Todos os joysticks começam habilitados

        print(f"Joystick {i}:")
        print(f"  Nome: {joystick.get_name()}")
        print(f"  ID: {joystick.get_instance_id()}")
        print(f"  Número de botões: {joystick.get_numbuttons()}")
        print(f"  Número de eixos: {joystick.get_numaxes()}")
        print(f"  Número de hats (direcionais): {joystick.get_numhats()}")
        print()

    print("COMANDOS:")
    print("  Pressione Ctrl+C para sair")
    print("  Pressione 'h' seguido de um número (0, 1, etc.) para habilitar um joystick")
    print("  Pressione 'd' seguido de um número (0, 1, etc.) para desabilitar um joystick")
    print("-" * 50)

    # Buffer para armazenar comandos
    comando_buffer = ""

    try:
        while True:
            # Processa eventos para atualizar o estado dos joysticks
            pygame.event.pump()

            limpar_tela()
            print("DETECTOR DE JOYSTICK - MODO CONSOLE")
            print("Pressione Ctrl+C para sair")
            print("Pressione 'h' + número para habilitar ou 'd' + número para desabilitar um joystick (ex: h0, d1)")
            if comando_buffer:
                print(f"Comando atual: {comando_buffer}")
            print("-" * 50)

            # Exibe informações de cada joystick em tempo real
            for i, joystick in enumerate(joysticks):
                status = "HABILITADO" if joystick_habilitado[i] else "DESABILITADO"
                print(f"Joystick {i}: {joystick.get_name()} - {status}")

                # Se o joystick estiver desabilitado, não mostra os detalhes
                if not joystick_habilitado[i]:
                    print("  Este joystick está desabilitado. Pressione 'h" + str(i) + "' para habilitá-lo.")
                    print()
                    continue

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

            # Verifica se há entrada do usuário (sem bloquear)
            if kbhit():
                char = getch()

                # Se for Enter, processa o comando
                if char == '\r':
                    # Processa comandos para habilitar/desabilitar joysticks
                    if comando_buffer.startswith('h') and len(comando_buffer) > 1:
                        try:
                            idx = int(comando_buffer[1:])
                            if 0 <= idx < len(joysticks):
                                joystick_habilitado[idx] = True
                                print(f"\nJoystick {idx} habilitado!")
                                time.sleep(1)
                        except ValueError:
                            pass

                    elif comando_buffer.startswith('d') and len(comando_buffer) > 1:
                        try:
                            idx = int(comando_buffer[1:])
                            if 0 <= idx < len(joysticks):
                                joystick_habilitado[idx] = False
                                print(f"\nJoystick {idx} desabilitado!")
                                time.sleep(1)
                        except ValueError:
                            pass

                    # Limpa o buffer após processar
                    comando_buffer = ""

                # Backspace - remove o último caractere
                elif char == '\b':
                    if comando_buffer:
                        comando_buffer = comando_buffer[:-1]

                # Adiciona o caractere ao buffer
                elif char.isprintable():
                    comando_buffer += char

            # Pequena pausa para não sobrecarregar a CPU
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nEncerrando o detector de joystick...")

    # Finaliza o pygame
    pygame.quit()

if __name__ == "__main__":
    main()
