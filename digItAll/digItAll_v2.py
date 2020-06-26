# dig it all version 2.0

# ************************************ TO DO **********************************************
# 1) enemy and player collision - add noise and inability to detect
# 2) weight limit: need to empty junk, trash icon
# 3) pouch: see all finds and info blurb about them by clicking on each
# 4) 2-3 other beep signals depending on what is found

import random
import time
import math
import pygame
from pygame import mixer
import time

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# hide for mac, unhide for windows
import winsound
player_beep = mixer.Sound('C:/Users/nahol/Dropbox/Code/beep.wav')
# high_tone = mixer.Sound('C:/Users/nahol/Dropbox/Code/high_tone_beep.wav')
# low_tone = mixer.Sound ('C:/Users/nahol/Dropbox/Code/low_tone_beep.wav')


WIDTH = 900
HEIGHT = 800
item_image_size = (200, 200)
num_items = 50


# set frame
frame = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dig It All!')
clock = pygame.time.Clock()

# register shapes
background_image = pygame.image.load('grass-bg.gif')

# character images
playerImg = pygame.image.load('player_right.gif')
player_left = pygame.image.load('player_left.gif')
player_down = pygame.image.load('player_up.gif')
player_up = pygame.image.load('player_down.gif')

enemy_down = pygame.image.load('enemy_down.gif')
enemy_up = pygame.image.load('enemy_up.gif')
enemy_left = pygame.image.load('enemy_left.gif')
enemy_right = pygame.image.load('enemy_right.gif')

plug = pygame.image.load('plug.gif')

# item images
barber = pygame.image.load('barber-quarter.gif')
buckle = pygame.image.load('colonial-shoe-buckle.gif')
crotal_bell = pygame.image.load('crotal-bell.gif')
dandy = pygame.image.load('dandy-button.gif')
gw = pygame.image.load('gw-button.gif')
harmonica_reed = pygame.image.load('harmonica-reed.gif')
jaw_harp = pygame.image.load('jaw-harp.gif')
skellie = pygame.image.load('key.gif')
musket_ball = pygame.image.load('musket-ball.gif')
ox_knob = pygame.image.load('ox-knob.gif')
pull_tab = pygame.image.load('pull-tab.gif')
nail = pygame.image.load('rusty-nail.gif')
thimble = pygame.image.load('thimble.gif')
tombac = pygame.image.load('tombac-button.gif')
two_tine_fork = pygame.image.load('two-tine-fork.gif')
walking_half = pygame.image.load('walking-half.gif')
real = pygame.image.load('2-real.gif')
pine_tree = pygame.image.load('pine-tree-shilling.gif')
ox_shoe = pygame.image.load('ox-shoe.gif')
fugio = pygame.image.load('fugio.gif')


rareItems = ['GW button', 'pine tree shilling', 'fugio', '2-real']
commonItems = ['tombac button', 'ox knob', 'harmonica reed', 'musket ball', 'ox shoe']*5
semiRareItems = ['colonial shoe buckle', 'walking half dollar', 'skeleton key', 'two-tine fork', 'crotal bell', 'jaw harp', 'barber quarter', 'thimble', 'dandy button']*2
junk = ['rusty nail', 'pull tab']*5
allItems = rareItems + commonItems + semiRareItems + junk

image_pairs = {'ox knob': ox_knob, 'skeleton key': skellie, 'rusty nail': nail, 'two-tine fork': two_tine_fork,
            'GW button': gw, 'pull tab': pull_tab, 'musket ball': musket_ball, 'barber quarter': barber, 'thimble': thimble,
             'dandy button': dandy, 'walking half dollar': walking_half, 'jaw harp': jaw_harp,
            'tombac button': tombac, 'harmonica reed': harmonica_reed, 'crotal bell': crotal_bell,
             'colonial shoe buckle': buckle, '2-real': real, 'ox shoe': ox_shoe, 'fugio': fugio, 'pine tree shilling': pine_tree}

values = {'GW button': 75, 'pine tree shilling': 100, 'fugio': 50, 'rusty nail': 0, 'tombac button': 15, 'pull tab': 0,
        'ox knob': 5, 'harmonica reed': 5, 'two-tine fork': 30, 'colonial shoe buckle': 30, 'walking half dollar': 25, '2-real': 75, 'skeleton key': 25, 'crotal bell': 30, 'jaw harp': 15,
        'musket ball': 10, 'barber quarter': 20, 'thimble': 15, 'dandy button': 20, 'ox shoe': 2}



