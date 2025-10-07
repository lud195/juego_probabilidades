import pygame, random

def jugar_cartas(saldo, pantalla):
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
    mensaje = "Elegí tu carta 🍓"
    carta_elegida = None
    carta_ganadora = None
    mostrar_ganadora = False
    reloj = pygame.time.Clock()

    def dibujar_texto(texto, fuente, color, x, y, centrar=False):
        s = fuente.render(texto, True, color)
        r = s.get_rect(center=(x, y) if centrar else (x, y))
        pantalla.blit(s, r)

    def dibujar_boton(rect, texto, color_fondo, color_texto=NEGRO):
        pygame.draw.rect(pantalla, color_fondo, rect, border_radius=12)
        dibujar_texto(texto, mini_fuente, color_texto, rect.centerx, rect.centery, centrar=True)

    botones = {
        "GIRAR": pygame.Rect(600, 450, 150, 50),
        "+10": pygame.Rect(600, 510, 70, 40),
        "-10": pygame.Rect(680, 510, 70, 40),
        "VOLVER": pygame.Rect(50, 520, 120, 40)
    }

    cartas_pos = [pygame.Rect(100+i*160, 220, 120, 180) for i in range(4)]

    run = True
    while run:
        pantalla.fill(CREMA)
        dibujar_texto("Cartas de Frutillas", titulo_fuente, ROSA_FUERTE, ANCHO//2, 40, centrar=True)
        dibujar_texto(f"Saldo: {saldo}", texto_fuente, NEGRO, 40, 80)
        dibujar_texto(f"Apuesta: {apuesta}", mini_fuente, NEGRO, 40, 120)
        dibujar_texto(mensaje, mini_fuente, NEGRO, ANCHO//2, 180, centrar=True)

        # Dibujar cartas
        for i, rect in enumerate(cartas_pos):
            color = ROSA_CLARO if i%2==0 else ROSA
            pygame.draw.rect(pantalla, color, rect, border_radius=15)
            dibujar_texto(str(i+1), texto_fuente, BLANCO, rect.centerx, rect.centery, centrar=True)
            if carta_elegida == i:
                pygame.draw.rect(pantalla, DORADO, rect, width=4, border_radius=15)

        # Carta ganadora
        if mostrar_ganadora and carta_ganadora is not None:
            center_rect = pygame.Rect(ANCHO//2-60, 430, 120, 180)
            pygame.draw.rect(pantalla, DORADO, center_rect, border_radius=15)
            dibujar_texto(f"Carta {carta_ganadora+1}", texto_fuente, BLANCO, center_rect.centerx, center_rect.centery, centrar=True)

        # Dibujar botones
        for nombre, rect in botones.items():
            color = ROSA_FUERTE if nombre=="GIRAR" else LILA if nombre=="VOLVER" else ROSA_CLARO
            dibujar_boton(rect, nombre, color, BLANCO if nombre=="VOLVER" else NEGRO)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                # Elegir carta
                for i, rect in enumerate(cartas_pos):
                    if rect.collidepoint(mx, my):
                        carta_elegida = i
                        mensaje = f"Elegiste la carta {carta_elegida+1}"
                        mostrar_ganadora = False

                # Girar
                if botones["GIRAR"].collidepoint(mx, my):
                    if apuesta <= 0:
                        mensaje = "Primero apostá con +10 💸"
                    elif carta_elegida is None:
                        mensaje = "Elegí una carta antes de girar 🎯"
                    else:
                        carta_ganadora = random.randint(0,3)
                        mostrar_ganadora = True
                        if carta_elegida == carta_ganadora:
                            saldo += apuesta*2
                            mensaje = f"¡Ganaste {apuesta*2} frutillas! 🎉"
                        else:
                            # Ya se descontó al apostar, no restamos de nuevo
                            mensaje = f"Perdiste {apuesta} frutillas 😢"
                        apuesta = 0
                        carta_elegida = None

                # +10 apuesta
                elif botones["+10"].collidepoint(mx, my):
                    if saldo >= 10:
                        apuesta += 10
                        saldo -= 10

                # -10 apuesta
                elif botones["-10"].collidepoint(mx, my):
                    if apuesta >= 10:
                        apuesta -= 10
                        saldo += 10

                # Volver
                elif botones["VOLVER"].collidepoint(mx, my):
                    run = False

        pygame.display.flip()
        reloj.tick(60)

    return saldo

