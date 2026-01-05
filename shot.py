import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            "red",
            (int(self.position.x), int(self.position.y)),
            self.radius,
            LINE_WIDTH * 2
        )

    def update(self, dt):
        self.position += self.velocity * dt
        screen_rect = pygame.display.get_surface().get_rect()
        if not screen_rect.collidepoint(self.position):
            self.kill()


        