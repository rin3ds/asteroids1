import pygame
from circleshape import CircleShape
from shot import Shot
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, SHOT_RADIUS, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown = 0

    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt, direction):
        self.rotation += PLAYER_TURN_SPEED * dt * direction

    def move(self, dt, direction):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        self.position += rotated_vector * PLAYER_SPEED * dt * direction

    def shoot(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        spawn_position = self.position + forward * (self.radius + SHOT_RADIUS)

        shot = Shot(spawn_position.x, spawn_position.y, SHOT_RADIUS)
        shot.velocity = forward * PLAYER_SHOOT_SPEED
        
        if hasattr(self, "containers"):
            for group in self.containers:
                group.add(shot)
        
        return shot
    

    
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(dt, -1)
        if keys[pygame.K_d]:
            self.rotate(dt, 1)
        if keys[pygame.K_w]:
            self.move(dt, 1)
        if keys[pygame.K_s]:
            self.move(dt, -1)

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
            shot = self.shoot()
            for group in self.containers:
                self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

    





