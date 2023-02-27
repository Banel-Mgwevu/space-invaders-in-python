import pygame
import random


# init the pygame

pygame.init()


#creating the screen
screen=pygame.display.set_mode((800,600))

#Game Title & Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

#background image
backImg=pygame.image.load('background.jpg')

#Invader (player I)
playerImg=pygame.image.load('invader.png')
playerX=370
playerY=480
playerX_change=0
playerY_change=0

#Enemy (player I)
enemyImg=pygame.image.load('enemy.png')
enemyX=random.randint(0, 730)
enemyY=random.randint(50, 150)
enemyX_change=0.3
enemyY_change=10

#bullet

#If bullet is ready its invisible
#Fire bullet is visible and Y is decreasing

bulletImg=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=10
bullet_state="ready"


def player(x,y):
    screen.blit(playerImg,(playerX,playerY))

def enemy(x,y):
    screen.blit(enemyImg,(enemyX,enemyY))

def fire_bullet(x,y):
    global bullet_state
    bullet_state='fire'
    screen.blit(bulletImg,(bulletX+16,bulletY+10))


#This is how freeeze a screen
running=True

while running:

    screen.fill((0, 0, 0))
    screen.blit(backImg,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change=-0.4
            if event.key == pygame.K_RIGHT:
                playerX_change=0.4
            if event.key == pygame.K_UP:
                playerY_change=-0.4
            if event.key == pygame.K_DOWN:
                playerY_change=0.4
            if event.key == pygame.K_SPACE:
                bulletX=playerX
                fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change=0
                playerY_change=0

    playerX+=playerX_change
    playerY+=playerY_change

    if playerX<=0:
        playerX=0
    elif playerX >=734 :
        playerX=734

    if playerY<=5:
        playerY=5
    elif playerY>=734:
        playerY=734

    enemyX+=enemyX_change

    if enemyX<=0:
        enemyX_change=0.3
        enemyY+=enemyY_change
    if enemyX>=734:
        enemyX_change=-0.3
        enemyY+=enemyY_change

    if bullet_state is "fire":
        fire_bullet(bulletX,playerY)
        bulletY=-bulletX_change

    if bulletY<=10:
        bulletY=480
        bullet_state='ready'

    player(playerX,playerY)
    enemy(enemyX,enemyY)

    pygame.display.update()