# define colors
white = (255,255,255)
black = (0,0,0)
green = (0,150,70)
darkgreen = (0,40, 0)
lightgreen = (210,255,210)

# define variables
newgame = True
menuOpen = True
treasuresOpen = False
highScoresOpen = False
controlsOpen = False
creditsOpen = False
aMenu = True
inPlay = False
dig = False
digIt = ()
playerDigs = False
recentDig = False
recentItem = 'undefined'
recentImage = 'undefined'
highScores = []
menu_button_size = [350,25]
large_menu_window = [100, 100, WIDTH-200, HEIGHT-200]
back_button = [110, 110, 160, 25]
sm_button_size = [125, 25]

# define fonts
main_btn_font = pygame.font.Font('freesansbold.ttf', 30)
back_btn_font = pygame.font.Font('freesansbold.ttf', 18)
title_font = pygame.font.Font('freesansbold.ttf', 30)
menu_font = pygame.font.Font('freesansbold.ttf', 50)
score_font = pygame.font.Font('freesansbold.ttf', 20)
sm_menu_font = pygame.font.Font('freesansbold.ttf', 18)
font = pygame.font.Font('freesansbold.ttf', 15)


def endGame():
    global inPlay
    inPlay = False
    result = ''
    if player1.score > enemy1.score:
        result = 'won!'
    else:
        result = 'lost!'
    end1 = title_font.render('Congratulations! Everything has been found!', True, darkgreen)
    end2 = menu_font.render('Game Over! You ' + result, True, darkgreen)
    end3 = title_font.render("Don't forget to save your high score!", True, darkgreen)
    end4 = title_font.render("You're score will not be saved", True, darkgreen)
    end5 = score_font.render("and look at your treasures before you go!", True, darkgreen)
    if menuOpen != True and treasuresOpen != True and controlsOpen != True and highScoresOpen != True:
        frame.blit(end2, (200, 275))
        frame.blit(end1, (100, 350))
        if result == 'won!':
            frame.blit(end3, (200, 450))
        if result == 'lost!':
            frame.blit(end4, (150, 450))
        frame.blit(end5, (250, 490))


def round_rect(topLeft, width, height, color):
    # edges
    x = topLeft[0]
    y = topLeft[1]
    w = width
    h = height
    radius = 10
    pygame.draw.rect(frame, color, [x-radius, y, w+radius*2, h])
    pygame.draw.rect(frame, color, [x, y-radius, w, h+radius*2])
    # corners
    pygame.draw.circle(frame, color, (x, y), radius)
    pygame.draw.circle(frame, color, (x+w, y), radius)
    pygame.draw.circle(frame, color, (x, y+h), radius)
    pygame.draw.circle(frame, color, (x+w, y+h), radius)

# define game functions

def newGame():
    global newgame, item_locs_found, items_id, finds_pouch, username
    # newgame = False
    finds_pouch = []
    username = ''
    player1.score = 0
    enemy1.score = 0
    createItems()
    item_locs_found = []
    items_id = []
    for i in items:
        i.get_value()
        i.get_type()

    # create items
    for i in items:
        new_id = i.id
        items_id.append(new_id)


