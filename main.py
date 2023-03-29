import math
import pygame
import random
import sys
from settings import *
from classes.tower import Tower
from classes.enemy import Enemy


# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chrono Guardians")


# Set up the font for the game
font = pygame.font.Font(None, 30)

# Set up Pygame clock and lists for sprites
enemies_spawned = 0
clock = pygame.time.Clock()
towers = []
enemies = []

# Set up the game loop
running = True
level = 1
score = 0
money = 50
lives = 20
selected_tower = Tower(0, 0)
enemies_spawned = 0
enemies_per_level = 15
enemy_spawn_interval = 0.02


def draw_pathway():
    # Draw pathway
    for i in range(len(pathway) - 1):
        x1, y1 = pathway[i]
        x2, y2 = pathway[i + 1]

        # Draw two blocks thick pathway
        if x1 == x2:  # vertical segment
            pygame.draw.rect(
                screen, BLUE, (x1 - 30, min(y1, y2) - 30, 59, abs(y1 - y2) + 59))
        else:  # horizontal segment
            pygame.draw.rect(screen, BLUE, (min(x1, x2) - 30,
                             y1 - 30, abs(x1 - x2) + 59, 59))


# Create a function to draw the game screen
def draw_game(lives):
    screen.fill(BLACK)

    # Draw grid
    for i in range(0, 660 + 1, BLOCK_SIZE):
        pygame.draw.line(screen, WHITE, (i, 239), (i, SCREEN_HEIGHT - 1))
    for j in range(240, SCREEN_HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, WHITE, (0, j - 1), (660, j - 1))

    pygame.draw.line(screen, WHITE, (0, 899), (660, 899))

   # Draw pathway
    draw_pathway()

    # Draw sprites
    for tower in towers:
        tower.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)

    # Draw text
    tower_cost_text = font.render(f"Cost: {selected_tower.cost}", True, WHITE)
    screen.blit(tower_cost_text, (10, 10))
    player_money_text = font.render(f"Money: {money}", True, WHITE)
    screen.blit(player_money_text, (10, 40))
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (10, 70))
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 100))
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (10, 130))
    pygame.display.update()


# Define a function to check if a point is inside the pathway
def point_inside_pathway(x, y):
    for i in range(len(pathway) - 1):
        px1, py1 = pathway[i]
        px2, py2 = pathway[i + 1]

        if px1 == px2:  # vertical segment
            if min(py1, py2) <= y <= max(py1, py2) and abs(x - px1) < 45:
                return True
        else:  # horizontal segment
            if min(px1, px2) <= x <= max(px1, px2) and abs(y - py1) < 45:
                return True

    return False


def update_path(enemy):
    global lives
    if enemy.path_index >= len(pathway):
        if enemy in enemies:
            enemies.remove(enemy)
            lives -= 1
            # if lives == 0:
            #     pygame.quit()
            #     sys.exit()
        return

    target_x, target_y = pathway[enemy.path_index]
    dx, dy = target_x - enemy.x, target_y - enemy.y

    if abs(dx) < enemy.speed and abs(dy) < enemy.speed:
        enemy.x, enemy.y = target_x, target_y
        enemy.path_index += 1
    else:
        direction = (dx / abs(dx + dy), dy / abs(dx + dy))
        enemy.x += direction[0] * enemy.speed
        enemy.y += direction[1] * enemy.speed


# Create a function to handle tower placement
def place_tower(x, y):
    global money

    if not point_inside_pathway(x, y) and money >= selected_tower.cost and x < SCREEN_WIDTH - 240 and y >= 240:
        tower = Tower(x // 30 * 30, y // 30 * 30)
        towers.append(tower)
        money -= selected_tower.cost


# Create a function to handle enemy spawning and movement
def spawn_enemy(level, lives):
    enemy_type = random.choice(
        ["Blue Spinner", "Red Shredder", "Green Shark", "Purple Square", "Orange Mystery"])
    enemy = Enemy(level, enemy_type)
    enemies.append(enemy)
    if enemy.color == RED:
        lives -= 1
    update_path(enemy)


while running:
    # Set the game FPS
    clock.tick(FPS)

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if x < SCREEN_WIDTH and y < SCREEN_HEIGHT:
                if x // 30 * 30 < SCREEN_WIDTH and y // 30 * 30 < SCREEN_HEIGHT:
                    place_tower(x, y)
                else:
                    selected_tower = Tower(x, y)

    # Spawn enemies randomly
    if random.random() < enemy_spawn_interval and enemies_spawned < enemies_per_level:
        spawn_enemy(level, lives)
        enemies_spawned += 1

    # Move enemies and check for collisions
    for enemy in enemies:
        update_path(enemy)
        for tower in towers:
            if (enemy.x - tower.x) ** 2 + (enemy.y - tower.y) ** 2 < tower.range ** 2:
                if tower.target is None:
                    tower.target = enemy
                enemy.health -= tower.damage
                if enemy.health <= 0:
                    if enemy in enemies:
                        enemies.remove(enemy)
                    money += 5
                    score += 10
                    for t in towers:
                        if t.target == enemy:
                            t.target = None

    # Check if level is complete
    if len(enemies) == 0 and enemies_spawned == enemies_per_level:
        level += 1
        enemy_spawn_interval *= 0.9
        enemies_spawned = 0

    # Draw the game screen
    draw_game(lives)

    # Check for game over
    if lives == 0:
        pygame.time.wait(2000)
        screen.fill(BLACK)
        game_over_text = font.render("You Lost", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH //
                    2 - 50, SCREEN_HEIGHT // 2))
        pygame.display.update()
        pygame.time.wait(2000)
        running = False

# Quit Pygame
pygame.quit()
