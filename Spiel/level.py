import pygame
import sys
from Figur.spielfigur import Spielfigur, Gegner

breite   = 1920
hoehe    = 1080
boden_y  = 690
gegner_y = boden_y - 30  # Zombie minimal höher damit er nicht unter den Boden geht

# Farben
schwarz = (0, 0, 0)
weiss   = (255, 255, 255)
rot     = (200, 50, 50)
grau    = (100, 100, 100)
gold    = (212, 175, 55)


class Plattform:

    def __init__(self, x, y, breite, hoehe, farbe=(80, 50, 20)):
        self.rect  = pygame.Rect(x, y, breite, hoehe)
        self.farbe = farbe

    def zeichnen(self, screen):
        pygame.draw.rect(screen, self.farbe, self.rect)
        pygame.draw.rect(screen, schwarz, self.rect, 2)


def kampf_starten(screen, level_nr, ist_boss):

    clock = pygame.time.Clock()
    font  = pygame.font.SysFont("georgia", 28, bold=True)
    klein = pygame.font.SysFont("georgia", 18)

    # Zombie-Animationen laden
    zombie_run  = [pygame.image.load(f"Spiel/Gegner/PNG/Zombie1/animation/Run{i}.png")  for i in range(1, 11)]
    zombie_dead = [pygame.image.load(f"Spiel/Gegner/PNG/Zombie1/animation/Dead{i}.png") for i in range(1, 9)]

    # Hintergrund je nach Level
    hintergrund_pfade = {
        0: "Spiel/Hintergründe/4/background.png",
        1: "Spiel/Hintergründe/4/background.png",
        2: "Spiel/Hintergründe/4/background.png",
        3: "Spiel/Hintergründe/4/background.png",
        4: "Spiel/Hintergründe/3/background.png",
    }
    hintergrund = pygame.transform.scale(
        pygame.image.load(hintergrund_pfade[level_nr]).convert(),
        (breite, hoehe)
    )

    # Plattformen je Level – niedrig genug damit man sie mit dem Sprung erreicht
    # Spieler bei boden_y=690, Sprung geht ca. 200px hoch → Plattform max bei ~500
    plattformen_pro_level = {
        0: [],
        1: [Plattform(700, 565, 400, 25)],
        2: [Plattform(400, 490, 250, 25), Plattform(1100, 450, 250, 25)],
        3: [Plattform(300, 560, 200, 25), Plattform(750, 470, 200, 25), Plattform(1200, 390, 200, 25)],
        4: [],
    }
    plattformen = plattformen_pro_level[level_nr]

    # Gegner je Level
    gegner_pro_level = {
        0: [
            Gegner(None, "Nahkampf", 1800, gegner_y, 100, 1850, 137, 290,
                   [1, 0, 0, 0], 3, 2, None, [], zombie_run, [], [], zombie_dead),
        ],
        1: [
            Gegner(None, "Nahkampf", 1200, gegner_y, 100, 1500, 137, 290,
                   [1, 0, 0, 0], 4, 4, None, [], zombie_run, [], [], zombie_dead),
            Gegner(None, "Nahkampf", 1700, gegner_y, 900, 1850, 137, 290,
                   [1, 0, 0, 0], 4, 2, None, [], zombie_run, [], [], zombie_dead),
        ],
        2: [
            Gegner(None, "Nahkampf", 900,  gegner_y, 100, 1300, 137, 290,
                   [0, 1, 0, 0], 5, 4, None, [], zombie_run, [], [], zombie_dead),
            Gegner(None, "Nahkampf", 1500, gegner_y, 800, 1850, 137, 290,
                   [1, 0, 0, 0], 5, 4, None, [], zombie_run, [], [], zombie_dead),
        ],
        3: [
            Gegner(None, "Nahkampf", 700,  gegner_y, 100,  1100, 137, 290,
                   [0, 1, 0, 0], 5, 4, None, [], zombie_run, [], [], zombie_dead),
            Gegner(None, "Nahkampf", 1200, gegner_y, 700,  1600, 137, 290,
                   [1, 0, 0, 0], 5, 4, None, [], zombie_run, [], [], zombie_dead),
            Gegner(None, "Nahkampf", 1700, gegner_y, 1200, 1850, 137, 290,
                   [1, 0, 0, 0], 5, 4, None, [], zombie_run, [], [], zombie_dead),
        ],
        4: [
            Gegner(None, "Nahkampf", 1500, gegner_y, 100, 1850, 200, 400,
                   [1, 0, 0, 0], 4, 12, None, [], zombie_run, [], [], zombie_dead),
        ],
    }
    gegner_liste = gegner_pro_level[level_nr]

    for g in gegner_liste:
        g.screen = screen

    spieler     = Spielfigur(screen, 200, boden_y, 320, 271, [0, 0, 1, 0], 10)
    linke_wand  = pygame.Rect(0,    0, 2, hoehe)
    rechte_wand = pygame.Rect(1918, 0, 2, hoehe)

    while True:

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None

        # Tasten
        tasten = pygame.key.get_pressed()

        if tasten[pygame.K_a] and not spieler.hitbox.colliderect(linke_wand) and not spieler.dead:
            spieler.laufen([1, 0])
        elif tasten[pygame.K_d] and not spieler.hitbox.colliderect(rechte_wand) and not spieler.dead:
            spieler.laufen([0, 1])
        else:
            spieler.stehen()

        if tasten[pygame.K_SPACE] and not spieler.sprung and not spieler.dead:
            spieler.startSprung()
        spieler.updateSprung()
        print(spieler.y, spieler.sprung, spieler.sprungzahl, spieler.go, spieler.dead)

        if tasten[pygame.K_f] and len(spieler.kugeln) <= 2:
            spieler.schiessen()
            spieler.ok = False
        if not tasten[pygame.K_f]:
            spieler.ok = True

        spieler.kugelverhalten()

        # Spieler auf Boden halten
        auf_plattform = False
        if spieler.y >= boden_y:
            spieler.y= boden_y
            spieler.sprung= False
            spieler.sprungzahl = 13
        else:
            for p in plattformen:
                spieler_rect = pygame.Rect(spieler.x + 80, spieler.y, spieler.breite - 160, spieler.hoehe)
                fuesse = spieler.y + spieler.hoehe
                # X-Überlappung prüfen UND von oben kommen
            if (spieler_rect.right > p.rect.left and spieler_rect.left < p.rect.right
                    and fuesse >= p.rect.top and fuesse <= p.rect.bottom + 10
                    and spieler.sprungzahl <= 0):  # nur wenn Spieler fällt (sprungzahl negativ)
                spieler.y          = p.rect.y - spieler.hoehe
                spieler.sprung     = False
                spieler.sprungzahl = 13
                auf_plattform      = True
                break
            if not auf_plattform and not spieler.sprung:
                spieler.y += 8

        # Zeichnen
        screen.blit(hintergrund, (0, 0))

        for p in plattformen:
            p.zeichnen(screen)

        for k in spieler.kugeln:
            k.zeichnen()

        # erst zeichnen → hitbox wird in gegnerImage() aktualisiert
        for g in gegner_liste:
            if g.go:
                g.gegnerImage()

        spieler.spielerImage()

        # dann Treffer prüfen – hitbox stimmt jetzt
        for g in gegner_liste:
            if g.go and not g.dead:
                g.Bewegungsregler()
                g.bewegen(spieler)
                spieler.trefferCheck(g)

        level_text = font.render(f"Level {level_nr + 1}{'  –  BOSS!' if ist_boss else ''}", True, weiss)
        screen.blit(level_text, (20, 20))
        hinweis = klein.render("ESC = zurück zur Map  |  F = Schießen  |  Leertaste = Springen", True, grau)
        screen.blit(hinweis, (20, 60))

        # Gewonnen?
        if all(not g.go for g in gegner_liste):
            gewonnen_text = font.render("Level geschafft!", True, gold)
            screen.blit(gewonnen_text, (breite // 2 - gewonnen_text.get_width() // 2, hoehe // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            return True

        # Verloren?
        if not spieler.go:
            verloren_text = font.render("Du bist gestorben!", True, rot)
            screen.blit(verloren_text, (breite // 2 - verloren_text.get_width() // 2, hoehe // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            return False

        pygame.display.flip()
        clock.tick(60)