def mainMenu():
    global menux, menuy, menuw, menuh, spacing, yspacing, button_font, newgame
    aMenu = True
    menux = int(WIDTH/4)
    menuy = int(HEIGHT/4)
    menuw = int(WIDTH/2)
    menuh = int(HEIGHT/2)+60
    b1 = int(menu_button_size[0])
    b2 = int(menu_button_size[1])
    # menu size
    spacing = 50
    yspacing = 30
    keyx = 585


    # menu window
    round_rect((menux, menuy), menuw, menuh, lightgreen)
    menuTitle = menu_font.render("Menu [m]", True, darkgreen)
    frame.blit(menuTitle, (menux+120,menuy+20))

    # play button
    if newgame == True:
        playButton = main_btn_font.render(" New Game", True, lightgreen)
        n = main_btn_font.render("[n]", True, lightgreen)
        round_rect((menux+spacing, menuy+yspacing*3), b1, b2, green)
        frame.blit(playButton, (menux+spacing,menuy+yspacing*3))
        frame.blit(n, (keyx,menuy+yspacing*3))
    elif newgame == False:
        resumeButton = main_btn_font.render(" Resume [r]", True, lightgreen)
        restartButton = main_btn_font.render(" Restart [n]", True, lightgreen)
        round_rect((menux+spacing, menuy+yspacing*3), int(b1/2-20), b2, green)
        round_rect((menux+spacing+int(b1/2+20), menuy+yspacing*3), int(b1/2-20), b2, green)
        frame.blit(resumeButton, (menux+spacing-10,menuy+yspacing*3))
        frame.blit(restartButton, (menux+spacing+b1/2+10,menuy+yspacing*3))


    # controls button
    controlsButton = main_btn_font.render(' Controls', True, lightgreen)
    c = main_btn_font.render('[c]', True, lightgreen)
    round_rect((menux+spacing, menuy+yspacing*5), b1, b2, green)
    frame.blit(controlsButton, (menux+spacing,menuy+yspacing*5))
    frame.blit(c, (keyx,menuy+yspacing*5))

    # pouch button
    pouchButton = main_btn_font.render(' View Treasures', True, lightgreen)
    t = main_btn_font.render('[t]', True, lightgreen)
    round_rect((menux+spacing, menuy+yspacing*7), b1, b2, green)
    frame.blit(pouchButton, (menux+spacing,menuy+yspacing*7))
    frame.blit(t, (keyx,menuy+yspacing*7))

    # high score button
    highScoreButton = main_btn_font.render(" High Score", True, lightgreen)
    s = main_btn_font.render('[s]', True, lightgreen)
    round_rect((menux+spacing, menuy+yspacing*9), b1, b2, green)
    frame.blit(highScoreButton, (menux+spacing,menuy+yspacing*9))
    frame.blit(s, (keyx, menuy+yspacing*9))

    # credits button
    creditButton = main_btn_font.render(" Credits", True, lightgreen)
    d = main_btn_font.render('[d]', True, lightgreen)
    round_rect((menux+spacing, menuy+yspacing*11), b1, b2, green)
    frame.blit(creditButton, (menux+spacing,menuy+yspacing*11))
    frame.blit(d, (keyx, menuy+yspacing*11))

    # quit button
    quitButton = main_btn_font.render(" Quit", True, lightgreen)
    q = main_btn_font.render('[q]', True, lightgreen)
    round_rect((menux+spacing, menuy+yspacing*13), b1, b2, green)
    frame.blit(quitButton, (menux+spacing,menuy+yspacing*13))
    frame.blit(q, (keyx, menuy+yspacing*13))



class Item():
    def __init__(self, pos, id):
        self.posx = pos[0]
        self.posy = pos[1]
        self.pos  = (pos[0], pos[1])
        self.id = id
        self.value = 0
        self.type = ''
        self.image = barber

    def get_image(self):
        for key in image_pairs:
            if key == self.id:
                self.image = image_pairs[key]

    def get_value(self):
        for key in values:
            if key == self.id:
                self.value = values[key]

    def get_type(self):
        pass

    def get_center(self):
        w = (self.posx + item_image_size[0]) / 2
        h = (self.posy + item_image_size[1]) / 2
        self.pos = (w, h)
        return (self.pos)

    def draw(self):
        pygame.draw.circle(frame, white, (self.pos), 5)


def createItems():
    global item_list, items, item_locs
    item_list = []
    items = []
    item_locs = []
    while len(items) < num_items:
        choice = random.choice(allItems)
        posx = random.randrange(25, WIDTH-25)
        posy = random.randrange(25, HEIGHT-25)
        new = Item((posx, posy), choice)
        new.get_image()
        items.append(new)
        item_locs.append((posx, posy))


