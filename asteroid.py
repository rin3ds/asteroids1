import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        # lazy-load sprites after pygame is initialized
        if not hasattr(Asteroid, "sprite_large"):
            try:
                Asteroid.sprite_large = pygame.image.load("asteroid_sprite.png").convert_alpha()
            except Exception:
                Asteroid.sprite_large = None
        if not hasattr(Asteroid, "sprite_small"):
            try:
                Asteroid.sprite_small = pygame.image.load("asteroid_sprite_small.png").convert_alpha()
            except Exception:
                Asteroid.sprite_small = None

        # rotation state for visual spinning
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-90, 90)

    def draw(self, screen):
        # choose sprite based on radius (low radius -> small sprite)
        sprite = None
        if hasattr(Asteroid, "sprite_large") and hasattr(Asteroid, "sprite_small"):
            sprite = Asteroid.sprite_small if self.radius <= ASTEROID_MIN_RADIUS else Asteroid.sprite_large

        if sprite:
            # scale sprite to roughly match the asteroid size (diameter ~ radius * 1.2)
            size = max(1, int(self.radius * 1.2))
            scaled = pygame.transform.scale(sprite, (size, size))
            rotated = pygame.transform.rotate(scaled, -self.rotation)
            self.rect = rotated.get_rect(center=(round(self.position.x), round(self.position.y)))
            screen.blit(rotated, self.rect)
        else:
            # fallback to circle if sprites aren't available
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
        # update rotation for spinning effect
        self.rotation = (self.rotation + self.rotation_speed * dt) % 360

        