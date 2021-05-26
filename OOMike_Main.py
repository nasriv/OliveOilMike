#!/usr/bin/env python
import pygame
from pygame import *
import sys
import random, os, time, math

from types import *

pygame.init()

# Initialize variables
display_width = 600
display_height = 600
HH = int(display_height/2)
HW = int(display_width/2)
FPS = 120

# Initialize colors
black = (0,0,0)
white = (255,255,255)
ltGreen = (153,255,153)
ltRed = (255, 204, 204)

homedir = os.path.dirname(__file__)
imagedir = os.path.join(homedir, "images")

gameTitle = "Olive Oil Mike"

gameDisplay = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()

pygame.display.set_caption(gameTitle)

persistentCount = 0
muPos = 0
muPosPrev = 0
musicList=os.listdir("music")
random.shuffle(musicList)


# Import background
bkIMG = pygame.image.load(os.path.join(imagedir,"background.png"))
bkIMG = bkIMG.convert()

# Import intro logo
IntroLogo = pygame.image.load(os.path.join(imagedir,"IntroLogo.png"))
IntroLogo = IntroLogo
Logorect = IntroLogo.get_rect()
hw_logo = int(Logorect.width/2)

# Import Player icon
plW = 390
plH = 490
SCALE = 7


class PlayerSprite:

    def __init__(self, name: str, scale: float = SCALE):
        self.name = name
        for side in 'left', 'right':
            setattr(
                self,
                side,
                pygame.transform.scale(
                    pygame.image.load(
                        os.path.join(
                            imagedir,
                            os.path.join(
                                imagedir,
                                "PlayerSprite{}{}.png".format(
                                    side.capitalize(),
                                    name
                                ),
                            ),
                        )
                    ),
                    (int(plW / scale), int(plH / scale)),
                ),
            )


PLAYER_SPRITE_MIKE = PlayerSprite("")
PLAYER_SPRITE_GRANT = PlayerSprite("Grant")
PLAYER_SPRITE_VINNY = PlayerSprite("Vinny")
PLAYER_SPRITE_CHRIS = PlayerSprite("Chris", scale=4)
PLAYER_SPRITE_STEF = PlayerSprite("Stef")
PLAYER_SPRITE_JONNY = PlayerSprite("Jonny", scale=4)

PlayerR_mask = pygame.mask.from_surface(PLAYER_SPRITE_MIKE.right)
PLayerL_mask = pygame.mask.from_surface(PLAYER_SPRITE_MIKE.left)

# import olive oil collectible
OilW = 548
OilH = 720
oilImg = pygame.image.load(os.path.join(imagedir,"OliveOilCollect.png"))
oilImg = pygame.transform.scale(oilImg,(int(OilW/8), int(OilH/8)))

# import rock
RockW = 640
RockH = 480
rockImg = pygame.image.load(os.path.join(imagedir,"Rock.png"))
rockImg = pygame.transform.scale(rockImg,(150,150))

bulletW=100
bulletH=150
bulletImg = pygame.image.load(os.path.join(imagedir,"bullet.png"))
bulletImg = pygame.transform.scale(bulletImg,(150,150))


# DEFINE CLASSES

class item(pygame.sprite.Sprite):

    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange( 0-self.rect.width, display_width + self.rect.width)
        self.rect.y = random.randrange(-100, -50)
        self.speedy = random.randrange(3, 10)
        self.speedx = random.randrange(-1,1)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > display_height+10 or self.rect.left+self.rect.width <0 or self.rect.right-self.rect.width>display_width:
            self.rect.x = random.randrange( 0-self.rect.width, display_width - self.rect.width)
            self.rect.y = random.randrange(-100, -50)
            self.speedy = random.randrange(3, 10)
            self.speedx = random.randrange(-1, 1)

        self.mask = pygame.mask.from_surface(self.image)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, xDir = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/bullet.png")
        self.image = pygame.transform.scale(self.image,(30,30))
        self.xDir = xDir

        self.rect = self.image.get_rect()
    def update(self):
        yVal = math.sqrt(20*20 - 2.5*2.5*self.xDir*self.xDir)
        self.rect.y -= yVal
        if self.xDir < 0 :
            self.rect.x -= math.sqrt(20*20 - yVal*yVal)
        else:
            self.rect.x += math.sqrt(20*20 - yVal*yVal)

        global gameDisplay
        if not gameDisplay.get_rect().contains(self.rect):
            self.kill()