def credits():
    aMenu = True
    creditsOpen = True
    tx = large_menu_window[0]
    ty = large_menu_window[1]
    tw = large_menu_window[2]
    th = large_menu_window[3]
    round_rect((tx, ty), tw, th, lightgreen)
    round_rect((back_button[0], back_button[1]), back_button[2], back_button[3], green)
    goBack = back_btn_font.render('<< Go Back [tab]', True, lightgreen)
    credits = title_font.render('Credits', True, darkgreen)
    game = font.render('All game design, code, and graphics by Nichola Holcomb', True, darkgreen)
    photo = font.render('All photos used in game taken by Nichola Holcomb ', True, darkgreen)
    expt1 = font.render('Exception: GW button photo taken by Stef Tanguay', True, darkgreen)
    finds = font.render('All items in game were found metal detecting by Nichola Holcomb (NH) and Stef Tanguay (ST)', True, darkgreen)
    expt2 = font.render("Exceptions (items listed below are replicas):", True, darkgreen)
    expt2a = font.render("Pine tree shilling (Nichola's)", True, darkgreen)
    expt2b = font.render("Fugio (Stef's)", True, darkgreen)
    expt2c = font.render("Silver pull tab (made by Warren [Rockcycle] Kruger for Stef)", True, darkgreen)
    credFinds = font.render("Credits for specific items below:", True, darkgreen)
    nh1 = font.render('NH: tombac button, ox knob, skeleton key, rusty nail, barber quarter, musket ball,', True, darkgreen)
    nh2 = font.render('shoe buckle, crotal bell, harmonica reed, jaw harp, thimble', True, darkgreen)
    st = font.render('ST: dandy button, 2 real, two tine fork, george washington (GW) button, walking half dollar', True, darkgreen)
    frame.blit(goBack, (120, 115))
    frame.blit(credits, (380, 120))
    frame.blit(game, (120, 200))
    frame.blit(photo, (120, 230))
    frame.blit(expt1, (180, 260))
    frame.blit(finds, (120, 290))
    frame.blit(expt2, (180, 320))
    frame.blit(expt2a, (240, 350))
    frame.blit(expt2b, (240, 380))
    frame.blit(expt2c, (240, 410))
    frame.blit(credFinds, (120, 460))
    frame.blit(nh1, (120, 500))
    frame.blit(nh2, (180, 530))
    frame.blit(st, (120, 570))


def controlsMenu():
    tx = large_menu_window[0]
    ty = large_menu_window[1]
    tw = large_menu_window[2]
    th = large_menu_window[3]
    newLine = 0
    aMenu = True
    round_rect((tx, ty), tw, th, lightgreen)
    round_rect((back_button[0], back_button[1]), back_button[2], back_button[3], green)
    controls = title_font.render("Controls", True, darkgreen)
    goBack = back_btn_font.render('<< Go Back [tab]', True, lightgreen)
    moveChar = sm_menu_font.render('Use arrow keys to move character', True, darkgreen)
    openMenu = sm_menu_font.render('Hit "M" to reopen menu and pause game', True, darkgreen)
    dig = sm_menu_font.render('Hit "Space" to dig when you hear a signal', True, darkgreen)
    howTo = sm_menu_font.render('HOW TO WIN:', True, darkgreen)
    win1 = sm_menu_font.render('Discover at least 50% of treasures, enemy finds included', True, darkgreen)
    win2 = sm_menu_font.render('Defeat enemy detectorist by having higher score at end of game', True, darkgreen)
    save = sm_menu_font.render("Don't forget to save your game if you want to keep your high score!", True, darkgreen)
    saving = sm_menu_font.render('You can only save your score if you win.', True, darkgreen)
    frame.blit(goBack, (120, 115))
    frame.blit(controls, (380, 120))
    frame.blit(moveChar, (300, 200))
    frame.blit(openMenu, (280, 230))
    frame.blit(dig, (275, 260))
    frame.blit(howTo, (380, 350))
    frame.blit(win1, (200, 380))
    frame.blit(win2, (160, 410))
    frame.blit(save, (150, 440))
    frame.blit(saving, (270, 470))

def treasuresPouch():
    global finds_pouch
    aMenu = True
    menuh = HEIGHT/2
    menuw = WIDTH/2
    x = 100
    y = 150
    tx = large_menu_window[0]
    ty = large_menu_window[1]
    tw = large_menu_window[2]
    th = large_menu_window[3]

    round_rect((tx, ty), tw, th, lightgreen)
    round_rect((back_button[0], back_button[1]), back_button[2], back_button[3], green)
    goBack = back_btn_font.render('<< Go Back [tab]', True, lightgreen)
    treasures = title_font.render('Treasures Pouch', True, darkgreen)
    frame.blit(goBack, (120, 115))
    frame.blit(treasures, (350, 120))

    for find in finds_pouch:
        img = find.image
        img = pygame.transform.scale(img,(100,100))
        frame.blit(img, (x,y))
        x += 100
        if x > 700:
            x = 100
            y += 100


def readHighScores():
    with open('highscores.txt', 'r') as f:
        for line in f:
            highScores.append(line)


def saveHighScore(name):
    global highScores

    if len(str(player1.score)) == 1:
        newScore = name + ': 00' + str(player1.score) + '\n'
    elif len(str(player1.score)) == 2:
            newScore = name + ': 0' + str(player1.score) + '\n'
    else:
        newScore = name + ': ' + str(player1.score) + '\n'
    # if player1.score != 0:
    if len(highScores) < 10:
        highScores.append(newScore)
    elif len(highScores) == 10:
        highScores.pop(0)
        highScores.append(newScore)
    highScores.sort(key = lambda x: x.split(' ')[1])
    with open('highscores.txt', 'w') as f:
        for score in highScores:
            score = str(score)
            f.write(score)


