import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            "white",
            (int(self.position.x), int(self.position.y)),
            self.radius,
            LINE_WIDTH
        )
    
    def split(self):
        if self.radius <= ASTEROID_MIN_RADIUS:
            Asteroid.kill(self)
        else:
            log_event("asteroid_split")
            
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            angle1 = random.uniform(20, 50)
            angle2 = -random.uniform(20, 50)
            velocity1 = self.velocity.rotate(angle1)
            velocity2 = self.velocity.rotate(angle2)

            Asteroid(self.position.x, self.position.y, new_radius).velocity = velocity1
            Asteroid(self.position.x, self.position.y, new_radius).velocity = velocity2

            
            self.kill()
            


    def update(self, dt):
        self.position += self.velocity * dt

        