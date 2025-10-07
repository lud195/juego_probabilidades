import pygame, random

def jugar_dados(saldo, pantalla):
    # --- Colores coquette ---
    ROSA = (255, 182, 193)
    ROSA_CLARO = (255, 200, 221)
    ROSA_FUERTE = (255, 105, 180)
    CREMA = (255, 240, 245)
    DORADO = (255, 223, 186)
    BLANCO = (255, 255, 255)
    NEGRO = (40, 40, 40)
    LILA = (200, 162, 200)

    ANCHO, ALTO = pantalla.get_size()
    titulo_fuente = pygame.font.SysFont("Comic Sans MS", 44, bold=True)
    texto_fuente = pygame.font.SysFont("Comic Sans MS", 26)
    mini_fuente = pygame.font.SysFont("Comic Sans MS", 20)

    apuesta = 0
    numero_elegido = None
    mensaje = "Elegí un número del 1 al 6 🍓"
    dado_resultado = None
    mostrar_resultado = False
    reloj = pygame.time.Clock()

    # Botones
    botones = {
        "GIRAR": pygame.Rect(600, 450, 150, 50),
        "+10": pygame.Rect(600, 510, 70, 40),
        "-10": pygame.Rect(680, 510, 70, 40),
        "ELEGIR": pygame.Rect(600, 390, 150, 50),
        "VOLVER": pygame.Rect(50, 520, 120, 40)
    }

    # Posición del dado
    dado_rect = pygame.Rect(ANCHO//2-60, 250, 120, 120)

    def dibujar_texto(texto, fuente, color, x, y, centrar=False):
        s = fuente.render(texto, True, color)
        r = s.get_rect(center=(x, y) if centrar else (x, y))
        pantalla.blit(s, r)

    def dibujar_boton(rect, texto, color_fondo, color_texto=NEGRO):
        pygame.draw.rect(pantalla, color_fondo, rect, border_radius=12)
        dibujar_texto(texto, mini_fuente, color_texto, rect.centerx, rect.centery, centrar=True)

    def dibujar_dado(num, rect):
        pygame.draw.rect(pantalla, ROSA_FUERTE, rect, border_radius=15)
        punto_radio = 8
        posiciones = {
            1: [(rect.centerx, rect.centery)],
            2: [(rect.left+30, rect.top+30), (rect.right-30, rect.bottom-30)],
            3: [(rect.left+30, rect.top+30), (rect.centerx, rect.centery), (rect.right-30, rect.bottom-30)],
            4: [(rect.left+30, rect.top+30), (rect.right-30, rect.top+30), (rect.left+30, rect.bottom-30), (rect.right-30, rect.bottom-30)],
            5: [(rect.left+30, rect.top+30), (rect.right-30, rect.top+30), (rect.centerx, rect.centery),
                (rect.left+30, rect.bottom-30), (rect.right-30, rect.bottom-30)],
            6: [(rect.left+30, rect.top+25), (rect.right-30, rect.top+25), (rect.left+30, rect.centery), (rect.right-30, rect.centery),
                (rect.left+30, rect.bottom-25), (rect.right-30, rect.bottom-25)]
        }
        for (x, y) in posiciones[num]:
            pygame.draw.circle(pantalla, BLANCO, (x, y), punto_radio)

    run = True
    while run:
        pantalla.fill(CREMA)
        dibujar_texto("Dados de Frutillas", titulo_fuente, ROSA_FUERTE, ANCHO//2, 40, centrar=True)
        dibujar_texto(f"Saldo: {saldo}", texto_fuente, NEGRO, 40, 80)
        dibujar_texto(f"Apuesta: {apuesta}", mini_fuente, NEGRO, 40, 120)
        dibujar_texto(mensaje, mini_fuente, NEGRO, ANCHO//2, 180, centrar=True)

        if mostrar_resultado and dado_resultado:
            dibujar_dado(dado_resultado, dado_rect)

        # Dibujar botones
        for nombre, rect in botones.items():
            color = ROSA_FUERTE if nombre in ["GIRAR","ELEGIR"] else LILA if nombre=="VOLVER" else ROSA_CLARO
            dibujar_boton(rect, nombre, color, BLANCO if nombre=="VOLVER" else NEGRO)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                # +10 apuesta
                if botones["+10"].collidepoint(mx, my) and saldo >= 10:
                    apuesta += 10
                    saldo -= 10

                # -10 apuesta
                elif botones["-10"].collidepoint(mx, my) and apuesta >= 10:
                    apuesta -= 10
                    saldo += 10

                # Elegir número (pantalla emergente)
                elif botones["ELEGIR"].collidepoint(mx, my):
                    seleccionando = True
                    while seleccionando:
                        pantalla.fill(CREMA)
                        dibujar_texto("Elegí un número del 1 al 6", mini_fuente, NEGRO, ANCHO//2, 100, centrar=True)
                        botones_num = []
                        for i in range(6):
                            rect = pygame.Rect(100+i*100, 200, 80, 80)
                            pygame.draw.rect(pantalla, ROSA_CLARO if i%2==0 else ROSA, rect, border_radius=15)
                            dibujar_texto(str(i+1), texto_fuente, BLANCO, rect.centerx, rect.centery, centrar=True)
                            botones_num.append(rect)
                        pygame.display.flip()
                        for e2 in pygame.event.get():
                            if e2.type == pygame.QUIT:
                                seleccionando = False
                                run = False
                            if e2.type == pygame.MOUSEBUTTONDOWN and e2.button == 1:
                                mx2, my2 = e2.pos
                                for i, rect in enumerate(botones_num):
                                    if rect.collidepoint(mx2, my2):
                                        numero_elegido = i+1
                                        mensaje = f"Elegiste el número {numero_elegido}"
                                        mostrar_resultado = False
                                        seleccionando = False

                # Girar
                elif botones["GIRAR"].collidepoint(mx, my):
                    if apuesta <= 0:
                        mensaje = "Primero apostá con +10 💸"
                    elif numero_elegido is None:
                        mensaje = "Elegí un número antes de girar 🎯"
                    else:
                        dado_resultado = random.randint(1,6)
                        mostrar_resultado = True
                        if numero_elegido == dado_resultado:
                            saldo += apuesta*5
                            mensaje = f"¡Ganaste {apuesta*5} frutillas! 🎉"
                        else:
                            mensaje = f"Tiraste {dado_resultado}. Perdiste {apuesta} frutillas 😢"
                            saldo -= apuesta
                        apuesta = 0
                        numero_elegido = None

                # Volver
                elif botones["VOLVER"].collidepoint(mx, my):
                    run = False

        pygame.display.flip()
        reloj.tick(60)

    return saldo