def highScore():
    global username
    pouch = [100, 100, WIDTH-200, HEIGHT-200]
    button = [110, 110, 160, 40]
    tx = large_menu_window[0]
    ty = large_menu_window[1]
    tw = large_menu_window[2]
    th = large_menu_window[3]

    highScore = title_font.render("High Scores", True, darkgreen)
    goBack = back_btn_font.render('<< Go Back [tab]', True, lightgreen)

    round_rect((tx, ty), tw, th, lightgreen)
    round_rect((back_button[0], back_button[1]), back_button[2], back_button[3], green)
    frame.blit(highScore, (350, 120))
    frame.blit(goBack, (120, 115))

    # save high score button
    noteFont = pygame.font.Font('freesansbold.ttf',15)
    toSave = sm_menu_font.render("Enter 'Name' and hit ENTER to save high score", True, darkgreen)
    note1 = font.render("Note: saving will reset the game.", True, darkgreen)
    note2 = font.render("Note: Saving only available if you win.", True, darkgreen)
    save = sm_menu_font.render("Save", True, black)

    pygame.draw.line(frame, black, (350, 630), (520, 630))
    round_rect((390, 650), 85, 25, green)
    frame.blit(toSave, (250, 540))
    frame.blit(note1, (340, 560))
    frame.blit(note2, (320, 580))
    frame.blit(save, (410, 655))

    # display name as typed by user
    name = sm_menu_font.render(username, True, black)
    frame.blit(name, (400, 610))

    x = 400
    y = 200
    for score in highScores:
        hScore = sm_menu_font.render(str(score), True, black)
        frame.blit(hScore, (x, y))
        y += 30

def canWin(pScore, eScore):
    if len(item_locs_found) >= num_items*.5:
        if pScore > eScore:
            return True
        else:
            return False

def noSave():
    noSave = font.render('test', True, black)
    frame.blit(noSave, (100, 300))

# draw game background and menus
def draw():
    global treasuresOpen, menuOpen
    frame.blit(background_image, (0,0))
    if menuOpen == True:
        treasuresOpen = False
        mainMenu()
    if treasuresOpen == True:
        menuOpen = False
        treasuresPouch()
    if highScoresOpen == True:
        menuOpen = False
        highScore()
    if controlsOpen == True:
        menuOpen = False
        controlsMenu()
    if creditsOpen == True:
        credits()


# show player score
def showScore():
    pscore = score_font.render('Score: ' + str(player1.score), True, black)
    frame.blit(pscore, (750, 10))
    escore = score_font.render('Score: ' + str(enemy1.score), True, black)
    frame.blit(escore, (20, 10))

# draw plug after digging
def drawPlug(pos, plug):
    frame.blit(plug, pos)


class Player():
    global playerImg, currentPos, item_locs_found, score
    def __init__(self, pos, image):
        self.posx = pos[0]
        self.posy = pos[1]
        self.pos = (self.posx, self.posy)
        self.image = playerImg
        self.vel = 2
        # self.rect = self.image.get_rect()
        self.orientation = 'right'
        self.score = 0

    def draw(self, pos):
        if self.orientation == 'right':
            self.image = playerImg
            frame.blit(self.image, self.pos)
        elif self.orientation == 'left':
            self.image = player_left
            frame.blit(self.image, self.pos)
        elif self.orientation == 'up':
            self.image = player_down
            frame.blit(self.image,  self.pos)
        elif self.orientation == 'down':
            self.image = player_up
            frame.blit(self.image,  self.pos)

    def update(self, pos):
        self.pos = pos

    # check if player is walking over hidden item
    def isCollision(self, other):
        # offset to account for player image size (pos uses top left corner of image)
        #dist = math.sqrt((x1 - x)**2 + ((y1 - y)**2))
        dist = math.sqrt((self.pos[0]+50 - other.pos[0])**2 + ((self.pos[1]+50 - other.pos[1])**2))
        if other.pos not in item_locs_found:
            if dist < 15:
                return True
            else:
                return False

    # dig item and add to pouch
    def dig(self, item):
        if item.pos not in item_locs_found:
            finds_pouch.append(item)
            item_locs_found.append(item.pos)
            self.score += item.value

    # show dug item decription and image when dug
    def showDug(self, itemName, image):
        font = pygame.font.Font('freesansbold.ttf', 20)
        display = font.render("You dug a " + str(itemName), True, black)
        frame.blit(display, (100, 50))
        frame.blit(image, (120, 70))