class Player(pygame.sprite.Sprite):
    # sprite for the player

    PlayerSpriteLeft = PLAYER_SPRITE_MIKE.left
    PlayerSpriteRight = PLAYER_SPRITE_MIKE.right
    playerName="Mike"

    def __init__(self, velocity):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.PlayerSpriteLeft.convert_alpha()
        self.rect = self.image.get_rect()
        self.velocity = velocity
        self.rect.centerx = HW
        self.rect.centery = display_height - self.rect.height/2
        self.counter = 0
        self.boomCounter = 0
        self.interval = 20
        self.boomInterval = -1
        self.doubleBullet = False

    def update(self):
        k = pygame.key.get_pressed()

        if k[K_ESCAPE]:
            game_intro()
        elif k[K_LEFT]:
            self.rect.x -= self.velocity
            self.image = self.PlayerSpriteLeft.convert_alpha()
        elif k[K_RIGHT]:
            self.rect.x += self.velocity
            self.image = self.PlayerSpriteRight.convert_alpha()

        if k[K_UP]:
            self.rect.y -= self.velocity
        elif k[K_DOWN]:
            self.rect.y += self.velocity


        self.counter += 1

        if self.boomInterval > 0:
            self.boomCounter += 1

        if self.counter == self.interval:
            global persistentCount

            if persistentCount >= 60:
                self.boomInterval = 100
            elif persistentCount >= 40:
                self.interval = 10
            elif persistentCount >= 38:
                self.interval = 11
            elif persistentCount >= 36:
                self.interval = 12
            elif persistentCount >= 34:
                self.interval = 13
            elif persistentCount >= 32:
                self.interval = 14
            elif persistentCount >= 30:
                self.doubleBullet = True
            elif persistentCount >= 20:
                self.interval = 15
            elif persistentCount >= 18:
                self.interval = 16
            elif persistentCount >= 16:
                self.interval = 17
            elif persistentCount >= 14:
                self.interval = 18
            elif persistentCount >= 12:
                self.interval = 19
            self.counter = 0

            if persistentCount >= 10:
                if self.doubleBullet:
                    bullet1 = Bullet()
                    bullet2 = Bullet()
                    bullet1.rect.x = self.rect.x - 10
                    bullet1.rect.y = self.rect.y
                    bullet2.rect.x = self.rect.x + 10
                    bullet2.rect.y = self.rect.y
                    all_sprites.add(bullet1)
                    bullet_sprites.add(bullet1)
                    all_sprites.add(bullet2)
                    bullet_sprites.add(bullet2)
                else:
                    bullet = Bullet()
                    bullet.rect.x = self.rect.x
                    bullet.rect.y = self.rect.y
                    all_sprites.add(bullet)
                    bullet_sprites.add(bullet)

        if self.boomCounter == self.boomInterval:

            for i in range(0,11):
                bullet = Bullet(-5 + i)
                bullet.rect.x = self.rect.x
                bullet.rect.y = self.rect.y
                all_sprites.add(bullet)
                bullet_sprites.add(bullet)

            self.boomCounter = 0



        if self.rect.right > display_width:
            self.rect.right = display_width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= display_height:
            self.rect.bottom = display_height

    def set_callback(self, sprite: PlayerSprite):
        def callback():
            self.set_player(sprite)
            game_intro()
        return callback

    def set_player(self, sprite: PlayerSprite):
        self.PlayerSpriteRight = sprite.right
        self.PlayerSpriteLeft = sprite.left
        self.image = self.PlayerSpriteLeft.convert_alpha()
        self.playerName = sprite.name

    def getPlayerName(self):
        return self.playerName

       # self.mask = pygame.mask.from_surface(self.image)

# ------------------------ #

def oil_count(count_oil):
    font = pygame.font.Font('freesansbold.ttf', 25)
    text = font.render("Olive Oil: "+str(count_oil),True,white)
    gameDisplay.blit(text,(0,0))

def gameQuit():
    pygame.quit()
    quit()

