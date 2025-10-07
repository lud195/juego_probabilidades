import pygame
import random
import math

def jugar_ruleta(saldo, pantalla):
    # --- colores coquette ---
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
    mensaje = "Bienvenida — elegí un número"
    girando = False
    angulo = 0.0
    velocidad = 0.0
    numero_ganador = None

    SEGMENTOS = 10
    SEG_SIZE = 360.0 / SEGMENTOS
    FLECHA_ANGLE = 270.0

    reloj = pygame.time.Clock()

    def dibujar_texto(texto, fuente, color, x, y, centrar=False):
        s = fuente.render(texto, True, color)
        r = s.get_rect(center=(x, y) if centrar else (x, y))
        pantalla.blit(s, r)

    def boton_rect(x, y, w, h, color, texto, texto_color=NEGRO):
        pygame.draw.rect(pantalla, color, (x, y, w, h), border_radius=12)
        dibujar_texto(texto, mini_fuente, texto_color, x + w//2, y + h//2, centrar=True)

    def dibujar_ruleta(centro, radio, angulo_actual):
        for i in range(SEGMENTOS):
            start = angulo_actual + i * SEG_SIZE
            end = start + SEG_SIZE
            color = ROSA_CLARO if i % 2 == 0 else ROSA
            puntos = [centro]
            step = 6
            for deg in range(int(start), int(end)+1, step):
                rad = math.radians(deg)
                x = centro[0] + radio * math.cos(rad)
                y = centro[1] + radio * math.sin(rad)
                puntos.append((x, y))
            pygame.draw.polygon(pantalla, color, puntos)

        for i in range(SEGMENTOS):
            center_deg = angulo_actual + i * SEG_SIZE + SEG_SIZE/2
            rad = math.radians(center_deg)
            x = centro[0] + (radio - 60) * math.cos(rad)
            y = centro[1] + (radio - 60) * math.sin(rad)
            dibujar_texto(str(i), texto_fuente, DORADO, x, y, centrar=True)

        pygame.draw.circle(pantalla, BLANCO, centro, 34)
        pygame.draw.circle(pantalla, DORADO, centro, 10)

    def obtener_segmento_bajo_flecha(angulo_actual):
        return int(((FLECHA_ANGLE - angulo_actual) % 360) // SEG_SIZE) % SEGMENTOS

    def girar_si_puede():
        nonlocal girando, velocidad, mensaje, numero_ganador
        if girando:
            return
        if apuesta <= 0:
            mensaje = "Primero apostá (botón +10) 💸"
            return
        if numero_elegido is None:
            mensaje = "Elegí un número primero 🎯"
            return
        girando = True
        velocidad = random.uniform(18.0, 32.0)
        numero_ganador = None
        mensaje = "Girando..."

    run = True
    while run:
        pantalla.fill(CREMA)
        dibujar_texto("Ruleta", titulo_fuente, ROSA_FUERTE, ANCHO//2, 40, centrar=True)
        dibujar_texto(f"Saldo: {saldo}", texto_fuente, NEGRO, 40, 80)
        dibujar_texto(mensaje, mini_fuente, NEGRO, ANCHO//2, 110, centrar=True)

        centro = (ANCHO//2, ALTO//2 + 40)
        radio = 170
        dibujar_ruleta(centro, radio, angulo)

        arrow_top = (centro[0], centro[1] - radio - 18)
        arrow_left = (centro[0] - 16, centro[1] - radio + 8)
        arrow_right = (centro[0] + 16, centro[1] - radio + 8)
        pygame.draw.polygon(pantalla, DORADO, [arrow_top, arrow_left, arrow_right])

        dibujar_texto(f"Apuesta: {apuesta}", mini_fuente, NEGRO, 40, 430)
        dibujar_texto(f"Número elegido: {numero_elegido if numero_elegido is not None else '-'}", mini_fuente, NEGRO, 40, 460)
        boton_rect(600, 420, 150, 40, ROSA_FUERTE, "GIRAR")
        boton_rect(600, 470, 70, 34, ROSA_CLARO, "+10")
        boton_rect(680, 470, 70, 34, ROSA_CLARO, "-10")
        boton_rect(600, 520, 150, 34, DORADO, "Elegir número")
        boton_rect(50, 520, 120, 34, LILA, "VOLVER", BLANCO)

        if numero_ganador is not None:
            dibujar_texto(f"GANÓ EL {numero_ganador}", texto_fuente, NEGRO, ANCHO//2, 520, centrar=True)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                if 600 <= mx <= 750 and 420 <= my <= 460:
                    girar_si_puede()
                elif 600 <= mx <= 670 and 470 <= my <= 504:
                    if saldo >= 10:
                        apuesta += 10
                        saldo -= 10
                elif 680 <= mx <= 750 and 470 <= my <= 504:
                    if apuesta >= 10:
                        apuesta -= 10
                        saldo += 10
                elif 600 <= mx <= 750 and 520 <= my <= 554:
                    seleccionando = True
                    while seleccionando:
                        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
                        overlay.fill((255,255,255,200))
                        pantalla.blit(overlay, (0,0))
                        dibujar_texto("Elegí un número (0-9)", mini_fuente, NEGRO, ANCHO//2, 120, centrar=True)
                        start_x = 60
                        for i in range(SEGMENTOS):
                            bx = start_x + i*70
                            by = 200
                            boton_rect(bx, by, 60, 60, ROSA_CLARO if i%2==0 else ROSA, str(i))
                        pygame.display.flip()
                        for ev2 in pygame.event.get():
                            if ev2.type == pygame.QUIT:
                                run = False
                                seleccionando = False
                            if ev2.type == pygame.MOUSEBUTTONDOWN and ev2.button == 1:
                                mx2, my2 = ev2.pos
                                for i in range(SEGMENTOS):
                                    bx = start_x + i*70
                                    by = 200
                                    if bx <= mx2 <= bx+60 and by <= my2 <= by+60:
                                        numero_elegido = i
                                        mensaje = f"Elegiste el número {numero_elegido}"
                                        seleccionando = False
                                        break
                            if ev2.type == pygame.KEYDOWN and ev2.key == pygame.K_ESCAPE:
                                seleccionando = False

        # VOLVER
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            if 50 <= mx <= 170 and 520 <= my <= 554:
                run = False

        if girando:
            angulo += velocidad
            velocidad *= 0.985
            if velocidad < 0.15:
                girando = False
                angulo %= 360
                numero_ganador = obtener_segmento_bajo_flecha(angulo)
                mensaje = f"Este número ganó: {numero_ganador}"
                if numero_elegido == numero_ganador:
                    saldo += apuesta * 3
                    mensaje += " — Acierto, cobras x3!"
                else:
                    mensaje += " — Lo siento, perdiste la apuesta."
                apuesta = 0
                numero_elegido = None

        pygame.display.flip()
        reloj.tick(60)

    return saldo