class Enemy(Player):
    def __init__(self, pos, image):
        self.pos = pos
        self.image = image
        self.vel = 1
        self.orientation = 'E'
        self.score = 0

    def draw(self, pos, image):
        if self.orientation == 'NE' or self.orientation == 'E' or self.orientation == 'SE':
            self.image = enemy_right
        if self.orientation == 'NW' or self.orientation == 'W' or self.orientation == 'SW':
            self.image = enemy_left
        elif self.orientation == 'N':
            self.image = enemy_up
        elif self.orientation == 'S':
            self.image = enemy_down
        frame.blit(image, pos)

    def update(self, pos):
        self.pos = pos

    def move(self, pos):
        global enx, eny, enmovex, enmovey

        if self.orientation == 'E':
            enmovex = enemy1.vel
            enmovey = 0
        if self.orientation == 'W':
            enmovex = -enemy1.vel
            enmovey = 0
        if self.orientation == 'N':
            enmovex = 0
            enmovey = -enemy1.vel
        if self.orientation == 'S':
            enmovex = 0
            enmovey = enemy1.vel
        if self.orientation == 'NE':
            enmovex = enemy1.vel
            enmovey = -enemy1.vel
        if self.orientation == 'SE':
            enmovex = enemy1.vel
            enmovey = enemy1.vel
        if self.orientation == 'SW':
            enmovex = -enemy1.vel
            enmovey = enemy1.vel
        if self.orientation == 'NW':
            enmovex = -enemy1.vel
            enmovey = -enemy1.vel
        enx += enmovex
        eny += enmovey


    def change_orientation(self, bool):
        dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        if bool == True:
            d = self.orientation

            if self.pos[0] <= 1 or self.pos[0] >= WIDTH-51:
                if d == 'E' or d == 'NE' or d == 'SE':
                    dirs.remove('E')
                    dirs.remove('NE')
                    dirs.remove('SE')
                    dirs.remove('N')
                    dirs.remove('S')
                elif d == 'W' or d == 'NW' or d == 'SW':
                    dirs.remove('W')
                    dirs.remove('NW')
                    dirs.remove('SW')
                    dirs.remove('N')
                    dirs.remove('S')
            if self.pos[1] <= 1 or self.pos[1] >= HEIGHT-101:
                if d == 'N' or d == 'NW' or d == 'NE':
                    dirs.remove('N')
                    dirs.remove('NW')
                    dirs.remove('NE')
                    dirs.remove('E')
                    dirs.remove('W')
                elif d == 'S' or d == 'SW' or d == 'SE':
                    dirs.remove('S')
                    dirs.remove('SE')
                    dirs.remove('SW')
                    dirs.remove('E')
                    dirs.remove('W')

        new = random.choice(dirs)
        self.orientation = new

    def isCollision(self, other):
        # offset to account for player image size (pos uses top left corner of image)
        #dist = math.sqrt((x1 - x)**2 + ((y1 - y)**2))
        dist = math.sqrt((self.pos[0]+50 - other.pos[0])**2 + ((self.pos[1]+50 - other.pos[1])**2))
        if other.pos not in item_locs_found:
            if dist < 10:
                return True
            else:
                return False

    # dig item and add to pouch
    def dig(self, item):
        if item.pos not in item_locs_found:
            item_locs_found.append(item.pos)
            self.score += item.value


    def showDug(self, itemName, image):
        font = pygame.font.Font('freesansbold.ttf', 20)
        display = font.render("You dug a " + str(itemName), True, black)
        frame.blit(display, (100, 50))
        frame.blit(image, (300, 50))
        enemySteps = 0
        num_steps = [5, 10, 15, 20, 30, 40]
        rand_steps = random.choice(num_steps)



# create player
player_start_pos = (0,500)
player1 = Player(player_start_pos, playerImg)

# create enemy
enemy_start_pos = (50,50)
enemy1 = Enemy(enemy_start_pos, enemy_right)

highScores.sort(key = lambda x: x.split(' ')[1])
newGame()


