import pygame
from logger import log_state
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroids")

run = True
while run:
    log_state()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    screen.fill("black")
    pygame.display.flip()


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

if __name__ == "__main__":
    main()
