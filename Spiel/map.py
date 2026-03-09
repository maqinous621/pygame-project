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

    def __init__(self, name, pos, freigeschaltet, boss):
        self.name           = name
        self.pos            = pos
        self.freigeschaltet = freigeschaltet
        self.boss           = boss
        self.besucht        = False

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
            schloss = font.render("", True, weiss)
            screen.blit(schloss, (x - schloss.get_width() // 2, y - schloss.get_height() // 2))
        else:
            text = font.render(self.name, True, schwarz)
            screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

    def wird_geklickt(self, maus_pos):
        # prüft ob der Mausklick richtig, von claude naachgeschaut
        mx, my = maus_pos
        lx, ly = self.pos
        return math.hypot(mx - lx, my - ly) <= self.radius


class Fortschrittsmap:
    def __init__(self, screen):
        self.screen = screen
        self.hintergrund = pygame.transform.scale(
            pygame.image.load("Spiel/Hintergründe/2/background.png").convert(),
            (breite, hoehe) 
        )
        self.font = pygame.font.SysFont("Arial", 14, bold=True)
        self.titel_font = pygame.font.SysFont("Arial", 72, bold=True)
        self.ausgewaehlt = None

        # level-Daten sollen sein: Name, Position auf der Map, freigeschaltet?, Boss?
        self.level_liste = [
            Level("Kampf 1", (240,  540), True,  False),
            Level("Kampf 2", (624,  540), False, False),
            Level("Kampf 3", (960,  540), False, False),
            Level("Kampf 4", (1296, 540), False, False),
            Level("BOSS",    (1680, 540), False, True),
        ]

    def zeichnen(self):
        # wieder hintergrund mit abdunkelung
        self.screen.blit(self.hintergrund, (0,0))
        dunkel =pygame.Surface((breite, hoehe),pygame.SRCALPHA)
        dunkel.fill((0,0,0,150))
        self.screen.blit(dunkel, (0,0))

        #titel
        titel = self.titel_font.render("Quest 1892", True, gold)
        self.screen.blit(titel, (breite // 2 -titel.get_width()//2, 60))

        #  verbindungslinien zwischen den Leveln
        for i in range(len(self.level_liste) - 1):
            pos_a = self.level_liste[i].pos
            pos_b = self.level_liste[i + 1].pos
            farbe = gruen if self.level_liste[i + 1].freigeschaltet else grau
            pygame.draw.line(self.screen, farbe, pos_a, pos_b, 4)

        for i, lv in enumerate(self.level_liste):
            lv.zeichnen(self.screen, self.font, ausgewaehlt=(self.ausgewaehlt == i))

    # ein Klick startet direkt
    def klick_verarbeiten(self, maus_pos):
        for i, lv in enumerate(self.level_liste):
            if lv.wird_geklickt(maus_pos) and lv.freigeschaltet:
                return i
        return None

    # level abschliessen
    def level_abschliessen(self, index):
        self.level_liste[index].besucht = True
        if index + 1 < len(self.level_liste):
            self.level_liste[index + 1].freigeschaltet = True


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


