import pygame
import sys
import math

# Fenstergröße
breite = 900
hoehe = 600

# Farben
weiss = (255, 255, 255)
schwarz = (0, 0, 0)
grau = (150, 150, 150)
dunkelgrau = (80, 80, 80)
gelb = (255, 215, 0)
gruen = (50, 200, 50)
rot = (200, 50, 50)
beige = (245, 222, 179)
hellblau = (173, 216, 230)


class Level:
    # Auf der Map wird einzelnes Level angezeigt

    radius = 35

    def __init__(self, daten):
        self.name = daten["name"]
        self.pos = daten["pos"]
        self.freigeschaltet = daten["freigeschaltet"]
        self.boss = daten["boss"]
        self.besucht = False

    def zeichnen(self, screen, font, ausgewaehlt):
        x, y = self.pos

        # Farbe je nach Status des Levels
        if self.boss:
            farbe = rot if self.freigeschaltet else dunkelgrau
        elif self.besucht:
            farbe = gruen
        elif self.freigeschaltet:
            farbe = hellblau
        else:
            farbe = dunkelgrau

        # Gelber Rahmen wenn Level gerade ausgewählt ist
        if ausgewaehlt:
            pygame.draw.circle(screen, gelb, (x, y), self.radius + 5)

        # Kreis und Umrandung zeichnen
        pygame.draw.circle(screen, farbe, (x, y), self.radius)
        pygame.draw.circle(screen, schwarz, (x, y), self.radius, 2)

        # Schloss anzeigen wenn gesperrt, sonst den Level-Namen
        if not self.freigeschaltet:
            schloss = font.render("🔒", True, weiss)
            screen.blit(schloss, (x - schloss.get_width() // 2, y - schloss.get_height() // 2))
        else:
            text = font.render(self.name, True, schwarz)
            screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

    def wird_geklickt(self, maus_pos):
        # Prüft ob der Mausklick innerhalb des Kreises liegt (Satz des Pythagoras)
        mx, my = maus_pos
        lx, ly = self.pos
        abstand = math.hypot(mx - lx, my - ly)
        return abstand <= self.radius


class Fortschrittsmap:
    # Die Übersichtskarte mit allen Leveln

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 14, bold=True)
        self.titel_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.info_font = pygame.font.SysFont("Arial", 18)
        self.ausgewaehlt = None

        # Level-Daten: Name, Position auf der Map, freigeschaltet?, Boss?
        level_daten = [
            {"name": "Kampf 1", "pos": (100, 300), "freigeschaltet": True,  "boss": False},
            {"name": "Kampf 2", "pos": (230, 300), "freigeschaltet": False, "boss": False},
            {"name": "Kampf 3", "pos": (360, 200), "freigeschaltet": False, "boss": False},
            {"name": "Kampf 4", "pos": (490, 150), "freigeschaltet": False, "boss": False},
            {"name": "Kampf 5", "pos": (490, 350), "freigeschaltet": False, "boss": False},
            {"name": "Kampf 6", "pos": (620, 200), "freigeschaltet": False, "boss": False},
            {"name": "Kampf 7", "pos": (620, 350), "freigeschaltet": False, "boss": False},
            {"name": "BOSS",    "pos": (760, 300), "freigeschaltet": False, "boss": True},
        ]

        # Verbindungen zwischen den Leveln (welche sind durch Linien verbunden?)
        self.verbindungen = [
            (0, 1),
            (1, 2),
            (1, 3),
            (1, 4),
            (2, 5),
            (3, 5),
            (4, 6),
            (5, 7),
            (6, 7),
        ]

        # Level-Objekte aus den Daten erstellen
        self.level_liste = [Level(d) for d in level_daten]

    def zeichnen(self):
        self.screen.fill(beige)

        # Titel oben in der Mitte
        titel = self.titel_font.render("⭐ Fortschritt-Map ⭐", True, schwarz)
        self.screen.blit(titel, (breite // 2 - titel.get_width() // 2, 20))

        # Verbindungslinien zwischen den Leveln zeichnen
        for (a, b) in self.verbindungen:
            pos_a = self.level_liste[a].pos
            pos_b = self.level_liste[b].pos
            farbe = gruen if self.level_liste[b].freigeschaltet else grau
            pygame.draw.line(self.screen, farbe, pos_a, pos_b, 3)

        # Alle Level zeichnen
        for i, level in enumerate(self.level_liste):
            level.zeichnen(self.screen, self.font, ausgewaehlt=(self.ausgewaehlt == i))

        # Info-Box am unteren Rand
        self.info_box_zeichnen()

    def info_box_zeichnen(self):
        # Dunkler Balken unten mit Infos zum ausgewählten Level
        pygame.draw.rect(self.screen, dunkelgrau, (0, hoehe - 80, breite, 80))

        if self.ausgewaehlt is not None:
            level = self.level_liste[self.ausgewaehlt]
            if level.freigeschaltet:
                text = f"▶  {level.name}  –  Klicke erneut zum Starten!"
                farbe = gelb
            else:
                text = f"🔒  {level.name}  –  Noch gesperrt. Besiege zuerst das vorherige Level!"
                farbe = grau
        else:
            text = "Klicke auf ein Level um es auszuwählen."
            farbe = weiss

        info = self.info_font.render(text, True, farbe)
        self.screen.blit(info, (20, hoehe - 50))

    def klick_verarbeiten(self, maus_pos):
        # Schaut welches Level geklickt wurde
        for i, level in enumerate(self.level_liste):
            if level.wird_geklickt(maus_pos):
                if self.ausgewaehlt == i and level.freigeschaltet:
                    # Zweiter Klick auf dasselbe Level → starten
                    return i
                else:
                    # Erstes Mal klicken → nur auswählen
                    self.ausgewaehlt = i
                    return None
        # Klick ins Leere → Auswahl aufheben
        self.ausgewaehlt = None
        return None

    def level_abschliessen(self, index):
        # Level als besucht markieren und verbundene Level freischalten
        self.level_liste[index].besucht = True
        for (a, b) in self.verbindungen:
            if a == index:
                self.level_liste[b].freigeschaltet = True


def kampf_starten(screen, level_name, ist_boss):
    # Platzhalter für den echten Kampf – hier kommt später euer Kampfsystem rein!
    font = pygame.font.SysFont("Arial", 32, bold=True)
    klein = pygame.font.SysFont("Arial", 20)
    clock = pygame.time.Clock()

    while True:
        screen.fill(schwarz)

        if ist_boss:
            titel = font.render("Bosskampf!", True, rot)
        else:
            titel = font.render(f"Kampf: {level_name}", True, weiss)

        hinweis = klein.render("W = Gewinnen  |  L = Verlieren   |   ESC = Zurück", True, grau)
        screen.blit(titel, (breite // 2 - titel.get_width() // 2, 220))
        screen.blit(hinweis, (breite // 2 - hinweis.get_width() // 2, 320))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    return True    # Gewonnen
                if event.key == pygame.K_e:
                    return False   # Verloren
                if event.key == pygame.K_ESCAPE:
                    return None    # Abgebrochen

        clock.tick(60)


def main():
    pygame.init()
    screen = pygame.display.set_mode((breite, hoehe))
    pygame.display.set_caption("Schatzsuche – Map")
    clock = pygame.time.Clock()

    karte = Fortschrittsmap(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                geklicktes_level = karte.klick_verarbeiten(event.pos)

                if geklicktes_level is not None:
                    level = karte.level_liste[geklicktes_level]
                    ergebnis = kampf_starten(screen, level.name, level.boss)

                    if ergebnis == True:
                        karte.level_abschliessen(geklicktes_level)
                        karte.ausgewaehlt = None

                        # Wenn der Boss besiegt wurde → Spiel gewonnen!
                        if level.boss:
                            screen.fill(schwarz)
                            font = pygame.font.SysFont("Arial", 48, bold=True)
                            txt = font.render("🏆  Du hast den Schatz gefunden!  🏆", True, gelb)
                            screen.blit(txt, (breite // 2 - txt.get_width() // 2, hoehe // 2 - 30))
                            pygame.display.flip()
                            pygame.time.wait(3000)

        karte.zeichnen()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()