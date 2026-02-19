import pygame
import sys

pygame.init()

# --- Fenster ---
breite, hoehe = 800, 600
screen = pygame.display.set_mode((breite, hoehe))
pygame.display.set_caption("Schatzsuche in der verlassenen Stadt")
clock = pygame.time.Clock()

# --- Farben ---
weiss = (255, 255, 255)
schwarz = (0, 0, 0)
braun = (139, 69, 19)
hellbraun = (205, 133, 63)

# --- Schriftarten ---
titel_font = pygame.font.SysFont("arial", 48)
button_font = pygame.font.SysFont("arial", 32)


class Button:
    # Ein einfacher Button mit Hover-Effekt (Farbe ändert sich wenn Maus drüber ist)

    def __init__(self, text, x, y, breite, hoehe):
        self.text = text
        self.rect = pygame.Rect(x, y, breite, hoehe)

    def zeichnen(self, screen):
        # Farbe wechseln wenn Maus über dem Button ist
        maus_pos = pygame.mouse.get_pos()
        farbe = hellbraun if self.rect.collidepoint(maus_pos) else braun

        # Button-Rechteck und Rahmen zeichnen
        pygame.draw.rect(screen, farbe, self.rect)
        pygame.draw.rect(screen, schwarz, self.rect, 2)

        # Text zentriert auf dem Button anzeigen
        text_surface = button_font.render(self.text, True, weiss)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def wurde_geklickt(self, event):
        # Gibt True zurück wenn der Button angeklickt wurde
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


def hauptmenu():
    start_button = Button("Spiel starten", 300, 250, 200, 50)
    beenden_button = Button("Beenden", 300, 320, 200, 50)

    while True:
        # Hintergrund
        screen.fill((60, 60, 60))

        # Titel anzeigen
        titel = titel_font.render("Schatzsuche", True, weiss)
        screen.blit(titel, titel.get_rect(center=(breite // 2, 120)))

        # Buttons zeichnen
        start_button.zeichnen(screen)
        beenden_button.zeichnen(screen)

        # Events verarbeiten
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if start_button.wurde_geklickt(event):
                print("Spiel starten!")  # Hier später zur Fortschritts-Map wechseln

            if beenden_button.wurde_geklickt(event):
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    hauptmenu()
