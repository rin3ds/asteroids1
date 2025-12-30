import pygame
import sys
from logger import log_state
from logger import log_event
from constants import *
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
    
    
    #score
    score = 0
    font = pygame.font.Font(None, 36)
    

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # containers
    Player.containers = (updatable, drawable, shots)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (updatable, drawable, shots)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")

    run = True
    game_state = "playing"

    while run:
        log_state()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if game_state == "game_over" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    score = 0
                    
                    asteroids.empty()
                    updatable.empty()
                    drawable.empty()
                    shots.empty()
                    
                    player.kill()
                    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

                    asteroid_field.kill()
                    asteroid_field = AsteroidField()

                    game_state = "playing"
                elif event.key == pygame.K_q:
                    run = False

        if game_state == "playing":
        
            # Update all sprites
            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    log_event("player_hit")
                    game_state = "game_over"
    
                

            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collides_with(shot):
                        log_event("asteroid_shot")
                        asteroid.split()
                        shot.kill()
                        score += 100
            
            for asteroid in asteroids:
                if player.melee_active:
                    if asteroid.position.distance_to(player.position) < player.radius * 8:
                        asteroid.split()
                        score += 100


            # Clear screen
            screen.fill("black")

            # Draw all sprites
            for d in drawable:
                d.draw(screen)

            # Draw Score
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

        elif game_state == "game_over":
            screen.fill("black")
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
            restart_text = font.render("Press R to Restart or Q to Quit", True, (200, 200, 200))

            screen.blit(game_over_text, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 - 60))
            screen.blit(score_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
            screen.blit(restart_text, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2 + 40))

        pygame.display.flip()
        dt = clock.tick(60) / 1000
        

    pygame.quit()

if __name__ == "__main__":
    main()
