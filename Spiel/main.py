import pygame
import sys
import map  # map.py wird importiert

pygame.init()

# fenster 1920x1080 (vollbild)
screen = pygame.display.set_mode((1920, 1080), pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption("Schatzsuche in der verlassenen Stadt")
clock = pygame.time.Clock()

# farben
weiss = (255, 255, 255)
schwarz = (0, 0, 0)
braun = (139, 69, 19)
hellbraun = (205, 133, 63)

# schriftarten
titel_font = pygame.font.SysFont("arial", 48)
button_font = pygame.font.SysFont("arial", 32)


class Button:
    # einfacher Button mit Hover-Effekt

    def __init__(self, text, x, y, breite, hoehe):
        self.text = text
        self.rect = pygame.Rect(x, y, breite, hoehe)

    def zeichnen(self, screen):
        # Farbe wechseln wenn Maus über dem Button ist
        maus_pos = pygame.mouse.get_pos()
        farbe = hellbraun if self.rect.collidepoint(maus_pos) else braun
        pygame.draw.rect(screen, farbe, self.rect)
        pygame.draw.rect(screen, schwarz, self.rect, 2)
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
    # Buttons zentriert auf 1920x1080
    start_button   = Button("Spiel starten", 760, 480, 400, 70)
    beenden_button = Button("Beenden",        760, 580, 400, 70)

    while True:
        screen.fill((60, 60, 60))

        # Titel
        titel = titel_font.render("Schatzsuche", True, weiss)
        untertitel = titel_font.render("in der verlassenen Stadt", True, weiss)
        screen.blit(titel,     titel.get_rect(center=(960, 280)))
        screen.blit(untertitel, untertitel.get_rect(center=(960, 350)))

        # Buttons zeichnen
        start_button.zeichnen(screen)
        beenden_button.zeichnen(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if start_button.wurde_geklickt(event):
                map.main(screen)  # → Fortschritts-Map starten

            if beenden_button.wurde_geklickt(event):
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    hauptmenu()