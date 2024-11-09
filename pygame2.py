import random
import os
import pygame

class Player(object):
    def __init__(self):
        self.rect = pygame.Rect(500, 250, 40, 40)

    def move(self, dx, dy):
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                global game
                game = False

class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 20, 20)

class Lava(object):
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], 20, 20)

    def update(self):
        self.rect.y += 5  # Move the lava down

        if self.rect.y > screen.get_height():
            lavas.remove(self)

        if self.rect.colliderect(player.rect):
            global game
            game = False

os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
screen = pygame.display.set_mode((1000, 500))

walls = []
lavas = []
clock = pygame.time.Clock()
player = Player()

level = [
    "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "w                                                w",
    "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"
]

x = y = 0
for row in level:
    for col in row:
        if col == "w":
            Wall((x, y))
        x += 20
    y += 20
    x = 0

last_lava_time = pygame.time.get_ticks()
start_time = pygame.time.get_ticks()
running = True
game = True

while running:
    if game:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                game = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
                game = False

        current_time = pygame.time.get_ticks()

        if current_time - last_lava_time > 50:  # Lava spawns every 50 ms
            last_lava_time = current_time
            x_pos = random.randint(0, screen.get_width() - 20)
            lavas.append(Lava((x_pos, 0)))

        time_alive = (current_time - start_time) / 1000  # Convert to seconds

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player.move(-4, 0)
        if key[pygame.K_RIGHT]:
            player.move(4, 0)
        if key[pygame.K_UP]:
            player.move(0, -4)
        if key[pygame.K_DOWN]:
            player.move(0, 4)

        screen.fill((0, 0, 0))

        for wall in walls:
            pygame.draw.rect(screen, (255, 0, 0), wall.rect)

        for lava in lavas:
            lava.update()
            pygame.draw.rect(screen, (255, 0, 0), lava.rect)

        pygame.draw.rect(screen, (255, 200, 0), player.rect)
        pygame.display.flip()

    else:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render(f"You survived for {time_alive:.2f} seconds", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(text, text_rect)
        pygame.display.flip()

        pygame.time.wait(3000)
        running = False

pygame.quit()

