import pygame
import sys
from logger import log_state
from logger import log_event
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot



def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")

    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Assign containers BEFORE creating instances
    Player.containers = (updatable, drawable, shots)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (updatable, drawable, shots)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")

    run = True
    while run:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Update all sprites
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()

        # Clear screen
        screen.fill("black")

        # Draw all sprites
        for d in drawable:
            d.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    pygame.quit()

if __name__ == "__main__":
    main()
