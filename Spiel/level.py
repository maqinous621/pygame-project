import pygame
import sys
from Figur.spielfigur import Spielfigur
from Gegner.gegner import Gegner

breite   = 1920
hoehe    = 1080

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

    boden_pro_level = {
        0: 690,
        1: 690,
        2: 690,
        3: 690,
        4: 740,
    }
    aktueller_boden = boden_pro_level[level_nr]


    # Zombie-Animationen laden
    zombie1_walk  = [pygame.image.load(f"Spiel/Gegner/PNG/Zombie1/animation/Walk{i}.png")  for i in range(1, 7)]
    zombie1_dead = [pygame.image.load(f"Spiel/Gegner/PNG/Zombie1/animation/Dead{i}.png") for i in range(1, 9)]
    zombie1_hurt = [pygame.image.load(f"Spiel/Gegner/PNG/Zombie1/animation/Hurt{i}.png") for i in range(1, 6)]
    zombie2_walk  = [pygame.image.load(f"Spiel/Gegner/PNG/Zombie2/animation/Walk{i}.png")  for i in range(1, 7)]
    zombie2_dead = [pygame.image.load(f"Spiel/Gegner/PNG/Zombie2/animation/Dead{i}.png") for i in range(1, 9)]
    zombie2_hurt = [pygame.image.load(f"Spiel/Gegner/PNG/Zombie2/animation/Hurt{i}.png") for i in range(1, 6)]

    # Demon-Animationen laden
    demon_flying = [pygame.image.load(f"Spiel/Gegner/PNG/Demon/Sprites/without_outline/Flying{i}.png") for i in range(1, 5)]
    demon_death = [pygame.image.load(f"Spiel/Gegner/PNG/Demon/Sprites/without_outline/DEATH{i}.png") for i in range(1, 8)]
    demon_hurt = [pygame.image.load(f"Spiel/Gegner/PNG/Demon/Sprites/without_outline/Hurt{i}.png") for i in range(1, 5)]
    demon_attack = [pygame.image.load(f"Spiel/Gegner/PNG/Demon/Sprites/without_outline/Attack{i}.png") for i in range(1, 9)]
    demon_projectile = pygame.image.load("Spiel/Gegner/PNG/Demon/Sprites/projectile.png")

    # Wraith-Animationen laden
    wraith3_feuerball = "Spiel/Gegner/PNG/Wraith3/PNG Sequences/Feuerball.png"
    wraith3_stand = [pygame.image.load(f"Spiel/Gegner/PNG/Wraith3/PNG Sequences/Idle/Wraith_03_Idle_{i:03d}.png") for i in range(0, 12)]
    wraith3_cast = [pygame.image.load(f"Spiel/Gegner/PNG/Wraith3/PNG Sequences/Casting Spells/Wraith_03_Casting Spells_{i:03d}.png") for i in range(0, 18)]
    wraith3_hurt = [pygame.image.load(f"Spiel/Gegner/PNG/Wraith3/PNG Sequences/Hurt/Wraith_03_Hurt_{i:03d}.png") for i in range(0, 12)]
    wraith3_dying = [pygame.image.load(f"Spiel/Gegner/PNG/Wraith3/PNG Sequences/Dying/Wraith_03_Dying_{i:03d}.png") for i in range(0, 15)]

    wraith1_feuerball = "Spiel/Gegner/PNG/Wraith1/PNG Sequences/FeuerballBlau.png"
    wraith1_stand = [pygame.image.load(f"Spiel/Gegner/PNG/Wraith1/PNG Sequences/Idle/Wraith_01_Idle_{i:03d}.png") for i in range(0, 12)]
    wraith1_cast = [pygame.image.load(f"Spiel/Gegner/PNG/Wraith1/PNG Sequences/Casting Spells/Wraith_01_Casting Spells_{i:03d}.png") for i in range(0, 18)]
    wraith1_hurt = [pygame.image.load(f"Spiel/Gegner/PNG/Wraith1/PNG Sequences/Hurt/Wraith_01_Hurt_{i:03d}.png") for i in range(0, 12)]
    wraith1_dying = [pygame.image.load(f"Spiel/Gegner/PNG/Wraith1/PNG Sequences/Dying/Wraith_01_Dying_{i:03d}.png") for i in range(0, 15)]

    wraith2_feuerball = "Spiel/Gegner/PNG/Wraith2/PNG Sequences/FeuerballOrange.png"
    wraith2_stand = [pygame.image.load(f"Spiel/Gegner/PNG/Wraith2/PNG Sequences/Idle/Wraith_02_Idle_{i:03d}.png") for i in range(0, 12)]
    wraith2_cast = [pygame.image.load(f"Spiel/Gegner/PNG/Wraith2/PNG Sequences/Casting Spells/Wraith_02_Casting Spells_{i:03d}.png") for i in range(0, 18)]
    wraith2_hurt = [pygame.image.load(f"Spiel/Gegner/PNG/Wraith2/PNG Sequences/Hurt/Wraith_02_Hurt_{i:03d}.png") for i in range(0, 12)]
    wraith2_dying = [pygame.image.load(f"Spiel/Gegner/PNG/Wraith2/PNG Sequences/Dying/Wraith_02_Dying_{i:03d}.png") for i in range(0, 15)]

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
            Gegner(None, "Nahkampf", 1800, 690, 100, 1850, 137, 290,
                   [1, 0, 0, 0], 3, 6, laufAnimation=zombie1_walk, totAnimation=zombie1_dead, trefferAnimation=zombie1_hurt),
        ],
        1: [
            Gegner(None, "Nahkampf", 1200, 690, 100, 1500, 137, 290,
                   [1, 0, 0, 0], 4, 6, laufAnimation=zombie1_walk, totAnimation=zombie1_dead, trefferAnimation=zombie1_hurt),
            Gegner(None, "Nahkampf", 1700, 690, 900, 1850, 137, 290,
                   [1, 0, 0, 0], 4, 6, laufAnimation=zombie2_walk, totAnimation=zombie2_dead, trefferAnimation=zombie2_hurt),
        ],
        2: [
            Gegner(None, "Nahkampf", 900, 690, 100, 1300, 137, 290,
                   [0, 1, 0, 0], 5, 6, laufAnimation=zombie1_walk, totAnimation=zombie1_dead, trefferAnimation=zombie1_hurt),
            Gegner(None, "Fernkampf", 1700, 690, 800, 1850, 260, 210,
                   [1, 0, 0, 0], 5, 6, projektil=wraith3_feuerball,standAnimation=wraith3_stand, angriffAnimation=wraith3_cast, totAnimation=wraith3_dying, trefferAnimation=wraith3_hurt),
        ],
        3: [
            Gegner(None, "Nahkampf", 700,  690, 100,  1100, 137, 290,
                   [0, 1, 0, 0], 5, 6, laufAnimation=zombie1_walk, totAnimation=zombie1_dead, trefferAnimation=zombie1_hurt),
            Gegner(None, "Nahkampf", 1200, 690, 700,  1600, 137, 290,
                   [1, 0, 0, 0], 5, 6, laufAnimation=zombie2_walk, totAnimation=zombie2_dead, trefferAnimation=zombie2_hurt),
            Gegner(None, "Fliegend", 1700, 300, 100, 1850, 237, 207, [1, 0, 0, 0], 3, 6, projektil="Spiel/Gegner/PNG/Demon/Sprites/projectile.png", angriffAnimation=demon_attack, FlugAnimation=demon_flying, totAnimation=demon_death, trefferAnimation=demon_hurt),
        ],
        4: [
            Gegner(None, "Nahkampf", 1200, 690, 300,  1400, 137, 290,
                   [1, 0, 0, 0], 5, 6, laufAnimation=zombie2_walk, totAnimation=zombie2_dead, trefferAnimation=zombie2_hurt),
            Gegner(None, "Fernkampf", 1700, 400, 800, 1800, 260, 210,
                   [1, 0, 0, 0], 5, 6, projektil=wraith1_feuerball,standAnimation=wraith1_stand, angriffAnimation=wraith1_cast, totAnimation=wraith1_dying, trefferAnimation=wraith1_hurt),
            Gegner(None, "Fernkampf", 1700, 750, 400, 1850, 260, 210,
                   [1, 0, 0, 0], 5, 6, projektil=wraith2_feuerball,standAnimation=wraith2_stand, angriffAnimation=wraith2_cast, totAnimation=wraith2_dying, trefferAnimation=wraith2_hurt)
        ],
    }
    gegner_liste = gegner_pro_level[level_nr]

    for g in gegner_liste:
        g.screen = screen

    spieler     = Spielfigur(screen, 200, aktueller_boden, 320, 271, [0, 0, 1, 0], 10)
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
        if not spieler.sprung and spieler.y < aktueller_boden and not steht_auf_plattform:
            spieler.sprung     = True
            spieler.sprungzahl = 0

        # Boden
        if spieler.y >= aktueller_boden:
            spieler.y           = aktueller_boden
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

        pygame.draw.rect(screen, (255,0,0), g.hitbox, 5)
        pygame.draw.rect(screen, (0,255,0), g.kopf, 5)
        pygame.draw.rect(screen, (0,0,0), spieler.hitbox, 5)    

        spieler.spielerImage()

        for g in gegner_liste:
            if g.go and not g.dead:
                g.Bewegungsregler()
                g.bewegen(spieler)
                spieler.trefferCheck(g)
                g.kugelverhalten(spieler)

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