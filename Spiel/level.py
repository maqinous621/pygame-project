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
gold = (212, 175, 55)

# boden-y-position (da wo die Figuren stehen)
boden_y = 690

class Plattform:
    # Plattform auf der Figur stehen kann
    def __init__(self, x, y, breite, hoehe, farbe=(80, 50, 20)):
        self.rect = pygame.Rect(x, y, breite, hoehe)
        self.farbe = farbe

    def zeichnen(self, screen):
        pygame.draw.rect(screen, self.farbe, self.rect)
        pygame.draw.rect(screen, schwarz, self.rect, 2)  # dünner Rahmen wie bei buttons auch


# level-Daten - hintergrund, Plattformen, gegner pro level, von claude 
def level_daten_laden(level_nr):

    # zombie-Animationen
    zombie_run  = [pygame.image.load(f"Spiel/Gegner/PNG/Zombie1/animation/Run{i}.png")  for i in range(1, 11)]
    zombie_dead = [pygame.image.load(f"Spiel/Gegner/PNG/Zombie1/animation/Dead{i}.png") for i in range(1, 9)]
    # hintergründe
    hintergrund_pfade = {
        0: "Spiel/Hintergründe/4/background.png",
        1: "Spiel/Hintergründe/4/background.png",
        2: "Spiel/Hintergründe/4/background.png",
        3: "Spiel/Hintergründe/4/background.png",
        4: "Spiel/Hintergründe/3/background.png",  # Boss
    }

    # plattformen je nach Level
    # strukrut: Plattform(x, y, breite, hoehe)
    plattformen_pro_level = {
        0: [],  # Kampf 1 - keine Plattformen (auch nur ein gegner)
        1: [    # Kampf 2 - eine Plattform in der Mitte
            Plattform(700, 550, 400, 25),
        ],
        2: [    # Kampf 3 zwei pattformen
            Plattform(400, 520, 250, 25),
            Plattform(1100, 480, 250, 25),
        ],
        3: [    # Kampf 4 - (wie treppe)
            Plattform(300, 620, 200, 25),
            Plattform(750, 520, 200, 25),
            Plattform(1200, 420, 200, 25),
        ],
        4: [],    # Boss: keine Plattformen, freie Fläche
    }

    gegner_pro_level = {
        0: [  # Kampf 1 - schwacher Zombie
            Gegner(None, "Nahkampf", 1800, boden_y - 30, 100, 1850, 137, 290,
                   [1, 0, 0, 0], 3, 2,
                   laufAnimation=zombie_run, totAnimation=zombie_dead),
        ],
        1: [  # Kampf 2: zwei Zombies
            Gegner(None, "Nahkampf", 1200, boden_y, 100, 1500, 137, 290,
                   [1, 0, 0, 0], 4, 4,
                   laufAnimation=zombie_run, totAnimation=zombie_dead),
            Gegner(None, "Nahkampf", 1700, boden_y, 900, 1850, 137, 290,
                   [1, 0, 0, 0], 4, 2,
                   laufAnimation=zombie_run, totAnimation=zombie_dead),
        ],
        2: [  # Kampf 3: zwei stärkere Zombies
            Gegner(None, "Nahkampf", 1200, boden_y, 100, 1500, 137, 290,
                   [1, 0, 0, 0], 4, 4,
                   laufAnimation=zombie_run, totAnimation=zombie_dead),
            Gegner(None, "Nahkampf", 1700, boden_y, 900, 1850, 137, 290,
                   [1, 0, 0, 0], 4, 2,
                   laufAnimation=zombie_run, totAnimation=zombie_dead),
        ],
        3: [  # Kampf 4: drei Zombies
            Gegner(None, "Nahkampf", 700, boden_y, 100, 1100, 137, 290,
                   [0, 1, 0, 0], 5, 4,
                   laufAnimation=zombie_run, totAnimation=zombie_dead),
            Gegner(None, "Nahkampf", 1200, boden_y, 700, 1600, 137, 290,
                   [1, 0, 0, 0], 5, 4,
                   laufAnimation=zombie_run, totAnimation=zombie_dead),
            Gegner(None, "Nahkampf", 1700, boden_y, 1200, 1850, 137, 290,
                   [1, 0, 0, 0], 5, 4,
                   laufAnimation=zombie_run, totAnimation=zombie_dead),
        ],
        4: [  # Boss: ein sehr starker Zombie
            Gegner(None, "Nahkampf", 1500, boden_y, 100, 1850, 200, 400,
                   [1, 0, 0, 0], 4, 12,
                   laufAnimation=zombie_run, totAnimation=zombie_dead),
        ],
    }

    # hntergrundbild laden & skalieren
    hintergrund = pygame.transform.scale(
        pygame.image.load(hintergrund_pfade[level_nr]).convert(),
        (breite, hoehe)
    )
        
    return hintergrund, plattformen_pro_level[level_nr], gegner_pro_level[level_nr]

