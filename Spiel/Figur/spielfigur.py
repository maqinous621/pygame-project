import pygame
import math

class Spielfigur:
    
    def __init__(self, screen, x, y, breite, hoehe, richtung, geschwindigkeit):
        self.screen = screen
        self.x = x
        self.y = y
        self.breite = breite
        self.hoehe = hoehe
        self.richtung = richtung
        self.rechtsIndex = 0
        self.linksIndex = 0
        self.sprungIndex = 0
        self.standIndex = 0
        self.totIndex = 0
        self.geschwindigkeit = geschwindigkeit
        self.sprunggeschwindigkeit = geschwindigkeit + 4 # wird nur für die Dauer des Sprungs verwendet, damit die Figur während des Sprungs schneller ist
        self.sprung = False
        self.sprungzahl = 13
        self.kugeln = []
        self.last = [0,1] #Letzte Richtung
        self.go = True
        self.dead = False
        self.schiessenIndex = 0
        self.schiessen_aktiv = False
        self.ok = True
        self.hitbox = pygame.Rect(self.x, self.y, self.breite, self.hoehe)
        self.linkslaufen = [pygame.image.load(f"Spiel/Figur/png/linksRun ({i}).png").convert_alpha() for i in range(1, 9)]
        self.rechtslaufen = [pygame.image.load(f"Spiel/Figur/png/rechtsRun ({i}).png").convert_alpha() for i in range(1, 9)]
        self.stehenRechts = [pygame.image.load(f"Spiel/Figur/png/Idle ({i}).png").convert_alpha() for i in range(1, 11)]
        self.stehenLinks = [pygame.image.load(f"Spiel/Figur/png/linksIdle ({i}).png").convert_alpha() for i in range(1, 11)]
        self.sprungImage = [pygame.image.load(f"Spiel/Figur/png/Jump ({i}).png").convert_alpha() for i in range(1, 11)]
        self.tot = [pygame.image.load(f"Spiel/Figur/png/Dead ({i}).png").convert_alpha() for i in range(1, 11)]
        self.schiessenRechts = [pygame.image.load(f"Spiel/Figur/png/Shoot ({i}).png").convert_alpha() for i in range(1, 4)]
        self.schiessenLinks = [pygame.image.load(f"Spiel/Figur/png/linksShoot ({i}).png").convert_alpha() for i in range(1, 4)]

    def laufen(self, liste):
        if self.sprung:
            speed = self.sprunggeschwindigkeit
        else:
            speed = self.geschwindigkeit
        if liste[0]:
            if self.richtung != [1, 0, 0, 0]: # Prüfen ob die Richtung geändert wurde
                self.resetIndex()
            self.x -= speed
            self.richtung = [1, 0, 0, 0]
            self.linksIndex += 1
        if liste[1]:
            if self.richtung != [0, 1, 0, 0]:
                self.resetIndex()
            self.x += speed
            self.richtung = [0, 1, 0 ,0]
            self.rechtsIndex += 1

    def startSprung(self):
        if not self.sprung:
            if self.richtung != [0, 0, 0, 1]:
                self.resetIndex()
            self.sprung = True
            self.richtung = [0, 0, 0, 1]
            # Sprung Sound hinzufügen

    def updateSprung(self):
        if self.sprung:
            if self.sprungzahl >= -13:
                self.sprungIndex += 1
                neg = 1
                if self.sprungzahl < 0:
                    neg = -1
                self.y -= (self.sprungzahl ** 2) * 0.5 * neg
                self.sprungzahl -= 1
            else:
                self.sprung = False
                self.sprungzahl = 13

    def stehen(self):
        if not self.sprung:
            self.richtung = [0,0,1,0]
        self.standIndex += 1

    def resetIndex(self):
        self.linksIndex = 0
        self.rechtsIndex = 0
        self.sprungIndex = 0
        self.standIndex = 0

    def trefferCheck(self, other):
        for k in self.kugeln:
            if other.hitbox.colliderect(k.hitbox):
                other.leben -= 1
                other.getroffen = True
                other.trefferIndex = 0
                self.kugeln.remove(k)
            elif other.kopf.colliderect(k.x-10,k.y-10, 20, 20):
                other.leben -= 3
                other.getroffen = True
                other.trefferIndex = 0
                self.kugeln.remove(k)
            if other.leben <= 0:
                other.dead = True
                # Treffer Sound hinzufügen
        if self.hitbox.colliderect(other.hitbox):
                self.dead = True
                # Tod Sound hinzufügen

    def schiessen(self):
        if self.ok and not self.schiessen_aktiv:
            self.kugeln.append(Kugel(self.screen, self.x, self.y, self.last, 10))
            self.schiessen_aktiv = True
            self.schiessenIndex = 0
            self.ok = False

    def kugelverhalten(self):
        for k in self.kugeln:
            if k.x > 0 and k.x < 1940 and k.y > 0 and k.y < 1080:
                k.bewegen()
            else:
                self.kugeln.remove(k)

    def spielerImage(self):
        if self.last[0]:
            self.hitbox = pygame.Rect((self.x + 110, self.y, self.breite-165, self.hoehe))
        else:
            self.hitbox = pygame.Rect((self.x + 80, self.y, self.breite-175, self.hoehe))

        if self.dead:
            bildIndex = min(self.totIndex // 10, 9)
            if self.last[0]:
                self.screen.blit(pygame.transform.flip(pygame.transform.scale(self.tot[bildIndex], (self.breite, self.hoehe)), True, False), (self.x, self.y))
            else:
                self.screen.blit(pygame.transform.scale(self.tot[bildIndex], (self.breite, self.hoehe)), (self.x, self.y))
            self.totIndex += 1
            if self.totIndex >= 100:
                self.go = False

        else:
            if self.schiessen_aktiv:
                if self.last[0]:  # links
                    self.screen.blit(pygame.transform.scale(self.schiessenLinks[self.schiessenIndex // 7], (self.breite, self.hoehe)), (self.x, self.y))
                else:
                    self.screen.blit(pygame.transform.scale(self.schiessenRechts[self.schiessenIndex // 7], (self.breite, self.hoehe)), (self.x, self.y))
                self.schiessenIndex += 1
                if self.schiessenIndex >= 21:  # 3 Bilder * 7 Frames pro Bild
                    self.schiessen_aktiv = False
                    self.ok = True
            else:
                if self.rechtsIndex == 63: # UNBEDINGT NOCHMAL NACHSCHAUEN WAS DAS BEDEUTET
                    self.rechtsIndex = 0
                if self.linksIndex == 63:
                    self.linksIndex = 0
                if self.standIndex >= 100:
                    self.standIndex = 0
                if self.sprungIndex >= 100:
                    self.sprungIndex = 0

                if self.richtung[0]:
                    self.screen.blit(pygame.transform.scale(self.linkslaufen[self.linksIndex//8], (self.breite, self.hoehe)), (self.x, self.y))
                    self.last =[1,0]
                
                if self.richtung[1]:
                    self.screen.blit(pygame.transform.scale(self.rechtslaufen[self.rechtsIndex//8], (self.breite, self.hoehe)), (self.x, self.y))
                    self.last =[0,1]
                
                if self.richtung[2]:
                    if self.last[1]:
                        self.screen.blit(pygame.transform.scale(self.stehenRechts[self.standIndex//10], (self.breite, self.hoehe)), (self.x, self.y))
                    else:
                        self.screen.blit(pygame.transform.scale(self.stehenLinks[self.standIndex//10], (self.breite, self.hoehe)), (self.x, self.y))

                if self.richtung[3]:
                    if self.last[0]:
                        self.screen.blit(pygame.transform.flip(pygame.transform.scale(self.sprungImage[self.sprungIndex//10], (self.breite, self.hoehe)), True, False), (self.x, self.y))
                    else:
                        self.screen.blit(pygame.transform.scale(self.sprungImage[self.sprungIndex//10], (self.breite, self.hoehe)), (self.x, self.y))

class Kugel:
    def __init__(self, screen, spX, spY, last, geschwindigkeit):
        self.screen = screen
        self.x = spX
        self.y = spY
        if last[0]:
            self.x += 5
            self.geschwindigkeit = -geschwindigkeit
        elif last[1]:
            self.x += 300
            self.geschwindigkeit = geschwindigkeit
        self.y += 50
        self.hitbox = pygame.Rect(self.x-10, self.y-10, 20, 20)

    def bewegen(self):
        self.x += self.geschwindigkeit
        self.hitbox = pygame.Rect(self.x-10, self.y-10, 20, 20)

    def zeichnen(self):
        pygame.draw.circle(self.screen, (0,0,0), (self.x, self.y), 10, 0)

##############################################################################################################

class Gegner:
    def __init__(self, screen, gegnerArt, x, y, xMin, xMax, breite, hoehe, richtung, geschwindigkeit, leben, projektil = None, angriffAnimation = [], laufAnimation = [], standAnimation = [], FlugAnimation = [], totAnimation = [], trefferAnimation = []):
        self.screen = screen
        self.gegnerArt = gegnerArt
        self.x = x
        self.y = y 
        self.xMin = xMin
        self.xMax = xMax
        self.breite = breite
        self.hoehe = hoehe
        self.richtung = richtung
        self.yRichtung = 1 # 1 = runter, -1 = hoch (nur für fliegende Gegner relevant)
        self.geschwindigkeit = geschwindigkeit
        self.leben = leben
        self.angriffAnimation = angriffAnimation
        self.laufAnimation = laufAnimation
        self.standAnimation = standAnimation
        self.FlugAnimation = FlugAnimation
        self.totAnimation = totAnimation
        self.trefferAnimation = trefferAnimation
        self.projektil = pygame.image.load(projektil).convert_alpha() if projektil else None
        self.angriffIndex = 0
        self.laufIndex = 0
        self.standIndex = 0 
        self.FlugIndex = 0
        self.totIndex = 0
        self.trefferIndex = 0
        self.herzen = [pygame.image.load("Spiel/Figur/png/voll.png"), pygame.image.load("Spiel/Figur/png/halb.png"), pygame.image.load("Spiel/Figur/png/leer.png")]
        self.hitbox = pygame.Rect(self.x, self.y, self.breite, self.hoehe)
        self.kopf = pygame.Rect(self.x, self.y, self.breite, self.hoehe)
        self.sprung = False
        self.kugeln = []
        self.schussTimer = 0
        self.schussCooldown = 180  # 3 Sekunden bei 60 FPS
        self.getroffen = False
        self.angriff_aktiv = False
        self.dead = False
        self.go = True
        self.last = [1,0] #Letzte Richtung

    def bewegen(self, spieler):
        if self.dead:
            return
        else:
            if self.gegnerArt == "Nahkampf":
                if self.richtung == [1,0,0,0]: # Links
                    self.x -= self.geschwindigkeit
                    self.last = [1,0]
                    self.laufIndex += 1
                elif self.richtung == [0,1,0,0]: # Rechts
                    self.x += self.geschwindigkeit
                    self.last = [0,1]
                    self.laufIndex += 1
            elif self.gegnerArt == "Fernkampf":
                pass

            elif self.gegnerArt == "Fliegend":
            
                if not self.angriff_aktiv:  # Richtung nur ändern wenn kein Angriff
                    if self.richtung == [1,0,0,0]:
                        self.x -= self.geschwindigkeit
                        self.last = [1,0]
                    elif self.richtung == [0,1,0,0]:
                        self.x += self.geschwindigkeit
                        self.last = [0,1]
                else:
                    # Trotzdem bewegen, aber last nicht ändern
                    if self.richtung == [1,0,0,0]:
                        self.x -= self.geschwindigkeit
                    elif self.richtung == [0,1,0,0]:
                        self.x += self.geschwindigkeit
                            
                # Vertikale Wellenbewegung
                if self.yRichtung == 1:  # runter
                    self.y += self.geschwindigkeit
                    if self.y >= 600:
                        self.yRichtung = -1
                else:  # hoch
                    self.y -= self.geschwindigkeit
                    if self.y <= 200:
                        self.yRichtung = 1

                 # Schießen
                self.schussTimer += 1
                if self.schussTimer >= self.schussCooldown:
                    self.schussTimer = 0
                    self.angriff_aktiv = True
                    self.attackIndex = 0
                    dx = spieler.x - self.x
                    dy = spieler.y - self.y
                    # Richtung zum Spieler setzen
                    if dx < 0:
                        self.last = [1, 0]  # Spieler ist links
                    else:
                        self.last = [0, 1]  # Spieler ist rechts
                    distanz = math.sqrt(dx**2 + dy**2)
                    if distanz > 0:
                        self.kugeln.append(GegnerKugel(self.screen, self.x + self.breite//2, self.y + self.hoehe//2, dx/distanz, dy/distanz, 8, self.projektil))
            elif self.gegnerArt == "Boss":
                pass

    def Bewegungsregler(self):
        if self.x <= self.xMin:
            self.richtung = [0,1,0,0]
            self.laufIndex = 0
        elif self.x >= self.xMax:
            self.richtung = [1,0,0,0]
            self.laufIndex = 0
    
    def kugelverhalten(self, spieler):
        for k in self.kugeln:
            if 0 < k.x < 1940:
                k.bewegen()
                k.zeichnen()
                if k.hitbox.colliderect(spieler.hitbox):
                    spieler.dead = True
                    self.kugeln.remove(k)
            else:
                self.kugeln.remove(k)
            

    def gegnerImage(self):  
        if self.gegnerArt == "Nahkampf":
            self.hitbox = pygame.Rect(self.x+50, self.y+130, self.breite-70, self.hoehe)
            self.kopf = pygame.Rect(self.x+30, self.y, self.breite-70, self.hoehe-130)
            if self.dead: # mit Hilfe von Claude.Ai erstellt, da die Tot-Animation des Zombies nicht richtig angezeigt wurde
                frameAnzahl = len(self.totAnimation)
                bildIndex = min(self.totIndex // 10, frameAnzahl - 1)

                referenzBreite = self.laufAnimation[0].get_width()
                origBreite, origHoehe = self.totAnimation[bildIndex].get_size()
                skalierung = self.breite / referenzBreite
                
                totBreite = int(origBreite * skalierung)
                totHoehe = int(origHoehe * skalierung)
                
                bodenY = self.y + self.hoehe          # Boden bleibt fest
                zeichenY = bodenY - totHoehe          # Bild von unten positionieren
                
                if self.last[0]:
                    self.screen.blit(pygame.transform.flip(pygame.transform.scale(self.totAnimation[bildIndex], (totBreite, totHoehe)), True, False), (self.x, zeichenY))
                else:
                    self.screen.blit(pygame.transform.scale(self.totAnimation[bildIndex], (totBreite, totHoehe)), (self.x, zeichenY))
                
                if self.totIndex < frameAnzahl * 10:
                    self.totIndex += 1
                else:
                    self.go = False
            else:
                if self.getroffen and len(self.trefferAnimation) > 0:
                    frameAnzahl = len(self.trefferAnimation)
                    bildIndex = min(self.trefferIndex // 5, frameAnzahl - 1)
                    if self.last[0]:
                        self.screen.blit(pygame.transform.flip(pygame.transform.scale(self.trefferAnimation[bildIndex], (self.breite, self.hoehe)), True, False), (self.x, self.y))
                    else:
                        self.screen.blit(pygame.transform.scale(self.trefferAnimation[bildIndex], (self.breite, self.hoehe)), (self.x, self.y))
                    self.trefferIndex += 1
                    if self.trefferIndex >= frameAnzahl * 5:
                        self.getroffen = False
                        self.trefferIndex = 0
                else:
                    if self.laufIndex >= len(self.laufAnimation) ** 2 - 1: 
                        self.laufIndex = 0
                    if self.richtung == [1,0,0,0]:
                        self.screen.blit(pygame.transform.flip(pygame.transform.scale(self.laufAnimation[self.laufIndex//len(self.laufAnimation)], (self.breite, self.hoehe)), True, False), (self.x, self.y))
                    elif self.richtung == [0,1,0,0]:
                        self.screen.blit(pygame.transform.scale(self.laufAnimation[self.laufIndex//len(self.laufAnimation)], (self.breite, self.hoehe)), (self.x, self.y))
                    
        elif self.gegnerArt == "Fliegend":
            self.hitbox = pygame.Rect(self.x+25, self.y+25, self.breite-50, self.hoehe-50)
            self.kopf = pygame.Rect(0, 0, 0, 0) # Fliegende Gegner haben keinen separaten Kopf-Hitbox
            if self.dead:
                frameAnzahl = len(self.totAnimation)
                bildIndex = min(self.totIndex // 10, frameAnzahl - 1)
                if self.last[0]:
                    self.screen.blit(pygame.transform.flip(pygame.transform.scale(self.totAnimation[bildIndex], (self.breite, self.hoehe)), True, False), (self.x, self.y))
                else:
                    self.screen.blit(pygame.transform.scale(self.totAnimation[bildIndex], (self.breite, self.hoehe)), (self.x, self.y))
                if self.totIndex < frameAnzahl * 10:
                    self.totIndex += 1
                else:
                    self.go = False
            else:
                if self.angriff_aktiv:
                    bildIndex = min(self.attackIndex // 5, 7)
                    if self.last[1]:
                        self.screen.blit(pygame.transform.flip(pygame.transform.scale(self.angriffAnimation[bildIndex], (self.breite, self.hoehe)), True, False), (self.x, self.y))
                    else:
                        self.screen.blit(pygame.transform.scale(self.angriffAnimation[bildIndex], (self.breite, self.hoehe)), (self.x, self.y))
                    self.attackIndex += 1
                    if self.attackIndex >= 40:  # 8 Bilder * 5 Frames
                        self.angriff_aktiv = False
                        self.attackIndex = 0
                elif self.getroffen:
                    frameAnzahl = len(self.trefferAnimation)
                    bildIndex = min(self.trefferIndex // 5, frameAnzahl - 1)
                    if self.last[0]:
                        self.screen.blit(pygame.transform.flip(pygame.transform.scale(self.trefferAnimation[bildIndex], (self.breite, self.hoehe)), True, False), (self.x, self.y))
                    else:
                        self.screen.blit(pygame.transform.scale(self.trefferAnimation[bildIndex], (self.breite, self.hoehe)), (self.x, self.y))
                    self.trefferIndex += 1
                    if self.trefferIndex >= frameAnzahl * 5:
                        self.getroffen = False
                        self.trefferIndex = 0
                else:
                    if self.FlugIndex >= len(self.FlugAnimation) ** 2 - 1:
                        self.FlugIndex = 0
                    if self.last[1]:
                        self.screen.blit(pygame.transform.flip(pygame.transform.scale(self.FlugAnimation[self.FlugIndex // len(self.FlugAnimation)], (self.breite, self.hoehe)), True, False), (self.x, self.y))
                    else:
                        self.screen.blit(pygame.transform.scale(self.FlugAnimation[self.FlugIndex // len(self.FlugAnimation)], (self.breite, self.hoehe)), (self.x, self.y))
                    self.FlugIndex += 1
        elif self.gegnerArt == "Fernkampf":
            pass

        # Herzenanzeige
        #VOLL
        if self.leben >= 2:
            self.screen.blit(self.herzen[0], (self.x - 25,self.y-70))
        if self.leben >= 4:
            self.screen.blit(self.herzen[0], (self.x + 37,self.y-70))
        if self.leben == 6:
            self.screen.blit(self.herzen[0], (self.x + 99,self.y-70))
        #HALB
        if self.leben == 1:
            self.screen.blit(self.herzen[1], (self.x - 25,self.y-70))
        elif self.leben == 3:
            self.screen.blit(self.herzen[1], (self.x + 37,self.y-70))
        if self.leben == 5:
            self.screen.blit(self.herzen[1], (self.x + 99,self.y-70))
        #LEER
        if self.leben <= 0:
            self.screen.blit(self.herzen[2], (self.x - 25,self.y-70))
        if self.leben <= 2:
            self.screen.blit(self.herzen[2], (self.x + 37,self.y-70))
        if self.leben <= 4:
            self.screen.blit(self.herzen[2], (self.x + 99,self.y-70))

class GegnerKugel:
    def __init__(self, screen, x, y, dx, dy, geschwindigkeit, bild):
        self.screen = screen
        self.x = x
        self.y = y
        self.dx = dx * geschwindigkeit
        self.dy = dy * geschwindigkeit
        self.bild = bild
        self.hitbox = pygame.Rect(self.x, self.y, 20, 20)

    def bewegen(self):
        self.x += self.dx
        self.y += self.dy
        self.hitbox = pygame.Rect(self.x, self.y, 20, 20)

    def zeichnen(self):
        self.screen.blit(pygame.transform.scale(self.bild, (40, 40)), (self.x, self.y))