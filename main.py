import pygame
from juego1_ruleta import jugar_ruleta
from juego2_cartas import jugar_cartas
from juego3_dados import jugar_dados

pygame.init()

# --- COLORES / FUENTES ---
ROSA = (255, 182, 193)
ROSA_CLARO = (255, 200, 221)
ROSA_FUERTE = (255, 105, 180)
CREMA = (255, 240, 245)
DORADO = (255, 223, 186)
BLANCO = (255, 255, 255)
NEGRO = (40, 40, 40)
LILA = (200, 162, 200)

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juegos de Frutillas — Menú")

titulo_fuente = pygame.font.SysFont("Comic Sans MS", 44, bold=True)
texto_fuente = pygame.font.SysFont("Comic Sans MS", 26)
mini_fuente = pygame.font.SysFont("Comic Sans MS", 20)

reloj = pygame.time.Clock()

# Estado compartido
saldo = 100
mensaje = "¡Bienvenida! Elegí un juego y apostá frutillas 🍓"

# Botones (x, y, w, h)
botones = {
    "Ruleta": pygame.Rect(250, 150, 300, 60),
    "Cartas": pygame.Rect(250, 250, 300, 60),
    "Dados":  pygame.Rect(250, 350, 300, 60),
}

def dibujar_texto(texto, fuente, color, x, y, centrar=False):
    s = fuente.render(texto, True, color)
    r = s.get_rect(center=(x, y)) if centrar else s.get_rect(topleft=(x, y))
    pantalla.blit(s, r)

def dibujar_boton(rect, texto, hover=False):
    color = ROSA_FUERTE if hover else LILA
    borde = ROSA_CLARO if hover else ROSA
    pygame.draw.rect(pantalla, borde, rect.inflate(6,6), border_radius=20)
    pygame.draw.rect(pantalla, color, rect, border_radius=16)
    dibujar_texto(texto, mini_fuente, BLANCO, rect.centerx, rect.centery, centrar=True)

def dibujar_decoracion():
    pygame.draw.rect(pantalla, ROSA_CLARO, (0, 0, ANCHO, 120))
    pygame.draw.rect(pantalla, CREMA, (0, 120, ANCHO, ALTO-120))
    cx, cy = 120, 80
    pygame.draw.circle(pantalla, ROSA_FUERTE, (cx, cy), 20)
    pygame.draw.circle(pantalla, ROSA_CLARO, (cx-6, cy-6), 6)
    pygame.draw.polygon(pantalla, (100,190,120), [(cx-6, cy-22),(cx,cy-10),(cx+6,cy-22)])

# --- LOOP PRINCIPAL ---
run = True
while run:
    pantalla.fill(CREMA)
    dibujar_decoracion()
    dibujar_texto("Juegos de Frutillas", titulo_fuente, ROSA_FUERTE, ANCHO//2, 42, centrar=True)
    dibujar_texto(f"Saldo: {saldo} frutillas", texto_fuente, NEGRO, 40, 140)
    dibujar_texto(mensaje, mini_fuente, NEGRO, 40, 170)

    mx, my = pygame.mouse.get_pos()
    for nombre, rect in botones.items():
        dibujar_boton(rect, nombre, rect.collidepoint(mx, my))

    dibujar_texto("Click en un botón para entrar al juego. Volverás al menú cuando termines.", mini_fuente, NEGRO, ANCHO//2, ALTO-30, centrar=True)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            run = False
        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            if botones["Ruleta"].collidepoint(ev.pos):
                saldo = jugar_ruleta(saldo, pantalla)
                mensaje = "Volviste del juego Ruleta 💖"
            elif botones["Cartas"].collidepoint(ev.pos):
                saldo = jugar_cartas(saldo, pantalla)
                mensaje = "Volviste del juego Cartas 💖"
            elif botones["Dados"].collidepoint(ev.pos):
                saldo = jugar_dados(saldo, pantalla)
                mensaje = "Volviste del juego Dados 💖"

    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
