import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown = 0
        self.melee_cooldown = 0
        self.melee_active = False

        self.mech_sprite = pygame.image.load("mech_sprite.png").convert_alpha()
        self.mech_sprite = pygame.transform.scale(self.mech_sprite, (PLAYER_RADIUS*5, PLAYER_RADIUS*5))
        self.mech_sprite_shoot = pygame.image.load("mech_sprite_shoot.png").convert_alpha()
        self.mech_sprite_shoot = pygame.transform.scale(self.mech_sprite_shoot, (PLAYER_RADIUS*5, PLAYER_RADIUS*5))
        self.original_image = self.mech_sprite
        self.shooting = False
        self.rect = self.original_image.get_rect(center=(x, y))


    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        # Draw the rotated mech sprite centered on the player position
        current_sprite = self.mech_sprite_shoot if self.shooting else self.mech_sprite
        rotated_image = pygame.transform.rotate(current_sprite, -self.rotation + 180)
        self.rect = rotated_image.get_rect(center=(round(self.position.x), round(self.position.y)))
        screen.blit(rotated_image, self.rect)

        if self.melee_active:
            pygame.draw.circle(screen, (255, 0, 0), self.position, self.radius * 4, 4)

    def rotate(self, dt, direction):
        self.rotation += PLAYER_TURN_SPEED * dt * direction

    def move(self, dt, direction):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        self.position += rotated_vector * PLAYER_SPEED * dt * direction

    def shoot(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation) 
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * (self.radius * 1.2)

        spawn_left = self.position + forward * (self.radius + SHOT_RADIUS) - right
        spawn_right = self.position + forward * (self.radius + SHOT_RADIUS) + right

        shot_left = Shot(spawn_left.x, spawn_left.y, SHOT_RADIUS)
        shot_left.velocity = forward * PLAYER_SHOOT_SPEED
        
        shot_right = Shot(spawn_right.x, spawn_right.y, SHOT_RADIUS)
        shot_right.velocity = forward * PLAYER_SHOOT_SPEED
        
        self.shooting = not self.shooting
        self.original_image = self.mech_sprite_shoot if self.shooting else self.mech_sprite
        
        if hasattr(self, "containers"):
            for group in self.containers:
                group.add(shot_left)
                group.add(shot_right)
        
        return shot_left
    

    
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

        if self.melee_cooldown > 0: 
            self.melee_cooldown -= dt
        
        if keys[pygame.K_e] and self.melee_cooldown <= 0:
            self.melee_active = True
            self.melee_cooldown = PLAYER_MELEE_COOLDOWN_SECONDS
            self.melee_timer = 0.5

        if self.melee_active:
            self.melee_timer -= dt
            if self.melee_timer <= 0:
                self.melee_active = False

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
            shot = self.shoot()
            self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
                
            # --- Wrap-around logic ---
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0

        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

    





