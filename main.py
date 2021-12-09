import pygame


class Ship:
    def __init__(self, coords, speed, xp=100, armor=0):
        self.coords = coords
        self.speed = speed
        self.xp = xp
        self.armor = armor

    def get_coord(self):
        return self.coords

    def move(self, vert, hor):
        self.coords[0] += self.speed * hor
        self.coords[1] += self.speed * vert
        self.render()

    def render(self):
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, pygame.Color('yellow'), (500, 500), 50)
        pygame.draw.circle(screen, pygame.Color('white'), tuple(self.coords), 25)


if __name__ == '__main__':
    fps = 60
    # Pygame
    pygame.init()
    size = width, height = 1024, 1024
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    ship = Ship([100, 100], 200 / fps)
    # Classes
    ship.render()
    # Variables
    move = [0, 0]
    running = True
    while running:
        ship.move(move[0], move[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if int(event.key) == ord('w'):
                    move[0] = -1
                elif int(event.key) == ord('s'):
                    move[0] = 1
                if int(event.key) == ord('a'):
                    move[1] = -1
                elif int(event.key) == ord('d'):
                    move[1] = 1
            elif event.type == pygame.KEYUP:
                if int(event.key) == ord('w'):
                    move[0] = 0
                elif int(event.key) == ord('s'):
                    move[0] = 0
                if int(event.key) == ord('a'):
                    move[1] = 0
                elif int(event.key) == ord('d'):
                    move[1] = 0
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
