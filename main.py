import pygame
import random
import math

pygame.init()

# Creating the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('alien.png')
pygame.display.set_icon(icon)

# Loading images
backImg = pygame.image.load('background.jpg')
playerImg = pygame.image.load('invader.png')
enemyImg = pygame.image.load('enemy.png')
bulletImg = pygame.image.load('bullet.png')

# Player
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy properties
enemies = []
num_of_enemies = 6  # Set initial number of enemies
max_enemies = 6  # Maximum number of enemies allowed

# Create enemies
for i in range(num_of_enemies):
    enemy_x = random.randint(0, 730)
    enemy_y = random.randint(50, 150)
    enemies.append({'x': enemy_x, 'y': enemy_y, 'x_change': 0.3, 'y_change': 40, 'state': 'alive'})

# Bullet
bulletX = 0
bulletY = 480
bulletY_change = 10
bullet_state = "ready"

game_over_font = pygame.font.Font(None, 64)
restart_font = pygame.font.Font(None, 32)

def player(x, y):
    screen.blit(playerImg, (x, y))

def draw_enemy(x, y):
    screen.blit(enemyImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:  # Adjust this value for better collision accuracy
        return True
    else:
        return False

def player_enemy_collision(playerX, playerY, enemyX, enemyY):
    distance = math.sqrt(math.pow(playerX - enemyX, 2) + math.pow(playerY - enemyY, 2))
    if distance < 27:  # Adjust this value for better collision accuracy
        return True
    else:
        return False

def reset_game():
    global playerX, playerY, bullet_state
    playerX = 370
    playerY = 480
    bullet_state = "ready"

def game_over_text(text):
    over_text = game_over_font.render(text, True, (255, 255, 255))
    restart_text = restart_font.render("Press 'R' to restart", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    screen.blit(restart_text, (300, 320))

def create_enemy():
    if len(enemies) < max_enemies:
        enemy_x = random.randint(0, 730)
        enemy_y = random.randint(50, 150)
        enemies.append({'x': enemy_x, 'y': enemy_y, 'x_change': 0.3, 'y_change': 40, 'state': 'alive'})

running = True
game_over = False
while running:

    screen.fill((0, 0, 0))
    screen.blit(backImg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -0.4
                if event.key == pygame.K_RIGHT:
                    playerX_change = 0.4
                if event.key == pygame.K_UP:
                    playerY_change = -0.4
                if event.key == pygame.K_DOWN:
                    playerY_change = 0.4
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerY_change = 0
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_over = False
                enemies.clear()
                for i in range(num_of_enemies):
                    enemy_x = random.randint(0, 730)
                    enemy_y = random.randint(50, 150)
                    enemies.append({'x': enemy_x, 'y': enemy_y, 'x_change': 0.3, 'y_change': 40, 'state': 'alive'})
                reset_game()

    playerX += playerX_change
    playerY += playerY_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    for enemy in enemies:
        if enemy['state'] == 'alive':
            enemy['x'] += enemy['x_change']
            if enemy['x'] <= 0:
                enemy['x_change'] = 0.3
                enemy['y'] += enemy['y_change']
            elif enemy['x'] >= 736:
                enemy['x_change'] = -0.3
                enemy['y'] += enemy['y_change']

            draw_enemy(enemy['x'], enemy['y'])

    create_enemy()

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    for enemy in enemies:
        if enemy['state'] == 'alive':
            collision = is_collision(enemy['x'], enemy['y'], bulletX, bulletY)
            if collision:
                bulletY = 480
                bullet_state = "ready"
                enemy['state'] = 'dead'

    alive_enemies = sum(enemy['state'] == 'alive' for enemy in enemies)
    if alive_enemies == 0 and not game_over:
        game_over = True

    for enemy in enemies:
        if enemy['state'] == 'alive':
            collision = player_enemy_collision(playerX, playerY, enemy['x'], enemy['y'])
            if collision:
                game_over = True

    if game_over and alive_enemies == 0:
        game_over_text("YOU WIN!")
    elif game_over:
        game_over_text("YOU'RE DEAD!")

    player(playerX, playerY)

    pygame.display.update()

pygame.quit()
