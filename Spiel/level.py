import pygame
import sys
from Figur.spielfigur import Spielfigur, Gegner

breite   = 1920
hoehe    = 1080
boden_y  = 690
gegner_y = boden_y - 30

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

    zombie_run  = [pygame.image.load(f"Spiel/Gegner/PNG/Zombie1/animation/Run{i}.png")  for i in range(1, 11)]
    zombie_dead = [pygame.image.load(f"Spiel/Gegner/PNG/Zombie1/animation/Dead{i}.png") for i in range(1, 9)]

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

    plattformen_pro_level = {
        0: [],
        1: [Plattform(700, 550, 400, 25)],
        2: [Plattform(400, 550, 250, 25), Plattform(1100, 550, 250, 25)],
        3: [Plattform(300, 560, 200, 25), Plattform(750, 470, 200, 25), Plattform(1200, 390, 200, 25)],
        4: [],
    }
    plattformen = plattformen_pro_level[level_nr]

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

    steht_auf_plattform = False  # merkt ob Spieler auf Plattform steht

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None

        tasten = pygame.key.get_pressed()

        if tasten[pygame.K_a] and not spieler.hitbox.colliderect(linke_wand) and not spieler.dead:
            spieler.laufen([1, 0])
        elif tasten[pygame.K_d] and not spieler.hitbox.colliderect(rechte_wand) and not spieler.dead:
            spieler.laufen([0, 1])
        else:
            spieler.stehen()

        if tasten[pygame.K_SPACE] and not spieler.sprung and not spieler.dead:
            spieler.startSprung()
            steht_auf_plattform = False

        if tasten[pygame.K_f] and len(spieler.kugeln) <= 2:
            spieler.schiessen()
            spieler.ok = False
        if not tasten[pygame.K_f]:
            spieler.ok = True

        spieler.kugelverhalten()

        # Sprung-Update und Fallrichtung merken
        vorheriges_y = spieler.y
        spieler.updateSprung()
        faellt = spieler.y > vorheriges_y

        # wenn sprung=False aber Spieler nicht auf Boden und nicht auf Plattform → fallen
        if not spieler.sprung and spieler.y < boden_y and not steht_auf_plattform:
            spieler.sprung     = True
            spieler.sprungzahl = 0

        # Boden
        if spieler.y >= boden_y:
            spieler.y           = boden_y
            spieler.sprung      = False
            spieler.sprungzahl  = 13
            steht_auf_plattform = False

        # Plattformen
        else:
            noch_drauf = False
            for p in plattformen:
                spieler_mitte_x = spieler.x + spieler.breite // 2
                fuesse          = spieler.y + spieler.hoehe
                ueber_plattform = p.rect.left < spieler_mitte_x < p.rect.right

                # landen wenn Spieler fällt und Füße die Plattform kreuzen
                if faellt and ueber_plattform and p.rect.top <= fuesse <= p.rect.bottom + 20:
                    spieler.y           = p.rect.y - spieler.hoehe
                    spieler.sprung      = False
                    spieler.sprungzahl  = 13
                    steht_auf_plattform = True
                    noch_drauf          = True
                    break

                # bereits drauf – prüfen ob Spieler noch horizontal über der Plattform ist
                if steht_auf_plattform and ueber_plattform:
                    noch_drauf = True
                    break

            # seitlich runtergelaufen → fallen lassen
            if steht_auf_plattform and not noch_drauf:
                steht_auf_plattform = False
                spieler.sprung      = True
                spieler.sprungzahl  = 0

        # Zeichnen
        screen.blit(hintergrund, (0, 0))

        for p in plattformen:
            p.zeichnen(screen)

        for k in spieler.kugeln:
            k.zeichnen()

        for g in gegner_liste:
            if g.go:
                g.gegnerImage()

        spieler.spielerImage()

        for g in gegner_liste:
            if g.go and not g.dead:
                g.Bewegungsregler()
                g.bewegen(spieler)
                spieler.trefferCheck(g)

        level_text = font.render(f"Level {level_nr + 1}{'  –  BOSS!' if ist_boss else ''}", True, weiss)
        screen.blit(level_text, (20, 20))
        hinweis = klein.render("ESC = zurück zur Map  |  F = Schießen  |  Leertaste = Springen", True, grau)
        screen.blit(hinweis, (20, 60))

        if all(not g.go for g in gegner_liste):
            gewonnen_text = font.render("Level geschafft!", True, gold)
            screen.blit(gewonnen_text, (breite // 2 - gewonnen_text.get_width() // 2, hoehe // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            return True

        if not spieler.go:
            verloren_text = font.render("Du bist gestorben!", True, rot)
            screen.blit(verloren_text, (breite // 2 - verloren_text.get_width() // 2, hoehe // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            return False

        pygame.display.flip()
        clock.tick(60)