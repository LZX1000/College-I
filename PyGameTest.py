import pygame
import math

pygame.init()
clock = pygame.time.Clock()
running = True

size = (1720, 1080)
image_size = str(size).replace(", ", "x")[1:-1]
screen = pygame.display.set_mode(size)   # ((1280, 720), pygame.FULLSCREEN)
background = pygame.image.load(f"assets/grasslands_{image_size}.png")

dt = 0
movement_speed = 300
diagonal_speed = movement_speed / math.sqrt(2)
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
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

    screen.blit(background, (0, 0))

    pygame.draw.circle(screen, "red", player_pos, 40)

    pygame.display.flip()

    dt = clock.tick(60) / 1000
pygame.quit()