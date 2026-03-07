import pygame
import sys
import math
import level # level.py wird importiert

# Fenstergröße
breite = 1920
hoehe = 1080

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
    # einzelnes Level auf der map

    radius = 35

    def __init__(self, daten):
        self.name = daten["name"]
        self.pos = daten["pos"]
        self.freigeschaltet = daten["freigeschaltet"]
        self.boss = daten["boss"]
        self.besucht = False

    def zeichnen(self, screen, font, ausgewaehlt):
        x, y = self.pos

        # Farbe nach "Status" des Levels
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
        # Prüft ob der Mausklick innerhalb des Kreises liegt (Satz des Pythagoras, bei claude.ai nachgeschaut)
        mx, my = maus_pos
        lx, ly = self.pos
        abstand = math.hypot(mx - lx, my - ly)
        return abstand <= self.radius


class Fortschrittsmap:
    # Übersichtsmap

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 14, bold=True)
        self.titel_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.info_font = pygame.font.SysFont("Arial", 18)
        self.ausgewaehlt = None

        # level-Daten sollen sein: Name, Position auf der Map, freigeschaltet?, Boss?
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

        # verbindungen zwischen Leveln (welche sind durch Linien verbunden)
        self.verbindungen = [
            (0, 1),
            (1, 2), (1, 3), (1, 4),
            (2, 5), (3, 5),
            (4, 6),
            (5, 7), (6, 7),
        ]

        # level-Objekte aus den Daten erstellen
        self.level_liste = [Level(d) for d in level_daten]

    def zeichnen(self):
        self.screen.fill(beige)

        # titel oben in der Mitte
        titel = self.titel_font.render("Fortschritt-Map", True, schwarz)
        self.screen.blit(titel, (breite // 2 - titel.get_width() // 2, 20))

        # verbindungslinien zwischen Leveln
        for (a, b) in self.verbindungen:
            pos_a = self.level_liste[a].pos
            pos_b = self.level_liste[b].pos
            farbe = gruen if self.level_liste[b].freigeschaltet else grau
            pygame.draw.line(self.screen, farbe, pos_a, pos_b, 3)

        # alle Level zeichnen
        for i, level in enumerate(self.level_liste):
            level.zeichnen(self.screen, self.font, ausgewaehlt=(self.ausgewaehlt == i))

        # info-Box am unteren Rand
        self.info_box_zeichnen()

    def info_box_zeichnen(self):
        # dunkler Balken unten mit Infos zum ausgewählten Level
        pygame.draw.rect(self.screen, dunkelgrau, (0, hoehe - 100, breite, 100))

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
        self.screen.blit(info, (40, hoehe - 65))

    def klick_verarbeiten(self, maus_pos):
        # soll gucken welches Level geklickt wurde
        for i, level in enumerate(self.level_liste):
            if level.wird_geklickt(maus_pos):
                if self.ausgewaehlt == i and level.freigeschaltet:
                    # zweiter Klick auf selbe Level soll level starten
                    return i
                else:
                    # erstes Mal klicken soll nur auswählen
                    self.ausgewaehlt = i
                    return None
        # wenn man ins Leere klickt soll Auswahl aufgehoben werden
        self.ausgewaehlt = None
        return None

    def level_abschliessen(self, index):
        # level als "besucht" markieren & nächstes freischalten
        self.level_liste[index].besucht = True
        for (a, b) in self.verbindungen:
            if a == index:
                self.level_liste[b].freigeschaltet = True


def main(screen):
    # wird in main.py aufgerufen
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
                    lv = karte.level_liste[geklicktes_level]

                    # echten kampf aus level.py strarten
                    ergebnis = level.kampf_starten(screen, geklicktes_level, lv.boss)

                    if ergebnis == True:
                        karte.level_abschliessen(geklicktes_level)
                        karte.ausgewaehlt = None
                    
                        # wenn man boss besiegt dann hat man gewonnen
                        if lv.boss:
                            screen.fill(schwarz)
                            font = pygame.font.SysFont("Arial", 64, bold=True)
                            txt = font.render("Du hast den Schatz gefunden")
                            screen.blit(txt, (breite //2 - txt.get_width()// 2, hoehe // 2-40))
                            pygame.display.flip()
                            pygame.time.wait(4000)
                            return # zurück zu hauptmenü

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


