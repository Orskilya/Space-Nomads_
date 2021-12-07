import pygame


class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_coord(self):
        return self.x, self.y

    def move(self, x, y):
        self.x += x
        self.y += y

    def draw(self):
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, pygame.Color('yellow'), (500, 500), 100)
        pygame.draw.circle(screen, pygame.Color('white'), (self.x, self.y), 25)


if __name__ == '__main__':
    pygame.init()
    fps = 60
    size = width, height = 1024, 1024
    screen = pygame.display.set_mode(size)
    pygame.draw.circle(screen, pygame.Color('yellow'), (500, 500), 100)
    ship = Ship(100, 100)
    ship.draw()
    clock = pygame.time.Clock()
    move = False
    running = True
    while running:
        if move:
            ship.move(100 / fps, 100 / fps)
        ship.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                move = True
            elif event.type == pygame.KEYUP:
                move = False
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
