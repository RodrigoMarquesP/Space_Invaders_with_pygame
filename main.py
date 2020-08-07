# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 08:50:35 2020.

@author: sucod

Ship icon made by Nhor Phai from www.flaticon.com
Meteor icon made by Freepik from www.flaticon.com
Bullet icon made by Smashicons from www.flaticon.com
Shield icons made by Freepik from www.flaticon.com
Medal icon made by Freepik from www.flaticon.com
Bomb icon made by smalllikeart from www.flaticon.com

"""
import pygame
import numpy as np

# setting the variables to oscilate the color
c = (56, 40, 92)  # purplesky
samp = 500  # number of color samples
# the vectors will gradually lead to the desired color
r = np.linspace(0, c[0], samp, dtype='int8')  # red vector
g = np.linspace(0, c[1], samp, dtype='int8')  # green vector
b = np.linspace(0, c[2], samp, dtype='int8')  # blue vector
i = 0  # position on the vectors
up = bool()  # bool that indicates if the color is increasing or decreasing


def rgb_oscilator():
    """

    Return the next color in the sequence.

    Using global variables as guides,
    it returns the next set of rgb colors
    in the sequence, making a only color
    oscilate from black to the color itselt.

    Returns
    -------
    (r[i], g[i], b[i]) : tuple
        set of RGB color.

    """
    global i
    global up

    if i == 0:
        up = True
    if i == samp-1:
        up = False

    if up:
        i += 1
    else:
        i -= 1

    return (r[i], g[i], b[i])


# initializing the module and mixer
# the 8000 Hz is a choice, to make the sounds looks like 'old school'
# the 16 bits is a requirement of pygame module
# number of channel was set as 25 to never saturate
# buffer size was set to 64 to give almost no delay on sound reproduction
pygame.mixer.pre_init(8000, -16, 25, 64)  # Hz, bits/sample, channels, buffer
pygame.init()
pygame.mixer.init(8000, -16)  # Frequency[Hz], bits/sample

# creating a screen for the game with 800 for 600 pixels
s = (800, 600)  # (x, y) beginning from top left (in pixels)
# creating a surface object
screen = pygame.display.set_mode((s), pygame.DOUBLEBUF | pygame.HWSURFACE, 32)
# the parameter pygame.HWSURFACE creates a hardware surface,
# what is created using the video card, it was use to acelerate.

# the parameter pygame.DOUBLEBUF acelerate the game:
# it creates two hardware surfaces, but displays just once
# at a time, so, every frame, the program doesn't need to
# generate a new surface, since its already generated.

# title, icon and game over sound
pygame.display.set_caption('Space Invaders')  # display the name of the window
icon = pygame.image.load('icons/icon.png')  # load the icon of the window
pygame.display.set_icon(icon)  # display the icon of the window
game_oversound = pygame.mixer.Sound('sounds/game_over.wav')

# main theme
# list all sounds
game_tracks = ['sounds/French 79 - Hometown.mp3',
               'sounds/Kid Francescoli - Moon.mp3',
               'sounds/Aaron Smith - Dancin.mp3',
               'sounds/Midnight City.mp3',
               'sounds/Pumped Up Kicks.mp3',
               'sounds/Take On Me.mp3',
               'sounds/What You Know.mp3']
np.random.shuffle(game_tracks)  # shuffle the list
music_counter = 0  # count the musics beginning at zero
pygame.mixer.music.set_volume(0.6)  # reducing the background  music volume
pygame.mixer.music.load(game_tracks[music_counter])  # load it
pygame.mixer.music.play()  # play it

# player
# choose one between the 8 ship colors
chosen_ship = 'icons/battleship/' + str(np.random.choice(range(1, 9))) + '.png'
playerimg = pygame.image.load(chosen_ship)  # load the image
playerx = s[0]*0.45  # set X initial position
playery = s[1]*0.83  # set Y initial position
playerx_change = 0.0  # the actual velocity (stars at zero=no key pressed)
std_player_vel = 0.8  # the standart velocity of the player when moving
player_vel = std_player_vel  # initialy the velocity is the standart
hitsound = pygame.mixer.Sound('sounds/playerhit.wav')

# window stars
starimg = pygame.image.load('icons/star_dot.png')
n_stars = 80  # stars drawn at screen at the same time
starx = np.random.randint(0, s[0]/2, n_stars) * 2.  # initial x locations
stary = np.random.randint(0, s[1]/2, n_stars) * 2.  # initial y locations
std_star_vel = 0.5
star_vel = std_star_vel

# window meteors
meteorimg = pygame.image.load('icons/asteroid.png')
n_meteors = 3  # meteors on screen simultaneously
step = -250  # y distance between meteors
angle = 0  # angle variable for the meteors rotation
meteorx = np.random.randint(0, s[0]/64, n_meteors) * 64.  # initial x loc
meteory = np.arange(0, n_meteors*step, step, dtype='float64')  # initial y loc
std_meteor_vel = 0.4
meteor_vel = std_meteor_vel

# enemies
enemyimg = pygame.image.load('icons/enemy.png')
enemyy_decay = 80  # pixels that enemies decay each time they reach boundaries
std_enemy_vel = 0.8
enemy_vel = std_enemy_vel
enemies = []  # list of actual enemies
spawn_counter = 0  # comput how much iterations have been since last spawn
std_spawn_rate = 1800  # set how much iterations are between each spawn
spawn_rate = std_spawn_rate

# enemy bullets
enemy_bullets = []  # list of all enemy bullets
std_enemy_bullet_vel = 1  # standart velocity of the enemy bullets
enemy_bullet_vel = std_enemy_bullet_vel
enemy_bullettimg = pygame.image.load('icons/enemy_bullet.png')
std_shoot_rate = 900  # standart rate (in iterations) of each enemy shoots
shoot_rate = std_shoot_rate
enemyshoot_sound = pygame.mixer.Sound('sounds/enemyshoot.wav')

# bullet
bulletimg = pygame.image.load('icons/bullet.png')
std_bullet_vel = 1
bullet_vel = std_bullet_vel
bullets = []  # list of all bullets still on screen
playershoot_sound = pygame.mixer.Sound('sounds/playershoot.wav')

# heat status
baseimg = pygame.image.load('icons/heat_bar_base.png')  # background
heatimg = pygame.image.load('icons/heat_bar.png')  # heat bar itself
markerimg = pygame.image.load('icons/marker.png')  # middle marker
fire = False  # sinalizes that a shoot was performed
heat = 0  # initial heat
std_cool_rate = 0.08  # standart rate of cooling the player gun
cool_rate = std_cool_rate
allow_fire = True  # flag of the heat block of the gun

# life
shieldimg = pygame.image.load('icons/shield.png')
shields_remaining = 3  # number of shields (starts at 3)

# explosion
blast_sound = pygame.mixer.Sound('sounds/explosion.wav')
blasts = []  # list of each explosions happening
# sequence of images of the explosion
explode = [pygame.image.load('icons/Boom/1.png'),
           pygame.image.load('icons/Boom/2.png'),
           pygame.image.load('icons/Boom/3.png'),
           pygame.image.load('icons/Boom/4.png'),
           pygame.image.load('icons/Boom/5.png'),
           pygame.image.load('icons/Boom/6.png'),
           pygame.image.load('icons/Boom/7.png')]

# collectables
collec_delay = 5000  # rate of the collectables appearing
collec_counter = 0  # counter of iterations to spawn or not a collectable
collec = []  # caracteristics of the actual collec [witch_one, x, y]
std_collec_vel = 0.8
collec_vel = std_collec_vel
# each image and song for the 4 collectables
collec_shieldimg = pygame.image.load('icons/collectable_shield.png')
shield_sound = pygame.mixer.Sound('sounds/shield.wav')
collec_speedimg = pygame.image.load('icons/collectable_speed.png')
speed_sound = pygame.mixer.Sound('sounds/speed.wav')
collec_medalimg = pygame.image.load('icons/collectable_medal.png')
medal_sound = pygame.mixer.Sound('sounds/medal.wav')
collec_bombimg = pygame.image.load('icons/collectable_bomb.png')
bomb_sound = pygame.mixer.Sound('sounds/kabum.wav')
# list of the images to access with collecs[collec[0]]
collecs = [collec_shieldimg,
           collec_speedimg,
           collec_medalimg,
           collec_bombimg]

# the speed collectable increases dificulty
dificulty_multiplier = 1.2  # initial multiplier of every speed
add_dificulty_rate = 0.3  # rate of speed increasing by the speed collectable
"""Increasing the dificulty, increases: player velocity, enemies velocity,
bullets velocity, meteors velocity, stars velocity, collectables velocity
and the cooling rate of the player gun. Beyond this, it decreases the
shooting delay of the enemies and their spawn rate."""

# score
score = 0  # initial score
font = pygame.font.Font('Pokemon GB.ttf', 32)

# lower font
font2 = pygame.font.Font('Pokemon GB.ttf', 16)

# end game
endimg = pygame.image.load('icons/game_over.png')


def meteor():
    """
    Place passing meteors on screen.

    To rotate the meteor we get the center of the image
    and set it to rotated image, then, we move it to
    the (meteorx, meteory) position, manipulating the
    rectangle.
    Another important thing is to always rotate the original
    image, so it doesn't lose quality each rotation.

    Returns
    -------
    None.

    """
    global meteorx, meteory
    for i in range(0, n_meteors):
        if meteory[i] >= s[1]:  # each time a meteor goes out of screen
            meteory[i] = -64  # replace the new one just up the top
            meteorx[i] = np.random.randint(0, s[0]/64) * 64  # new x loc
        # generate the rotation by correcting the center of the image
        center = meteorimg.get_rect().center  # get the previous center
        image = pygame.transform.rotate(meteorimg, angle*(i+1))  # rotate
        new_rect = image.get_rect(center=center)  # apply the old center
        new_rect = new_rect.move(meteorx[i], meteory[i])  # move the rectangle
        # draw the actual image conserving the center and moving the rectangle
        screen.blit(image, new_rect)


def stars():
    """
    Place passing stars on screen.

    Returns
    -------
    None.
    """
    for i in range(0, n_stars):
        screen.blit(starimg, (starx[i], stary[i]))
        if stary[i] >= s[1]:  # each star that cross the bottom boundary
            stary[i] = 0  # replace at the top
            starx[i] = np.random.randint(0, s[0]/2) * 2  # new x loc


def player(x, y):
    """
    Set the position of the player on the screen.

    Parameters
    ----------
    x : float
        pixel position on x axis (left to right).
    y : float
        pixel position on y axis (top to bottom).

    Returns
    -------
    None.

    """
    screen.blit(playerimg, (x, y))


def add_enemy():
    """
    Add a new enemy on the screen.

    Returns
    -------
    None.

    """
    enemyx = np.random.randint(1, s[0]/2 - 65) * 2.  # spawn out the borders
    enemies.append([enemyx, 0, enemy_vel, 0])  # [x, y, velocity, shoot_count]


def enemies_update():
    """
    Set the position of the enemy on the screen.

    Returns
    -------
    None.

    """
    global enemies, shoot_rate
    for index, coords in enumerate(enemies):
        screen.blit(enemyimg, (coords[0], coords[1]))
        coords[0] += coords[2]  # move each enemy in x
        if coords[0] <= 0 or coords[0] >= s[0]-64:  # reaching the boundaries
            coords[2] *= -1  # invert movement
            coords[1] += enemyy_decay  # get the enemy a little down on window
        coords[3] += 1  # add to the counter
        if coords[3] >= shoot_rate:  # reaching the shoot_rate, it shoots
            coords[3] = 0  # resteart the counter
            enemyshoot_sound.play()
            enemy_bullets.append([coords[0] + 32, coords[1] + 60])


def enemy_bullets_update(px, py):
    """
    Update the bullet shooted by the enemies.

    Parameters
    ----------
    px : float
        x position of the player.
    py : float
        y position of the player.

    Returns
    -------
    None.

    """
    global enemy_bullets, shields_remaining
    for i, coords in enumerate(enemy_bullets):
        screen.blit(enemy_bullettimg, (coords[0], coords[1]))
        coords[1] += enemy_bullet_vel  # moving the bullet
        if coords[1] == s[1]+32:  # +32 to the full disappear of the bullet
            enemy_bullets.pop(i)  # clean the bullet
        # we set a point to assume collision
        hit_dot = (coords[0], coords[1] + 5)
        if (px < hit_dot[0] < px+64) and (py < hit_dot[1] < py+64):
            hitsound.play()
            # at a collision, we delete the enemy bullet and add a blast
            enemy_bullets.pop(i)
            blasts.append([px, py, 0])
            shields_remaining -= 1  # destroy the ship shields


def fire_bullet():
    """
    Add a new bullet.

    Returns
    -------
    None.

    """
    bullets.append([playerx + 25, playery])


def bullets_update():
    """
    Update each ballet state.

    Move bullet up,
    Delete bullets that reach top boundarie,

    Returns
    -------
    None.

    """
    global bullets, enemies, score
    for index, coords in enumerate(bullets):
        screen.blit(bulletimg, (coords[0], coords[1]))
        coords[1] -= bullet_vel  # moving the bullet
        if coords[1] == 0-32:  # -32 to the full disappear of the bullet
            bullets.pop(index)  # put off the bullet
        # we set a point to assume collision
        hit_dot = (coords[0] + 7, coords[1] + 16)
        for i, c in enumerate(enemies):
            if (c[0] < hit_dot[0] < c[0]+64) and (c[1] < hit_dot[1] < c[1]+64):
                # each hit, delete the bullet and the enemy and add a blast
                blast_sound.play()
                bullets.pop(index)
                enemies.pop(i)
                score += 10  # score for each enemy down
                blasts.append([hit_dot[0], hit_dot[1], 0])  # [x, y, counter]


def heat_status():
    """

    Refresh the heat status of the ship guns.

    195 pixels == 100%

    Returns
    -------
    None.

    """
    global heat, fire, allow_fire
    if fire:  # each shoot
        heat += 40  # heat 40%
    heat_width = 195*(heat/100)  # percentage of the 195 pixels width bar
    # we use a third parameter to show just a part of the area
    # (Xo, Yo, Xf, Yf), draw the area at Xo to Xf and Yo to Yf
    screen.blit(heatimg, (597.5, 577), (0, 0, heat_width, 16))
    if heat >= 0.5:  # just if it's still hot
        heat -= cool_rate  # cooling
    fire = False  # wait till the next shoot
    if heat >= 100:  # reaching the maximum heat
        allow_fire = False  # block the gun
    if heat <= 50:  # reaching the necessary cooling
        allow_fire = True  # release the gun


def shield_status():
    """
    Display the actual shields of the ship.

    Returns
    -------
    None.

    """
    global shields_remaining
    for i in range(0, shields_remaining):  # just the remaining shields
        screen.blit(shieldimg, (505 + 30*i, 574))


def draw_blasts():
    """
    Draw every blast thats activated.

    Returns
    -------
    None.

    """
    global blasts
    for index, value in enumerate(blasts):
        screen.blit(explode[value[2]//9], (value[0], value[1]))
        # use value[2]//9, to repeate each imagem 9 times
        value[2] += 1  # add the counter
        if value[2] >= 63:  # after expose all frames of the explosion
            blasts.pop(index)  # delete the finished blast


def draw_score():
    """
    Render the actual score.

    Returns
    -------
    None.

    """
    # first parameter of font.render is a string
    text = font.render(str(score), True, (255, 0, 255))
    screen.blit(text, (680, 10))


def att_dificulty(dificulty_multiplier):
    """
    Update the objects velocity or rate.

    Parameters
    ----------
    dificulty_multiplier : float
        how much multiply the standart velocitys.

    Returns
    -------
    None.

    """
    global player_vel, enemy_vel, bullet_vel, enemy_bullet_vel, meteor_vel,\
        star_vel, collec_vel, shoot_rate, spawn_rate, cool_rate
    # updating the values
    player_vel = std_player_vel * dificulty_multiplier
    enemy_vel = std_enemy_vel * dificulty_multiplier
    bullet_vel = std_bullet_vel * dificulty_multiplier
    enemy_bullet_vel = std_enemy_bullet_vel * dificulty_multiplier
    meteor_vel = std_meteor_vel * dificulty_multiplier
    star_vel = std_star_vel * dificulty_multiplier
    collec_vel = std_collec_vel * dificulty_multiplier
    shoot_rate = std_shoot_rate * (1/dificulty_multiplier)
    spawn_rate = std_spawn_rate * (1/dificulty_multiplier)
    cool_rate = std_cool_rate * dificulty_multiplier


def collectables(px, py):
    """
    Draw and set the collectables mechanics.

    Parameters
    ----------
    px : float
        x position of the player.
    py : float
        y position of the player.

    Returns
    -------
    None.

    """
    global collec_counter, collec, score, dificulty_multiplier,\
        shields_remaining, enemies
    collec_counter += 1
    # just enter if a number of cicles is completed
    if collec_counter >= collec_delay:
        collec_counter = 0  # restart the counter
        # the speed collectable have double probability of spawn
        c = np.random.choice([0, 1, 2, 3], p=[0.2, 0.4, 0.2, 0.2])  # choose
        x = np.random.randint(1, s[0]/2 - 65) * 2.  # place it
        y = -64
        collec = [c, x, y]  # form the collec list [witch_one, x, y]
    if collec != []:  # if there's a collectable
        # we want the collectable to oscilate 4 times in the screen
        # (4*2*pi = aprox 25rad) --> (600pixels/25rad = 24)
        collec[2] += collec_vel + 0.3*np.sin(collec[2]/24)  # 0.3 amplitude
        screen.blit(collecs[collec[0]], (collec[1], collec[2]))
        # we set k value to assign a right hit point
        # when using the bomb collectable, which have
        # 64x64 pixels, instead of the other collectables,
        # which have only 32x32 pixels
        if collec[0] == 3:  # if the sort collectable is the bomb
            k = 16  # put the hit point more 16 pixels down and right
        else:  # if its any other collectable
            k = 0
        # we determine the hit point depending on k value
        hit_dot = (collec[1] + 16 + k, collec[2] + 16 + k)
        if collec[2] >= 600:  # reaching the bottom boundary
            collec = []  # clear the collec list since it was lost
    if collec != []:  # if there's a collectable
        if (px < hit_dot[0] < px+64) and (py < hit_dot[1] < py+64):
            # after hiting the collectable, each one have his own mechanic
            if collec[0] == 0:  # shield collectable
                shield_sound.play()
                if shields_remaining != 3:
                    shields_remaining += 1  # add a shield
            if collec[0] == 1:  # speed collectable
                speed_sound.play()
                dificulty_multiplier += add_dificulty_rate  # set new difculty
                att_dificulty(dificulty_multiplier)  # apply new dificulty
            if collec[0] == 2:  # medal collectable
                medal_sound.play()
                score += 100  # give a hundred points
            if collec[0] == 3:  # bomb collectable
                bomb_sound.play()
                for c in enemies:
                    score += 10  # add points
                    blasts.append([c[0]+32, c[1]+32, 0])  # add explosions
                enemies = []  # kill all enemies
            collec = []  # clear the collec list since it was collected


def music_queue():
    """
    Follows the music queue.

    Returns
    -------
    None.

    """
    global music_counter
    if not pygame.mixer.music.get_busy():  # at the end of each music
        music_counter += 1  # jump to the next
        pygame.mixer.music.load(game_tracks[music_counter])  # load it
        pygame.mixer.music.play()  # play it
        if music_counter == len(game_tracks)-1:  # when the queue ends
            music_counter = 0  # restart the queue


def end_game():
    """
    Verify the end of the game.

    Returns
    -------
    bool
        indicates the end of the game.

    """
    for n in enemies:
        # if a enemy reach player level
        if n[1] >= 480:
            return True
    for i, x in enumerate(meteory):
        # if player hits a meteor
        if 490 <= x <= 554 and np.abs(meteorx[i] - playerx) <= 54:
            return True
    # if player was hit by a enemy bullets and have no shield
    if shields_remaining < 0:
        return True
    else:
        return False


"""Buildind the game pre-menu"""
initial_menu = True
while initial_menu:
    # oscilate the color
    tup = rgb_oscilator()
    screen.fill(tup)

    # event recognizer
    for event in pygame.event.get():
        # recognize the exit buttom and end the program
        if event.type == pygame.QUIT:
            pygame.quit()

    # playing the musics queue
    music_queue()

    # monitoring a key press
    key_pressed = pygame.key.get_pressed()
    if True in key_pressed[:]:  # as some key is pressed
        initial_menu = False  # go out the start menu

    # print top text
    text1 = font.render('We all know that aren\'t', True, (255, 0, 255))
    text2 = font.render('explosions on space,', True, (255, 0, 255))
    text3 = font.render('but don\'t be annoying,', True, (255, 0, 255))
    text4 = font.render('just enjoy.', True, (255, 0, 255))
    screen.blit(text1, (30, 30))
    screen.blit(text2, (30, 70))
    screen.blit(text3, (30, 110))
    screen.blit(text4, (30, 150))

    # print bottom text
    text5 = font.render('press any key to start', True, (255, 0, 255))
    screen.blit(text5, (30, 520))

    # print middle text
    text6 = font2.render('tip: the speed collectable', True, (138, 43, 226))
    text7 = font2.render('make the game much more fun.', True, (138, 43, 226))
    screen.blit(text6, (70, 300))
    screen.blit(text7, (70, 320))

    pygame.display.flip()


"""Building the game loop itself"""
# add the first enemy
add_enemy()

# the Game Loop
running = True
while running:
    # setting the color in RGB
    tup = rgb_oscilator()
    screen.fill(tup)

    # event recognizer
    for event in pygame.event.get():
        # recognize the exit buttom and end the program
        if event.type == pygame.QUIT:
            pygame.quit()

        # alternative solution to keyboard pressing with events
        """
        # recognize left and right
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_LEFT, pygame.K_a]:
                playerx_change = -player_vel
            if event.key in [pygame.K_RIGHT, pygame.K_d]:
                playerx_change = player_vel
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT,
            pygame.K_a, pygame.K_RIGHT, pygame.K_d]:
                playerx_change = 0.0
        """

        # shoot a new bullet
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and allow_fire:
                playershoot_sound.play()  # playing the shoot sound
                fire_bullet()
                fire = True  # sinalise heating

    # playing the musics queue
    music_queue()

    # using get_pressed() returns a boolean list with True at pressed
    # positions. Can be sliced with [pygame.K_key_name]
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
        playerx_change = -player_vel
    if key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
        playerx_change = player_vel
    # as no key is pressed, the ship must stop
    if True not in key_pressed[:]:  # no key is pressed
        playerx_change = 0.0  # stops player movement

    # drawing the stars
    stary += star_vel
    stars()

    # drawing the meteors
    meteory += meteor_vel
    angle += 0.1  # angle increase in each meteor rotation
    angle = angle % 360  # prevent the variable to overlap
    meteor()

    # update the enemies states
    enemies_update()
    spawn_counter += 1
    if spawn_counter >= spawn_rate:  # passed the iterations
        spawn_counter = 0  # restar the counter to a new enemy spawn
        add_enemy()

    # update the bullets state
    bullets_update()

    # drawing collectables
    collectables(playerx, playery)

    # shields
    shield_status()

    # generating heat bar
    screen.blit(baseimg, (595, 575))
    heat_status()
    screen.blit(markerimg, (695, 575))

    # generating score number
    draw_score()

    # drawing the player upon the screen
    playerx += playerx_change
    # if the ship goes further than the boundaries, we cancel the change
    # we subtract 64 from the X limit cause the ship icon have 64 pixels
    if playerx <= 0 or playerx >= s[0]-64:  # reaching the boundaries
        playerx -= playerx_change  # undo the movement
    player(playerx, playery)

    # drawing explosions
    draw_blasts()

    # updating the enemy bullets
    enemy_bullets_update(playerx, playery)

    # verify end game
    if end_game():
        running = False  # stops the main loop

    # display everything
    pygame.display.flip()  # using .flip cause of the dual buffer


"""Building the Game Over screen"""
game_oversound.play()  # playing the game over sound
# game over screen
while True:
    # setting the color in RGB
    tup = rgb_oscilator()
    screen.fill(tup)

    # drawing the stars
    stary += (star_vel*3)
    stars()

    # playing the musics queue
    music_queue()

    # event recognizer
    for event in pygame.event.get():
        # recognize the exit buttom and end the program
        if event.type == pygame.QUIT:
            pygame.quit()

    # print the score
    screen.blit(endimg, (250, 200))
    text = font.render(str(score), True, (255, 0, 119))
    screen.blit(text, (300, 270))

    pygame.display.flip()
