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

    def updateSprung(self): # orientiert an https://www.youtube.com/watch?v=ODykzTEzDx8&list=PLjuHXsDGkbTSpTMJ4MXTiQXN4AeOzpu1w&index=2 (min 7:48 - 11:07)
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
        if self.hitbox.colliderect(other.hitbox):
                self.dead = True

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
            self.hitbox = pygame.Rect((self.x + 110, self.y, self.breite-200, self.hoehe))
        else:
            self.hitbox = pygame.Rect((self.x + 80, self.y, self.breite-200, self.hoehe))

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
                if self.rechtsIndex >= 63:
                    self.rechtsIndex = 0
                if self.linksIndex >= 63:
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
        self.y += 123
        self.hitbox = pygame.Rect(self.x-10, self.y-10, 20, 20)

    def bewegen(self):
        self.x += self.geschwindigkeit
        self.hitbox = pygame.Rect(self.x-10, self.y-10, 20, 20)

    def zeichnen(self):
        pygame.draw.circle(self.screen, (0,0,0), (self.x, self.y), 10, 0)


