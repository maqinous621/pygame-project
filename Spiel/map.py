import pygame
import sys
import math
import level # level.py wird importiert

pygame.init()
# fenstergröße
breite = 1920
hoehe = 1080

# farben
weiss = (255, 255, 255)
schwarz = (0, 0, 0)
grau = (150, 150, 150)
dunkelgrau = (80, 80, 80)
gold = (212, 175, 55)
gruen = (50, 200, 50)
rot = (200, 50, 50)
beige = (245, 222, 179)
hellblau = (173, 216, 230)

class Level:
    # einzelnes Level auf der map

    radius = 55 # kreis für ein level

    def __init__(self, daten):
        self.name = daten["name"]
        self.pos = daten["pos"]
        self.freigeschaltet = daten["freigeschaltet"]
        self.boss = daten["boss"]
        self.besucht = False

    def zeichnen(self, screen, font, ausgewaehlt):
        x, y = self.pos

        # frabe nach "Status" vom Level
        if self.boss:
            farbe = rot if self.freigeschaltet else dunkelgrau
        elif self.besucht:
            farbe = gruen
        elif self.freigeschaltet:
            farbe = hellblau
        else:
            farbe = dunkelgrau

        # goldener Rahmen wenn ausgewählt
        if ausgewaehlt:
            pygame.draw.circle(screen, gold, (x, y), self.radius + 8)

        # Kreis und Umrandung zeichnen
        pygame.draw.circle(screen, farbe, (x, y), self.radius)
        pygame.draw.circle(screen, schwarz, (x, y), self.radius, 2)

        # schloss anzeigen wenn level gesperrt
        if not self.freigeschaltet:
            schloss = font.render("🔒", True, weiss)
            screen.blit(schloss, (x - schloss.get_width() // 2, y - schloss.get_height() // 2))
        else:
            text = font.render(self.name, True, schwarz)
            screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

    def wird_geklickt(self, maus_pos):
        # prüft ob der Mausklick richtig, von claude naachgeschaut
        mx, my = maus_pos
        lx, ly = self.pos
        abstand = math.hypot(mx - lx, my - ly)
        return abstand <= self.radius


class Fortschrittsmap:
    def __init__(self, screen):
        self.screen = screen
        self.hintergrund = pygame.transform.scale(
            pygame.image.load("Spiel/Hintergründe/2/background.png").convert(),
            (breite, hoehe) 
        )
        self.font = pygame.font.SysFont("Arial", 14, bold=True)
        self.titel_font = pygame.font.SysFont("Arial", 42, bold=True)
        self.info_font = pygame.font.SysFont("Arial", 24)
        self.ausgewaehlt = None

        # level-Daten sollen sein: Name, Position auf der Map, freigeschaltet?, Boss?
        level_daten = [
            {"name": "Kampf 1", "pos": (240, 540), "freigeschaltet": True,  "boss": False},
            {"name": "Kampf 2", "pos": (624, 540), "freigeschaltet": False, "boss": False},
            {"name": "Kampf 3", "pos": (960, 540), "freigeschaltet": False, "boss": False},
            {"name": "Kampf 4", "pos": (1296, 540), "freigeschaltet": False, "boss": False},
            {"name": "BOSS", "pos": (1680, 540), "freigeschaltet": False, "boss": True},
        ]

        # verbindungen zwischen Leveln (welche sind durch Linien verbunden)
        self.verbindungen = [(0, 1), (1, 2), (2, 3), (3, 4)]
        # level-Objekte aus den Daten erstellen, bei claude nachgeguckt
        self.level_liste = [Level(d) for d in level_daten]

    def zeichnen(self):
        # wieder hintergrund mit abdunkelung
        self.screen.blit(self.hintergrund, (0,0))
        dunkel =pygame.Surface((breite, hoehe),pygame.SRCALPHA)
        dunkel.fill((0,0,0,150))
        self.screen.blit(dunkel, (0,0))

        #titel
        titel = self.titel_font.render("Quest 1892", True, gold)
        self.screen.blit(titel, (breite // 2 -titel.get_width()//2, 60))

        # verbindungslinien zwischen Leveln
        for (a, b) in self.verbindungen:
            pos_a = self.level_liste[a].pos
            pos_b = self.level_liste[b].pos
            farbe = gruen if self.level_liste[b].freigeschaltet else grau
            pygame.draw.line(self.screen, farbe, pos_a, pos_b, 4)

        # alle Level zeichnen, bei claude nachgeguckt
        for i, level in enumerate(self.level_liste):
            level.zeichnen(self.screen, self.font, ausgewaehlt=(self.ausgewaehlt == i))
        self.info_box_zeichnen()

    def info_box_zeichnen(self):
        # dunkler Balken unten mit Infos zum ausgewählten Level
        pygame.draw.rect(self.screen, (30,20,10), (0, hoehe - 100, breite, 100))
        pygame.draw.line(self.screen, gold, (0, hoehe-100),(breite, hoehe -100),2)

        if self.ausgewaehlt is not None:
            level = self.level_liste[self.ausgewaehlt]
            if level.freigeschaltet:
                text = f"▶  {level.name}  –  Klicke erneut zum Starten!"
                farbe = gold
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
        for i, lv in enumerate(self.level_liste):
            if lv.wird_geklickt(maus_pos):
                if self.ausgewaehlt == i and lv.freigeschaltet:
                    # zweiter Klick auf selbe Level soll starten
                    return i
                else:
                    # erstes Mal klicken soll nur auswählen
                    self.ausgewaehlt = i
                    return None
        # wenn Klick ins Leere - auswahl aufgehoben
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
                            txt = font.render("🏆 Du hast den Schatz gefunden!")
                            screen.blit(txt, (breite //2 - txt.get_width()// 2, hoehe // 2-40))
                            pygame.display.flip()
                            pygame.time.wait(4000)
                            pygame.time.wait(33)
                            return # zurück zu hauptmenü
                        

        karte.zeichnen()
        pygame.display.flip()
        clock.tick(60)