# Game Loop
def gameLoop():
    global menuOpen, controlsOpen, treasuresOpen, highScoresOpen, creditsOpen, inPlay, digIt, playerDigs, recentDig, recentItem, recentImage, username, WIDTH, HEIGHT
    global enx, eny, enmovex, enmovey, newgame, aMenu

    quitGame = False
    canSave = False
    newgame = True
    playerx = player1.pos[0]
    playery = player1.pos[1]
    movex = 0
    movey = 0
    enx = enemy1.pos[0]
    eny = enemy1.pos[1]
    enmovex = 0
    enmovey = 0
    hitx = 0
    hity = 0
    count_moves = 0

    if newgame == True:
        readHighScores()

    while not quitGame:

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        keypress = pygame.key.get_pressed()

        frame.fill(white)
        draw()
        showScore()


        if aMenu != True:
        # if menuOpen != True and treasuresOpen != True and highScoresOpen != True and controlsOpen != True:
            player1.draw(player_start_pos)

        player1.update((playerx,playery))

        if len(item_locs_found) == num_items:
            endGame()

        # event handling
        for event in pygame.event.get():

            # quits and closes game when user hits window X
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        # ********* MENU ***********
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                abc = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'
                canSave = canWin(player1.score, enemy1.score)

                if key == 'm':
                    menuOpen = True

                if menuOpen == False and controlsOpen == False and treasuresOpen == False and highScoresOpen == False:
                    newgame = False

                if menuOpen == True:
                    inPlay = False
                    aMenu = True
                    if newgame == True:
                        if key == 'n':
                            newGame()
                            inPlay = True
                            aMenu = False
                            menuOpen = False
                            highScoresOpen = False
                            controlsOpen = False
                            treasuresOpen = False
                            creditsOpen = False
                    if newgame == False:
                        if key == 'r':
                            inPlay = True
                            aMenu = False
                            menuOpen = False
                            highScoresOpen = False
                            controlsOpen = False
                            treasuresOpen = False
                            creditsOpen = False
                        if key == 'n':
                            newgame = True
                            aMenu = False
                            newGame()
                            inPlay = True
                            menuOpen = False
                            highScoresOpen = False
                            controlsOpen = False
                            treasuresOpen = False
                            creditsOpen = False
                    if key == 'c':
                        controlsOpen = True
                        menuOpen = False
                        highScoresOpen = False
                        treasuresOpen = False
                        creditsOpen = False
                    elif key == 't':
                        treasuresOpen = True
                        menuOpen = False
                        highScoresOpen = False
                        controlsOpen = False
                        creditsOpen = False
                    elif key == 's':
                        highScoresOpen = True
                        menuOpen = False
                        treasuresOpen = False
                        controlsOpen = False
                        creditsOpen = False
                    elif key == 'd':
                        creditsOpen = True
                        highScoresOpen = False
                        menuOpen = False
                        treasuresOpen = False
                        controlsOpen = False
                    elif key == 'q':
                        pygame.quit()
                        quit()


                if highScoresOpen == True:
                    if canSave == True:
                        if key in abc:
                            username += key
                        elif key == 'backspace':
                            username = username [:-1]
                        elif key == 'return':
                            saveHighScore(username)
                            newgame = True
                            newGame()

                if treasuresOpen == True or highScoresOpen == True or controlsOpen == True or creditsOpen == True:
                    if key == 'tab':
                        menuOpen = True
                        highScoresOpen = False
                        treasuresOpen = False
                        controlsOpen = False
                        creditsOpen = False

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     # close menu, play game
            #     if newgame == True:
            #         if mouse[0] > menux+spacing and mouse[0] < menux+spacing+menu_button_size[0]:
            #             if mouse[1] > menuy+yspacing*3 and mouse[1] < menuy+yspacing*3+menu_button_size[1]+10:
            #                 if click[0] == 0:
            #                     menuOpen = False
            #                     inPlay = True
            #                     newgame = False
            #     if newgame == False:
            #         # resume
            #         if mouse[0] > menux and mouse[0] < menux+spacing+sm_button_size[0]:
            #             if mouse[1] > menuy+yspacing*3 and mouse[1] < menuy+yspacing*3+sm_button_size[1]:
            #                 if click[0] == 0:
            #                     menuOpen = False
            #                     inPlay = True
            #         # restart
            #         if mouse[0] > menux+spacing+sm_button_size[0] and mouse[0] < menux+spacing+menu_button_size[0]:
            #             if mouse[1] > menuy+yspacing*3 and mouse[1] < menuy+yspacing*3+sm_button_size[1]:
            #                 if click[0] == 0:
            #                     menuOpen = False
            #                     inPlay = True
            #
            #     # open controls
            #     if mouse[0] > menux+spacing and mouse[0] < menux+spacing+menu_button_size[0]:
            #         if mouse[1] > menuy+yspacing*5 and mouse[1] < menuy+yspacing*5+menu_button_size[1]+10:
            #             if click[0] == 0:
            #                 controlsOpen = True
            #                 menuOpen = False
            #
            #     # open treasures pouch
            #     if mouse[0] > menux+spacing and mouse[0] < menux+spacing+menu_button_size[0]:
            #         if mouse[1] > menuy+yspacing*7 and mouse[1] < menuy+yspacing*7+menu_button_size[1]+10:
            #             if click[0] == 0:
            #                 treasuresOpen = True
            #                 menuOpen = False
            #
            #     # open high score
            #     if mouse[0] > menux+spacing and mouse[0] < menux+spacing+menu_button_size[0]:
            #         if mouse[1] > menuy+yspacing*9 and mouse[1] < menuy+yspacing*9+menu_button_size[1]+10:
            #             if click[0] == 0:
            #                 highScoresOpen = True
            #                 menuOpen = False
            #
            #     # quit game
            #     if mouse[0] > menux+spacing and mouse[0] < menux+spacing+menu_button_size[0]:
            #         if mouse[1] > menuy+yspacing*11 and mouse[1] < menuy+yspacing*11+menu_button_size[1]+10:
            #             if click[0] == 0:
            #                 pygame.quit()
            #                 quit()


            # if highScoresOpen == True:
            #     if mouse[0] > 390 and mouse[0] < 475:
            #         if mouse[1] > 650 and mouse[1] < 690:
            #             canSave = canWin(player1.score, enemy1.score)
            #             if canSave == True:
            #                 saveHighScore(username)

            # from other screen, return to main menu
            # if treasuresOpen == True or highScoresOpen == True or controlsOpen == True:
            #         if mouse[0] > 110 and mouse[0] < 240:
            #             if mouse[1] > 110 and mouse[1] < 150:
            #                 treasuresOpen = False
            #                 highScoresOpen = False
            #                 controlsOpen = False
            #                 menuOpen = True


        # ****** END OF MENU *******


        # ***** MAIN GAME LOOP *****
            # if inPlay == True:

            # player movement
                if inPlay == True:
                    recentDig = False
                    # key = pygame.key.name(event.key)
                    x = player1.pos[0]
                    y = player1.pos[1]
                    if key == 'left':
                        player1.orientation = 'left'
                        movex = -player1.vel
                    elif key == 'right':
                        movex = player1.vel
                        player1.orientation = 'right'
                    elif key == 'up':
                        player1.orientation = 'up'
                        movey -= player1.vel
                    elif key == 'down':
                        player1.orientation = 'down'
                        movey += player1.vel
                    elif key == 'space':
                            playerDigs = True

            if event.type == pygame.KEYUP:
                movex = 0
                movey = 0
                playerDigs = False

        # ***** END OF EVENT HANDLING *****


        playerx += movex
        playery += movey
        enemy1.move((enx, eny))


        # enemy movement
        if enx == WIDTH-50 or enx == 0:
            enemy1.change_orientation(True)

        elif eny == 0 or eny == HEIGHT-100:
            enemy1.change_orientation(True)


        enemy1.update((enx, eny))
        if menuOpen != True and treasuresOpen != True and highScoresOpen != True and controlsOpen != True:
            enemy1.draw((enx, eny), enemy1.image)

        if menuOpen == True or treasuresOpen == True or highScoresOpen == True:
            enemy1.vel = 0
        else:
            enemy1.vel = 1


        # check for collisions with items
        for i in items:
            # i.draw()

            if player1.isCollision(i):
                if i.pos not in item_locs_found:
                    player_beep.play()
                    dig = True
                    if dig == True:
                        if playerDigs == True:
                            player1.dig(i)
                            newPlug = player1.dig(i)
                            recentDig = True
                            recentItem = i.id
                            recentImage = i.image

            if enemy1.isCollision(i):
                if i.pos not in item_locs_found:
                    enemy1.dig(i)
                    newPlug = enemy1.dig(i)
                enemy1.change_orientation(False)
            else:
                dig = False

            if i.pos in item_locs_found:
                if menuOpen != True and treasuresOpen != True and highScoresOpen != True and controlsOpen != True and inPlay == True:
                    drawPlug(i.pos, plug)


        if recentDig == True:
            if menuOpen != True and treasuresOpen != True and controlsOpen != True and highScoresOpen != True:
                player1.showDug(recentItem, recentImage)



        pygame.display.update()
        clock.tick(60)

    # end of gameLoop


gameLoop()
pygame.quit()
quit()
