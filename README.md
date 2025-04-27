# Detector de Joystick

Uma solução simples para detectar e exibir informações sobre controles joystick conectados ao PC.

## Funcionalidades

- Detecção automática de todos os joysticks conectados
- Exibição de informações detalhadas sobre cada joystick:
  - Nome do dispositivo
  - ID do joystick
  - Número de botões
  - Número de eixos
  - Número de hats (direcionais)
- Monitoramento em tempo real do estado dos controles
- Disponível em duas versões: interface gráfica e console

## Requisitos

- Python 3.x
- Biblioteca Pygame

## Como usar

### Versão Console

```bash
python detector_joystick_console.py
```

Pressione Ctrl+C para sair.

### Versão com Interface Gráfica

```bash
python detector_joystick.py
```

Pressione ESC para sair.

## Exemplo de Saída

```
Joystick 0 detectado:
  Nome: Controller (Inno GamePad..)
  ID: 0
  Número de botões: 11
  Número de eixos: 6
  Número de hats: 1

Joystick 1 detectado:
  Nome: vJoy Device
  ID: 1
  Número de botões: 8
  Número de eixos: 8
  Número de hats: 0
```

## Licença

Este projeto está sob a licença MIT.
