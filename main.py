import pygame
import random
import math
from pygame import mixer

pygame.init()
# WE INITIALIZE OUR PYGAME MODULE TO START WORKING


# WE INITIALIZE THE SCREEN (WIDTH X HEIGTH)
screen = pygame.display.set_mode((800, 600))

# TITLE AND ICON
pygame.display.set_caption("Shooting Ninja")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# background music
mixer.music.load("file_example_WAV_10MG.wav")
mixer.music.play(-1)
# PLAYER
playerImg = pygame.image.load("spaceship.png")
playerX = 370
playerY = 490
playerX_Change = 0

# EMMEY
enemyImg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("space-invaders.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_Change.append(0.3)
    enemyY_Change.append(40)

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 490
bulletX_Change = 0
bulletY_Change = 5
# ready -> the bullet is not moving and it cannot be seen on the screen
# fire -> the bullet is  moving and it  be seen on the screen
bullet_state = "ready"

# player score
score_value = 0
font = pygame.font.Font("Great Wishes.otf", 32)
textX = 10
textY = 10

# Game over text
game_over_font = pygame.font.Font("Great Wishes.otf", 50)


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (0, 0, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = font.render("GAME OVER " + str(score_value), True, (0, 0, 0))
    screen.blit(over_text, (200, 300))


# PLAYER FUNCTION
def player(x, y):
    screen.blit(playerImg, (x, y))


# ENEMY FUNCTION
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def bullet_fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    # calculation the distance between the bullet and the enemy

    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    # if its shorter then the bullet has collided with our enemy
    if distance < 27:
        return True


# GAME LOOP
running = True
while running:
    # Background (RGB)
    screen.fill((0, 128, 128))

    # CALL A PLAYER
    player(playerX, playerY)
    # PLAYER MOVING X-COORDINATES

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # CHECK FOR A KEYSTROKE PRESSED (PRESS DOWN MEAN PRESSING THE KEY AND PRESS UP MEANS RELEASE THE KEY)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_Change = -2

            if event.key == pygame.K_RIGHT:
                playerX_Change = +2

            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("40_smith_wesson_single-mike-koenig.wav")
                    # Get the current X-coordinate of spaceship
                    bullet_sound.play()
                    bulletX = playerX
                    bullet_fire(bulletX, bulletY)

        # RELEASE THE KEY
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0

    playerX += playerX_Change
    # check game Boundary of a player
    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # check game Boundary an enemy (Enemy movement)
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
                # looser = mixer.Sound("Sad.wav")
                game_over_text()
                # looser.play()
            break
        enemyX[i] += enemyX_Change[i]
        if enemyX[i] <= 0:
            enemyX_Change[i] = +3
            enemyY[i] += enemyY_Change[i]

        elif enemyX[i] >= 736:
            enemyX_Change[i] = -1
            enemyY[i] += enemyY_Change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("glass_break_02.wav")
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Reset bullet
    if bulletY <= 0:
        bulletY = 490
        bullet_state = "ready"

    # bullet movement
    if bullet_state is "fire":
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletY_Change

    enemyX += enemyX_Change
    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()