def text_object(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None, size=20):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",size)
    textSurf, textRect = text_object(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def message_display(text, pos):
    largeText = pygame.font.Font('freesansbold.ttf',25)
    TextSurf = largeText.render(text, True, white)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((display_width/2),(display_height/2 + pos*50))
    gameDisplay.blit(TextSurf,TextRect)

    pygame.display.update()


def crash(count):
    message_display("You were hit by that kid throwing rocks...", 0)
    message_display("You collected " + str(count) + " bottles...", 1)
    time.sleep(1)
    return


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()

        gameDisplay.blit(bkIMG, (0, 0))
        gameDisplay.blit(IntroLogo,(HW-hw_logo,100))


        button("PLAY", HW-200, HH+20, 400, 50, white, ltGreen, gameLoop)
        button("CHOOSE CHARACTER", HW-200, HH+90, 400, 50, white, ltGreen, gameChar)
        button("CREDITS", HW-200, HH+160, 400, 50, white, ltGreen, gameCredits)
        button("QUIT", HW-200, HH+230, 400, 50, white, ltRed , gameQuit)

        pygame.display.update()
'''
        clock.tick(FPS)
'''

def gameLoop():

    global persistentCount
    count = 0
    gameExit = False

    try:
        while not gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameQuit()

    #MUSIC HANDLING
            global muPos
            global muPosPrev

            if len(musicList) > 0:
                if not pygame.mixer.music.get_busy():
                    if muPos != muPosPrev:
                        pygame.mixer.music.play(1)
                    elif muPos == muPosPrev:
                        pygame.mixer.music.load("music/" + musicList[muPos])
                        pygame.mixer.music.play(1)
                        if muPos < len(musicList) - 1:
                            muPos += 1
                        else:
                            muPos = 0
                elif muPos != muPosPrev:
                    muPosPrev = muPos

            # Backgound blit
            gameDisplay.blit(bkIMG,(0,0))

            # Update
            all_sprites.update()

            # check collision
            hits = pygame.sprite.spritecollide(player, rock_sprites, False, pygame.sprite.collide_mask)
            if hits and (player.getPlayerName() != "Jonny" or musicList[muPos].find("Steamshovel") == -1):
                for c in (rock_sprites, bullet_sprites):
                    for i in c:
                        i.kill()
                crash(persistentCount)
                count = 0

            for rock in rock_sprites:
                for bullet in bullet_sprites:
                    tempBulletSprites = pygame.sprite.Group()
                    tempBulletSprites.add(bullet)
                    rock_hits = pygame.sprite.spritecollide(rock, tempBulletSprites, False, pygame.sprite.collide_mask)
                    if rock_hits:
                        rock.kill()
                        bullet.kill()
                        break

            if len(rock_sprites) < 6:
                r = item(rockImg)
                rock_sprites.add(r)
                all_sprites.add(r)


            # check player collected oil
            collect = pygame.sprite.spritecollide(player, oil_sprites, True, pygame.sprite.collide_mask)
            for _ in collect:
                new_oil = item(oilImg)
                all_sprites.add(new_oil)
                oil_sprites.add(new_oil)
                count += 1

            persistentCount = count
            # Draw / Render
            all_sprites.draw(gameDisplay)
            oil_count(count)

            pygame.display.update()

            clock.tick(FPS)
    except pygame.error:
        sys.exit()


def gameChar():
    time.sleep(.5)
    char = True

    while char:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()

        gameDisplay.blit(bkIMG, (0, 0))
        gameDisplay.blit(IntroLogo,(HW-hw_logo,40))

        button("MIKE (THE GOOD BOY)", HW-200, HH-60, 400, 50, white, ltGreen, player.set_callback(PLAYER_SPRITE_MIKE))
        button("VINNY (EYY, BROOKLYN)", HW-200, HH+0, 400, 50, white, ltRed , player.set_callback(PLAYER_SPRITE_VINNY))
        button("GRANT (NOT THIS ONE)", HW-200, HH+60, 400, 50, white, ltRed , player.set_callback(PLAYER_SPRITE_GRANT))
        button("MCGINN (THE ONE WHO BEANS)", HW-200, HH+120, 400, 50, white, ltRed, player.set_callback(PLAYER_SPRITE_CHRIS))
        button("STEF (SICKO MODE ACTIVATE)", HW-200, HH+180, 400, 50, white, ltRed, player.set_callback(PLAYER_SPRITE_STEF))
        button("STEAMSHOVEL JONNY", HW-200, HH+240, 400, 50, white, ltGreen, player.set_callback(PLAYER_SPRITE_JONNY))

        pygame.display.update()

def gameCredits():
    time.sleep(.5)
    char = True

    while char:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()

        gameDisplay.blit(bkIMG, (0, 0))
        gameDisplay.blit(IntroLogo,(HW-hw_logo,100))

        button("Candy-Colored Sky by  Catmosphere (Creative Commons)", HW-250, HH+20, 500, 50, white, ltGreen, None, 14)
#        button("Steamshovel Harry by Brad Sucks and Allen (Creative Commons)", HW-250, HH+90, 500, 50, white, ltGreen, None, 14)
        button("BACK", HW-250, HH+170, 500, 50, white, ltRed, backToIntro)

        pygame.display.update()


def backToIntro():
    time.sleep(.5)
    game_intro()




# ---- Initialize player and items ---- #

all_sprites = pygame.sprite.Group()
oil_sprites = pygame.sprite.Group()
rock_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()

player = Player(10)
all_sprites.add(player)

for i in range(1):
    o = item(oilImg)
    all_sprites.add(o)
    oil_sprites.add(o)

for j in range(6):
    r = item(rockImg)
    all_sprites.add(r)
    rock_sprites.add(r)

if __name__ == '__main__':
    game_intro()
