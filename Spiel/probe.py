import pygame
import sys
import map

pygame.init()

# Vollbild 1920x1080
screen = pygame.display.set_mode((1920, 1080), pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption("Quest 1892 – Die verlorene Meisterschale")
clock = pygame.time.Clock()

# Farben
schwarz  = (0, 0, 0)
weiss    = (255, 255, 255)
braun    = (101, 50, 10)
hellbraun = (180, 100, 30)
gold     = (212, 175, 55)
grau     = (180, 170, 150)

# Schriftarten
titel_font      = pygame.font.SysFont("georgia", 72, bold=True)
untertitel_font = pygame.font.SysFont("georgia", 28, italic=True)
button_font     = pygame.font.SysFont("georgia", 34, bold=True)
lore_font       = pygame.font.SysFont("georgia", 21)

# Bilder laden
hintergrund = pygame.transform.scale(
    pygame.image.load("Hintergründe/2/background.png").convert(),
    (1920, 1080)
)

idle_frames = [
    pygame.transform.scale(
        pygame.image.load(f"Figur/png/Idle ({i}).png").convert_alpha(),
        (600, 600)
    ) for i in range(1, 11)
]

# Lore-Text
lore_zeilen = [
    "Das Jahr 1892. Die Junge Dame –",
    "schnellste Pistolenschützin im Wilden Westen –",
    "hat ein Problem.",
    "",
    "Die Meisterschale ist verschwunden.",
    "",
    "Was die Alte Dame einst gewann,",
    "muss die Junge Dame nun wiederfinden.",
    "",
    "Denn ohne Schale... ist alles nichts.",
]


class Button:
    # Button mit einfachem Hover-Effekt

    def __init__(self, text, x, y, breite, hoehe):
        self.text = text
        self.rect = pygame.Rect(x, y, breite, hoehe)

    def zeichnen(self, screen):
        maus_pos = pygame.mouse.get_pos()
        farbe = hellbraun if self.rect.collidepoint(maus_pos) else braun
        pygame.draw.rect(screen, farbe, self.rect)
        pygame.draw.rect(screen, gold, self.rect, 2)  # gold Rahmen
        text_surface = button_font.render(self.text, True, weiss)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def wurde_geklickt(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


def hauptmenu():
    start_button   = Button("Spiel starten", 130, 620, 360, 60)
    beenden_button = Button("Beenden",       130, 700, 360, 60)

    # Animationsstand für Cowgirl
    frame_index = 0
    frame_timer = 0

    while True:

        # Hintergrund zeichnen (leicht abgedunkelt)
        screen.blit(hintergrund, (0, 0))
        dunkel = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        dunkel.fill((0, 0, 0, 140))
        screen.blit(dunkel, (0, 0))

        # --- Linke Seite ---

        # Titel
        titel = titel_font.render("Quest 1892", True, gold)
        screen.blit(titel, (130, 160))

        # Untertitel
        untertitel = untertitel_font.render("Die verlorene Meisterschale", True, weiss)
        screen.blit(untertitel, (130, 270))

        # Lore-Text
        lore_y = 330
        for zeile in lore_zeilen:
            if zeile == "":
                lore_y += 14
            else:
                text = lore_font.render(zeile, True, grau)
                screen.blit(text, (130, lore_y))
                lore_y += 30

        # Buttons
        start_button.zeichnen(screen)
        beenden_button.zeichnen(screen)

        # Steuerungshinweis
        hinweis = lore_font.render("A/D = Bewegen  |  Leertaste = Springen  |  Linksklick = Schießen", True, grau)
        screen.blit(hinweis, (130, 800))

        # --- Rechte Seite: animiertes Cowgirl ---

        # alle 7 Frames zum nächsten Animationsbild wechseln
        frame_timer += 1
        if frame_timer >= 7:
            frame_timer = 0
            frame_index = (frame_index + 1) % len(idle_frames)

        screen.blit(idle_frames[frame_index], (1200, 380))

        # Name unter der Figur
        name = untertitel_font.render("Die Junge Dame", True, gold)
        screen.blit(name, (1390 - name.get_width() // 2, 990))

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if start_button.wurde_geklickt(event):
                map.main(screen)

            if beenden_button.wurde_geklickt(event):
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    hauptmenu()