import pygame
import math

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
                self.schussTimer += 1
                if self.schussTimer >= self.schussCooldown:
                    self.schussTimer = 0
                    self.angriff_aktiv = True
                    self.attackIndex = 0
                    dx = spieler.x - self.x
                    dy = spieler.y - self.y
                    if dx < 0:
                        self.last = [1, 0]
                    else:
                        self.last = [0, 1]
                    distanz = math.sqrt(dx**2 + dy**2)
                    if distanz > 0:
                        self.kugeln.append(GegnerKugel(self.screen, self.x + self.breite//2, self.y + self.hoehe//2, dx/distanz, dy/distanz, 8, self.projektil))

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
            self.hitbox = pygame.Rect(self.x+50, self.y+80, self.breite-70, self.hoehe)
            self.kopf = pygame.Rect(self.x+30, self.y, self.breite-70, self.hoehe-200)
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
        elif self.gegnerArt == "Fernkampf":
            self.hitbox = pygame.Rect(self.x+25, self.y+25, self.breite-50, self.hoehe-50)
            self.kopf = pygame.Rect(0, 0, 0, 0)
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
                    frameAnzahl = len(self.angriffAnimation)
                    bildIndex = min(self.attackIndex // 5, frameAnzahl - 1)
                    if self.last[0]:
                        self.screen.blit(pygame.transform.flip(pygame.transform.scale(self.angriffAnimation[bildIndex], (self.breite, self.hoehe)), True, False), (self.x, self.y))
                    else:
                        self.screen.blit(pygame.transform.scale(self.angriffAnimation[bildIndex], (self.breite, self.hoehe)), (self.x, self.y))
                    self.attackIndex += 1
                    if self.attackIndex >= frameAnzahl * 5:
                        self.angriff_aktiv = False
                        self.attackIndex = 0
                elif self.getroffen and len(self.trefferAnimation) > 0:
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
                    frameAnzahl = len(self.standAnimation)
                    if self.standIndex >= frameAnzahl * 10:
                        self.standIndex = 0
                    bildIndex = self.standIndex // 10
                    if self.last[0]:
                        self.screen.blit(pygame.transform.flip(pygame.transform.scale(self.standAnimation[bildIndex], (self.breite, self.hoehe)), True, False), (self.x, self.y))
                    else:
                        self.screen.blit(pygame.transform.scale(self.standAnimation[bildIndex], (self.breite, self.hoehe)), (self.x, self.y))
                    self.standIndex += 1            
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
        self.screen.blit(pygame.transform.scale(self.bild, (80, 80)), (self.x, self.y))


        