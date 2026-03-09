import pygame
import sys
import map  # map.py wird importiert

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

# schriftarten
titel_font = pygame.font.SysFont("arial", 82,bold=True)
untertitel_font = pygame.font.SysFont("arial",28)
button_font = pygame.font.SysFont("arial",34,bold=True)
lore_font = pygame.font.SysFont("arial", 21)

# Bilder
hintergrund = pygame.transform.scale(
    pygame.image.load("Spiel/Hintergründe/2/background.png").convert(),
    (1920, 1080)
)
    
idle_frames = [ 
    pygame.transform.scale(
        pygame.image.load(f"Spiel/Figur/png/Idle ({i}).png").convert_alpha(),
        (600,600)
    ) for i in range(1,11)
]

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
        # farbe soll gewechselt werden wenn Maus üer button
        maus_pos = pygame.mouse.get_pos()
        farbe = hellbraun if self.rect.collidepoint(maus_pos) else braun
        pygame.draw.rect(screen, farbe, self.rect)
        pygame.draw.rect(screen, gold, self.rect, 2) # goldener rahmen
        text_surface = button_font.render(self.text, True, weiss)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def wurde_geklickt(self, event):
        # gibt True wenn Button geklickt (von claude nachgeguckt)
        if event.type == pygame.MOUSEBUTTONDOWN: # war es ein mausclick?
            if self.rect.collidepoint(event.pos): # war die maus auf dem button?
                return True
        return False


def hauptmenu():
    start_button= Button("Spiel starten", 130, 620, 360, 60)
    beenden_button = Button("Beenden", 130, 700, 360, 60)

    frame_index = 0
    frame_timer= 0
    while True:
        # hintergrund (leicht abgedunkelt)
        screen.blit(hintergrund, (0, 0))
        dunkel = pygame.Surface((1920, 1080), pygame.SRCALPHA)
        dunkel.fill((0,0,0,140)) # vierter wert ist 140, also so halbtransparent (SRCALPHA)
        screen.blit(dunkel, (0, 0))

        # Titel
        titel = titel_font.render("Quest 1892", True, gold)
        screen.blit(titel, (130, 160))

        #  untertitel
        untertitel = untertitel_font.render("Die verlorene Meisterschale", True, weiss)
        screen.blit(untertitel, (130, 270))

        # lore-Text
        lore_y = 330
        for zeile in lore_text:
            if zeile == "":
                lore_y += 14
            else:
                text = lore_font.render(zeile, True, grau)
                screen.blit(text, (130, lore_y))
                lore_y += 30

        # buttons
        start_button.zeichnen(screen)
        beenden_button.zeichnen(screen)
     
        # echts - Cowgirl
        # alle 7 Frames zum nächsten animationsbild 
        frame_timer += 1
        if frame_timer >= 7:
            frame_timer = 0
            frame_index = (frame_index + 1) % len(idle_frames)

        screen.blit(idle_frames[frame_index], (1200, 380))

        # Name unter der Figur
        name = untertitel_font.render("Die Junge Dame", True, gold)
        screen.blit(name, (1360, 990))

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
        clock.tick(60)

if __name__ == "__main__":
    hauptmenu()