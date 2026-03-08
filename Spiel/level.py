import pygame
import sys
from Figur.spielfigur import Spielfigur, Gegner

# fenstergröße
breite = 1920
hoehe = 1080

# farben
schwarz = (0, 0, 0)
weiss = (255, 255, 255)
rot = (200, 50, 50)
gruen = (50, 200, 50)
grau = (100, 100, 100)

# boden-y-position (da wo die Figuren stehen)
boden_y = 780

class Plattform:
    # Plattform auf der Figur stehen kann
    def __init__(self, x, y, breite, hoehe, farbe=(80, 50, 20)):
        self.rect = pygame.Rect(x, y, breite, hoehe)
        self.farbe = farbe

    def zeichnen(self, screen):
        pygame.draw.rect(screen, self.farbe, self.rect)
        pygame.draw.rect(screen, schwarz, self.rect, 2)  # dünner Rahmen wie bei


# level-Daten - Hintergrund + Plattformen + gegner pro level
def level_daten_laden(level_nr):

    # zombie-Animationen
    zombie_lauf = [pygame.image.load(f"Spiel/Gegner/PNG/Zombie1/animation/Run{i}.png").convert_alpha() for i in range(1, 11)]

    # hintergründe
    hintergrund_pfade = {
        0: "Spiel/Hintergründe/2/background.png",
        1: "Spiel/Hintergründe/3/background.png",
        2: "Spiel/Hintergründe/4/background.png",
        3: "Spiel/Hintergründe/2/background.png",
        4: "Spiel/Hintergründe/3/background.png",
        5: "Spiel/Hintergründe/4/background.png",
        6: "Spiel/Hintergründe/2/background.png",
        7: "Spiel/Hintergründe/3/background.png",  # Boss
    }

    # plattformen: je nach Level andere Positionen
    # strukrut: Plattform(x, y, breite, hoehe)
    plattformen_pro_level = {
        0: [],  # Kampf 1 - keine Plattformen (auch nur ein gegner)
        1: [    # Kampf 2 - eine Plattform in der Mitte
            Plattform(700, 620, 300, 25),
        ],
        2: [    # Kampf 3
            Plattform(400, 600, 250, 25),
            Plattform(1100, 550, 250, 25),
        ],
        3: [    # Kampf 4 - (wie treppe)
            Plattform(300, 680, 200, 25),
            Plattform(700, 580, 200, 25),
            Plattform(1100, 480, 200, 25),
        ],
        4: [    # Kampf 5 - zwei Plattformen nebeneinander (hoch oben)
            Plattform(500, 500, 200, 25),
            Plattform(1000, 500, 200, 25),
        ],
        5: [    # Kampf 6 - eine breite Plattform
            Plattform(600, 550, 500, 25),
        ],
        6: [    # Kampf 7 - mehrere kleine Plattformen
            Plattform(250, 650, 150, 25),
            Plattform(600, 550, 150, 25),
            Plattform(950, 450, 150, 25),
            Plattform(1300, 550, 150, 25),
        ],
        7: [    # Boss: keine Plattformen, freie Fläche für Bosskampf
        ],
    }

    # Gegner pro Level werden stärker mit jedem Level
    gegner_pro_level = {
        0: [  # Kampf 1 - schwacher Gegner
            Gegner(None, "Nahkampf", 1200, boden_y - 200, 800, 1600, 200, 200,
                   [0, 1, 0, 0], 3, 2, laufAnimation=zombie_lauf),
        ],
        1: [  # Kampf 2 - zwei Gegner
            Gegner(None, "Nahkampf", 1000, boden_y - 200, 600, 1400, 200, 200,
                   [0, 1, 0, 0], 4, 4, laufAnimation=zombie_lauf),
            Gegner(None, "Nahkampf", 1500, boden_y - 200, 1000, 1800, 200, 200,
                   [1, 0, 0, 0], 4, 2, laufAnimation=zombie_lauf),
        ],
        2: [  # Kampf 3
            Gegner(None, "Nahkampf", 900, boden_y - 200, 500, 1400, 200, 200,
                   [0, 1, 0, 0], 5, 4, laufAnimation=zombie_lauf),
            Gegner(None, "Nahkampf", 1400, boden_y - 200, 900, 1800, 200, 200,
                   [1, 0, 0, 0], 5, 4, laufAnimation=zombie_lauf),
        ],
        3: [  # Kampf 4
            Gegner(None, "Nahkampf", 1100, boden_y - 200, 600, 1600, 200, 200,
                   [0, 1, 0, 0], 5, 6, laufAnimation=zombie_lauf),
        ],
        4: [  # Kampf 5
            Gegner(None, "Nahkampf", 800, boden_y - 200, 400, 1300, 200, 200,
                   [0, 1, 0, 0], 6, 4, laufAnimation=zombie_lauf),
            Gegner(None, "Nahkampf", 1400, boden_y - 200, 900, 1800, 200, 200,
                   [1, 0, 0, 0], 6, 4, laufAnimation=zombie_lauf),
        ],
        5: [  # Kampf 6
            Gegner(None, "Nahkampf", 900, boden_y - 200, 500, 1500, 200, 200,
                   [0, 1, 0, 0], 6, 6, laufAnimation=zombie_lauf),
            Gegner(None, "Nahkampf", 1500, boden_y - 200, 1000, 1800, 200, 200,
                   [1, 0, 0, 0], 6, 4, laufAnimation=zombie_lauf),
        ],
        6: [  # Kampf 7 - drei Gegner
            Gegner(None, "Nahkampf", 700, boden_y - 200, 300, 1200, 200, 200,
                   [0, 1, 0, 0], 7, 4, laufAnimation=zombie_lauf),
            Gegner(None, "Nahkampf", 1200, boden_y - 200, 800, 1600, 200, 200,
                   [1, 0, 0, 0], 7, 4, laufAnimation=zombie_lauf),
            Gegner(None, "Nahkampf", 1600, boden_y - 200, 1200, 1900, 200, 200,
                   [0, 1, 0, 0], 7, 4, laufAnimation=zombie_lauf),
        ],
        7: [  # Boss - sehr starker Gegner (bosskampf halt)
            Gegner(None, "Nahkampf", 1200, boden_y - 200, 500, 1700, 250, 250,
                   [1, 0, 0, 0], 5, 12, laufAnimation=zombie_lauf),
        ],
    }

    # hntergrundbild laden
    try:
        hintergrund = pygame.image.load(hintergrund_pfade[level_nr]).convert()
        hintergrund = pygame.transform.scale(hintergrund, (breite, hoehe))
    except:
        hintergrund = None 
        
    return hintergrund, plattformen_pro_level[level_nr], gegner_pro_level[level_nr]

