import pygame
import random
import math

pygame.init()
clock = pygame.time.Clock()

size = (1920, 1080)
image_size = str(size).replace(", ", "x")[1:-1]
screen = pygame.display.set_mode(size)   # ((1280, 720), pygame.FULLSCREEN)
background = pygame.image.load(f"assets/grasslands_1720x1080.png") # f"assets/grasslands_{image_size}.png"

max_fps = 60

dt = 0
movement_speed = 300
diagonal_speed = movement_speed / math.sqrt(2)
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

class GamePlayer(pygame.sprite.Sprite):
    def __init__(self, pos, image, size):
        super().__init__()
        self.source_image = pygame.image.load(f"assets/GameCharacter.png")
        self.image = pygame.transform.scale(self.source_image, (size, size))
        self.rect = self.image.get_rect(center=pos)

    def update(self, screen, pos):
        screen.blit(self.image, self.rect.topleft)
        self.rect.center = pos

class Object(pygame.sprite.Sprite):
    def __init__(self, size, pos=None):
        super().__init__()
        self.source_image = pygame.image.load(f"assets/Point.png")
        self.image = pygame.transform.scale(self.source_image, (size, size))
        self.rect = self.image.get_rect()
        self.size = size
        ## Randomize position
        while True:
            self.pos = pygame.Vector2(
                random.randint(size // 2, screen.get_width() - size // 2),
                random.randint(size // 2, screen.get_height() - size // 2)
            )
            ### Check for collision with other objects
            if not any(obj.rect.collidepoint(self.pos) for obj in objects):
                break
        self.rect.center = self.pos

    def update(self, screen):
        screen.blit(self.image, self.rect.topleft)

player = GamePlayer(player_pos, "green", 60)

# Object handling
objects = []
max_objects = 3
## Generate objects
for _ in range(max_objects):
    new_object = Object(30)
    objects.append(new_object)
object_sprites = pygame.sprite.Group(objects)

running = True

while running:
    # Exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    # Diagonal movement
    if keys[pygame.K_w] and keys[pygame.K_a] or keys[pygame.K_UP] and keys[pygame.K_LEFT]:
        player_pos.x -= diagonal_speed * dt
        player_pos.y -= diagonal_speed * dt
    elif keys[pygame.K_w] and keys[pygame.K_d] or keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
        player_pos.x += diagonal_speed * dt
        player_pos.y -= diagonal_speed * dt
    elif keys[pygame.K_s] and keys[pygame.K_a] or keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
        player_pos.x -= diagonal_speed * dt
        player_pos.y += diagonal_speed * dt
    elif keys[pygame.K_s] and keys[pygame.K_d] or keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
        player_pos.x += diagonal_speed * dt
        player_pos.y += diagonal_speed * dt
    # Straight movement
    elif keys[pygame.K_w] or keys[pygame.K_UP]:
        player_pos.y -= movement_speed * dt
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_pos.y += movement_speed * dt
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_pos.x -= movement_speed * dt
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_pos.x += movement_speed * dt
    # Misc inputs
    elif keys[pygame.K_ESCAPE]:
        running = False
    
    # Check Collisions
    collided_object = pygame.sprite.spritecollide(player, object_sprites, dokill=True)
    for collided in collided_object:
        ## Remove collided object
        if collided in objects:
            objects.remove(collided)
            object_sprites.remove(collided)
        ## Add new object
        new_object = Object(30)
        objects.append(new_object)
        object_sprites.add(new_object)

    # Update Screen
    screen.blit(background, (0, 0))
    for obj in objects:
        obj.update(screen)
    player.update(screen, player_pos)

    pygame.display.flip()
    # Tick Speed
    dt = clock.tick(max_fps) / 1000
pygame.quit()