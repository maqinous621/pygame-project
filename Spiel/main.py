import pygame
import sys
import map  # map.py importiert

pygame.init()

# fenster 1920x1080 (vollbild)
screen = pygame.display.set_mode((1920, 1080), pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption("Quest 1892 – Die verlorene Meisterschale")
clock = pygame.time.Clock()

# farben, von claude.ai
weiss = (255, 255, 255)
schwarz = (0, 0, 0)
braun = (139, 69, 19)
hellbraun = (205, 133, 63)
gold = (212, 175, 55)
grau = (180, 170, 150)

# schriftarten (name, größe & fett?)
titel_font = pygame.font.SysFont("arial", 72,bold=True)
untertitel_font = pygame.font.SysFont("arial",28)
button_font = pygame.font.SysFont("arial",34,bold=True)
lore_font = pygame.font.SysFont("arial", 21)

# hintergrund & auf 1920x1080 skalieren (mit diesem transform.scale), von claude.ai
hintergrund = pygame.transform.scale(
    pygame.image.load("Spiel/Hintergründe/2/background.png").convert(),
    (1920, 1080)
)
#idle animation - liste mit 10 frames, jedes auf 600x600 skaliert (wie hintergrund oben)
idle_frames = [ 
    pygame.transform.scale(
        pygame.image.load(f"Spiel/Figur/png/Idle ({i}).png").convert_alpha(),
        (600,600)
    ) for i in range(1,11)
]

#zeilenweise auf screen angezeigt, leere strings heißt quasi abstand
lore_text = [
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
    # einfacher button mit hover-Effekt

    def __init__(self, text, x, y, breite, hoehe):
        self.text = text
        self.rect = pygame.Rect(x, y, breite, hoehe)

    def zeichnen(self, screen):
        # Farbe wechseln wenn Maus über dem Button ist, bei claude nachgeschaut
        maus_pos = pygame.mouse.get_pos() #aktuelle mausposition (x,y)
        farbe = hellbraun if self.rect.collidepoint(maus_pos) else braun # prüft ob punkt im rechteck
        pygame.draw.rect(screen, farbe, self.rect)
        pygame.draw.rect(screen, gold, self.rect, 2) # goldener rahmen
        text_surface = button_font.render(self.text, True, weiss)
        text_rect = text_surface.get_rect(center=self.rect.center) # text in button-mitte zentrieren
        screen.blit(text_surface, text_rect)

    def wurde_geklickt(self, event):
        # gibt True wenn Button geklickt 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


def hauptmenu():
    start_button= Button("Spiel starten", 130, 620, 360, 60)
    beenden_button = Button("Beenden", 130, 700, 360, 60)

    frame_index = 0 # welches bild der animation wird gerade angezeigt (0-9), bei claude nachgeschaut
    frame_timer= 0  # zählt wie viele frames seit dem letzten bildwechsel vergangen sind
    while True:
        # hintergrund (leicht abgedunkelt)
        screen.blit(hintergrund, (0, 0))
        dunkel = pygame.Surface((1920, 1080), pygame.SRCALPHA) # SRCALPHA = transparenz, bei claude nachgeschaut
        dunkel.fill((0, 0, 0, 140)) # 4. Parameter 140, macht screen ca. 55% dunkel (halbtransparent, 140 von 255)
        screen.blit(dunkel, (0, 0))

        # Titel & untertitel
        titel = titel_font.render("Quest 1892", True, gold)
        screen.blit(titel, (130, 160))
        untertitel = untertitel_font.render("Die verlorene Meisterschale", True, weiss)
        screen.blit(untertitel, (130, 270))

        # lore-Text
        lore_y = 330
        for zeile in lore_text:
            if zeile == "":
                lore_y += 14 # leere zeile = kleiner abstand
            else:
                text = lore_font.render(zeile, True, grau)
                screen.blit(text, (130, lore_y))
                lore_y += 30 # nach jeder zeile 30px nach unten quasi

        # buttons
        start_button.zeichnen(screen)
        beenden_button.zeichnen(screen)
     
        # echte Seite - Cowgirl
        # alle 7 Frames zum nächsten animationsbild 
        frame_timer += 1
        if frame_timer >= 7:
            frame_timer = 0
            frame_index = (frame_index + 1) % len(idle_frames) # % len(...) = nach letzten bild wieder bei 0 anfangen, bei claude nachgeschaut

        screen.blit(idle_frames[frame_index], (1200, 380))

        # Name unter der Figur
        name = untertitel_font.render("Die Junge Dame", True, gold)
        screen.blit(name, (1360, 990))

        # events verarbeiten:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if start_button.wurde_geklickt(event):
                map.main(screen)  # map.py starten

            if beenden_button.wurde_geklickt(event):
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60) # spiel auf max. 60 fps begrenzen

if __name__ == "__main__":
    hauptmenu()