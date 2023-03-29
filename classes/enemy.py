from settings import *


# Create classes for Tower and Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, level, enemy_type):
        super().__init__()
        self.x, self.y = pathway[0]
        self.width = 20
        self.height = 20
        self.type = enemy_type
        self.boarder_width = 3
        self.max_health, self.color, self.speed, self.damage, self.boarder_color = self.get_enemy_properties(
            enemy_type)
        self.health = self.max_health + (level * 5)
        self.path_index = 1

        # Set color, shape, speed, and health based on enemy type
        if enemy_type == "Blue Spinner":
            self.color = (0, 191, 255)
            self.shape = "circle"
            self.speed = random.uniform(4.0, 5.0)
            self.max_health = 400 + (level * 5)
            self.health = self.max_health
        elif enemy_type == "Red Shredder":
            self.color = (255, 0, 0)
            self.shape = "octagon"
            self.speed = random.uniform(3.0, 4.0)
            self.max_health = 500 + (level * 5)
            self.health = self.max_health
        elif enemy_type == "Green Shark":
            self.color = (0, 255, 0)
            self.shape = "triangle"
            self.speed = random.uniform(2.0, 3.0)
            self.max_health = 1000 + (level * 5)
            self.health = self.max_health
        elif enemy_type == "Purple Square":
            self.color = (128, 0, 128)
            self.shape = "square"
            self.speed = random.uniform(3.0, 4.0)
            self.max_health = 750 + (level * 5)
            self.health = self.max_health
        elif enemy_type == "Orange Mystery":
            self.color = (255, 165, 0)
            self.shape = "diamond"
            self.speed = random.uniform(1.0, 2.0)
            self.max_health = 2000 + (level * 5)
            self.health = self.max_health
        else:
            raise ValueError(f"Invalid enemy type: {enemy_type}")

    def move(self):
        if self.path_index >= len(pathway):
            print("Enemy reached end of pathway")
            return  # enemy has reached the end of the path

        target_x, target_y = pathway[self.path_index]
        dx, dy = target_x - self.x, target_y - self.y

        if abs(dx) <= self.speed and abs(dy) <= self.speed:
            self.x, self.y = target_x, target_y
            self.path_index += 1
        else:
            direction = (dx / abs(dx + dy), dy / abs(dx + dy))
            self.x += direction[0] * self.speed
            self.y += direction[1] * self.speed

    def draw(self, screen):
        # draw shape
        if self.shape == "circle":
            pygame.draw.circle(screen, self.color + (64,), (int(
                self.x + self.width/2), int(self.y + self.height/2)), int(self.width/2))
            pygame.draw.circle(screen, self.boarder_color, (int(self.x + self.width/2), int(
                self.y + self.height/2)), int(self.width/2), self.boarder_width)
        elif self.shape == "square":
            pygame.draw.rect(screen, self.color + (64,),
                             (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, self.boarder_color, (self.x - self.boarder_width, self.y - self.boarder_width,
                                                          self.width + 2 * self.boarder_width, self.height + 2 * self.boarder_width), self.boarder_width)
        elif self.shape == "triangle":
            points = [(self.x + self.width/2, self.y), (self.x, self.y +
                                                        self.height), (self.x + self.width, self.y + self.height)]
            pygame.draw.polygon(screen, self.color + (64,), points)
            pygame.draw.polygon(screen, self.boarder_color,
                                points, self.boarder_width)
        elif self.shape == "octagon":
            points = [(self.x + self.width/4, self.y), (self.x + 3*self.width/4, self.y),
                      (self.x + self.width, self.y + self.height /
                       4), (self.x + self.width, self.y + 3*self.height/4),
                      (self.x + 3*self.width/4, self.y + self.height), (self.x +
                                                                        self.width/4, self.y + self.height),
                      (self.x, self.y + 3*self.height/4), (self.x, self.y + self.height/4)]
            pygame.draw.polygon(screen, self.color + (64,), points)
            pygame.draw.polygon(screen, self.boarder_color,
                                points, self.boarder_width)
        elif self.shape == "diamond":
            points = [(self.x + self.width/2, self.y), (self.x + self.width, self.y + self.height/2),
                      (self.x + self.width/2, self.y + self.height), (self.x, self.y + self.height/2)]
            pygame.draw.polygon(screen, self.color + (64,), points)
            pygame.draw.polygon(screen, self.boarder_color,
                                points, self.boarder_width)

        health_ratio = self.get_health_ratio()
        if health_ratio < 1.0:
            health_bar_width = self.width * health_ratio
            health_bar_rect = pygame.Rect(
                self.x, self.y - HEALTH_BAR_HEIGHT - 2, health_bar_width, HEALTH_BAR_HEIGHT)
            pygame.draw.rect(screen, RED, health_bar_rect)

    def get_enemy_properties(self, enemy_type):
        if enemy_type == "Blue Spinner":
            return 300, LIGHT_BLUE, random.uniform(4.0, 5.0), 15, DARK_BLUE
        elif enemy_type == "Red Shredder":
            return 500, RED, random.uniform(2.5, 3.5), 20, DARK_RED
        elif enemy_type == "Green Shark":
            return 1000, GREEN, random.uniform(1.0, 2.0), 50, DARK_GREEN
        elif enemy_type == "Purple Square":
            return 750, PURPLE, random.uniform(2.0, 3.0), 35, DARK_PURPLE
        elif enemy_type == "Orange Mystery":
            return 1500, ORANGE, random.uniform(1.0, 1.5), 100, DARK_ORANGE
        else:
            raise ValueError(f"Invalid enemy type: {enemy_type}")

    def get_health_ratio(self):
        return self.health / self.max_health
