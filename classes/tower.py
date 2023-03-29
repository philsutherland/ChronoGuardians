from settings import *


class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.cost = 10
        self.damage = 11
        self.range = 100
        self.type = "Green Laser"
        self.target = None

    def draw(self, screen):
        pygame.draw.rect(
            screen, GREEN, (self.x, self.y, self.width, self.height))
        if self.target is not None:
            pygame.draw.line(screen, WHITE, (self.x + self.width // 2, self.y + self.height // 2),
                             (self.target.x + self.target.width // 2, self.target.y + self.target.height // 2), 2)