def kampf_starten(screen, level_nr, ist_boss):

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 28, bold=True)

    # Level-Daten laden (Hintergrund, Plattformen, Gegner)
    hintergrund, plattformen, gegner_liste = level_daten_laden(level_nr)

    # Spielfigur erstellen – startet links auf dem Boden
    spieler = Spielfigur(screen, 100, boden_y - 200, 200, 200, [0, 1, 0, 0], 8)

    # Screen-Referenz an alle Gegner übergeben (wurde beim Erstellen noch nicht gesetzt)
    for g in gegner_liste:
        g.screen = screen

    # Boden-Rechteck für Kollision
    boden = pygame.Rect(0, boden_y, breite, hoehe - boden_y)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    spieler.startSprung()
                if event.key == pygame.K_ESCAPE:
                    return None  # zurück zur Map (ohne Ergebnis)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    spieler.schiessen()

        # tasten dauerhaft abfragen (für Bewegung links& rechts)
        tasten = pygame.key.get_pressed()
        links = tasten[pygame.K_a]
        rechts = tasten[pygame.K_d]

        if links or rechts:
            spieler.laufen([links, rechts])
        else:
            spieler.stehen()

        # --- Spieler-Updates ---
        spieler.updateSprung()
        spieler.kugelverhalten()

        # Spieler auf Boden halten
        if spieler.y >= boden_y - spieler.hoehe:
            spieler.y = boden_y - spieler.hoehe
            spieler.sprung = False
            spieler.sprungzahl = 13

        # Spieler auf Plattformen halten
        for p in plattformen:
            spieler_rect = pygame.Rect(spieler.x, spieler.y, spieler.breite, spieler.hoehe)
            if spieler_rect.colliderect(p.rect) and spieler.y + spieler.hoehe <= p.rect.y + 20:
                spieler.y = p.rect.y - spieler.hoehe
                spieler.sprung = False
                spieler.sprungzahl = 13

        # Spieler nicht aus dem Bildschirm laufen lassen
        spieler.x = max(0, min(breite - spieler.breite, spieler.x))

        # gegnerupdates
        for g in gegner_liste:
            if g.leben > 0:
                g.Bewegungsregler()
                g.bewegen()
                spieler.trefferCheck(g)   # prüft ob Kugeln Gegner treffen
                spieler.kollision(g)       # prüft ob Gegner Spieler berührt

        # zeichnen
        # Hintergrund
        if hintergrund:
            screen.blit(hintergrund, (0, 0))
        else:
            screen.fill((30, 30, 30))

        # Boden zeichnen
        pygame.draw.rect(screen, (60, 40, 10), boden)
        pygame.draw.line(screen, schwarz, (0, boden_y), (breite, boden_y), 3)

        # Plattformen zeichnen
        for p in plattformen:
            p.zeichnen(screen)

        # Kugeln zeichnen
        for k in spieler.kugeln:
            k.zeichnen()

        # Gegner zeichnen
        for g in gegner_liste:
            if g.leben > 0:
                g.gegnerImage()

        # Spieler zeichnen
        spieler.spielerImage()

        # HUD lever & hinweis
        level_text = font.render(f"Level {level_nr + 1}{'  –  BOSS!' if ist_boss else ''}", True, weiss)
        screen.blit(level_text, (20, 20))
        hinweis = pygame.font.SysFont("Arial", 18).render("ESC = zurück zur Map", True, grau)
        screen.blit(hinweis, (20, 60))

        # gewonnen - alle Gegner besiegt
        alle_tot = all(g.leben <= 0 for g in gegner_liste)
        if alle_tot:
            gewonnen_text = font.render("Level geschafft! Weiter...", True, gruen)
            screen.blit(gewonnen_text, (breite // 2 - gewonnen_text.get_width() // 2, hoehe // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            return True  # gewonnen - zurück zur map

        # verloren - spieler tot
        if not spieler.go:
            verloren_text = font.render("Du bist gestorben!", True, rot)
            screen.blit(verloren_text, (breite // 2 - verloren_text.get_width() // 2, hoehe // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            return False  # verloren - zurück zur map

        pygame.display.flip()
        clock.tick(60)

# if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.SCALED | pygame.FULLSCREEN)
    kampf_starten(screen, 0, False)