def kampf_starten(screen, level_nr, ist_boss):
    # wird bei der map.py aufgerufen

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 28, bold=True)
    klein = pygame.font.SysFont("Arial", 18)

    # Level-Daten laden (Hintergrund, Plattformen, Gegner)
    hintergrund, plattformen, gegner_liste = level_daten_laden(level_nr)

    # Spielfigur erstellen – startet links auf dem Boden
    spieler = Spielfigur(screen, 200, boden_y, 320, 271, [0,0,1,0], 10)

    linke_wand = pygame.Rect(0,0,2,hoehe)
    rechte_wand = pygame.Rect(1918,0,2,hoehe)

    # screen-Referenz an alle Gegner übergeben
    for g in gegner_liste:
        g.screen = screen

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

        # Bewegen mit Wandkollision (wie in test.py)
        if tasten[pygame.K_a] and not spieler.hitbox.colliderect(linke_wand) and not spieler.dead:
            spieler.laufen([1, 0])
        elif tasten[pygame.K_d] and not spieler.hitbox.colliderect(rechte_wand) and not spieler.dead:
            spieler.laufen([0, 1])
        else:
            spieler.stehen()
        # springen
        if tasten[pygame.K_SPACE] and not spieler.sprung and not spieler.dead:
            spieler.startSprung()
        spieler.updateSprung()

        #schießen mit F-Taste (wie in test.py auch)
        if tasten[pygame.K_f]:
            if len(spieler.kugeln) <= 2:
                spieler.schiessen()
                spieler.ok = False
        if not tasten[pygame.K_f]:
            spieler.ok = True

        spieler.kugelverhalten()

        # Spieler auf boden halten
        if spieler.y >= boden_y:
            spieler.y = boden_y
            spieler.sprung = False
            spieler.sprungzahl = 13

        # spieler auf plattformen halten
        for p in plattformen:
            spieler_rect = pygame.Rect(spieler.x, spieler.y, spieler.breite, spieler.hoehe)
            # nur von oben landen – Spieler muss von oben kommen (vorherige Y-Position über Plattform)
            if spieler_rect.colliderect(p.rect) and spieler.sprungzahl <= 0:
                spieler.y = p.rect.y - spieler.hoehe
                spieler.sprung = False
                spieler.sprungzahl = 13

        # gegner updates
        for g in gegner_liste:
            if g.go:
                if not g.dead:
                    g.Bewegungsregler()
                    g.bewegen()
                    spieler.trefferCheck(g)

        #zeichnen
        screen.blit(hintergrund, (0, 0))

        # Plattformen zeichnen
        for p in plattformen:
            p.zeichnen(screen)

        # Kugeln zeichnen
        for k in spieler.kugeln:
            k.zeichnen()

        # gegner gezeichnet
        for g in gegner_liste:
            if g.go:
                g.gegnerImage()

        # spieler gezeichnet
        spieler.spielerImage()

        # gewonnen - alle Gegner besiegt
        alle_tot = all(not g.go for g in gegner_liste)
        if alle_tot:
            gewonnen_text = font.render("Level geschafft! Weiter...", True, gold)
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