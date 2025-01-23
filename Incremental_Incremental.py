import pygame
import random
import time
import ctypes

def main():
    class Ball:
        def __init__(self):
            rarity = random.randint(1, 100)
            if rarity <= 50:
                self.rarity = "Common"
                self.color = (0, 0, 0)
                self.money_value = 1
            elif rarity <= 80:
                self.rarity = "Rare"
                self.color = (0, 0, 255)
                self.money_value = 5
            elif rarity <= 95:
                self.rarity = "Epic"
                self.color = (255, 0, 255)
                self.money_value = 25
            else:
                self.rarity = "Legendary"
                self.color = (255, 0, 0)
                self.money_value = 100
            
            self.time = time.monotonic()
        
        def check_for_payount(self):
            if time.monotonic() - self.time >= 5:
                self.time = time.monotonic()
                return self.money_value
            return 0
        
    # Initialize
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 20)
    pygame.display.set_caption("CollegeI")
    clock = pygame.time.Clock()

    # Display
    # # Resolutions
    internal_width = 640
    internal_height = 360
    ctypes.windll.user32.SetProcessDPIAware()
    screen_size = (1920, 1080)
    pixelation_factor = 2
    # # Surfaces
    internal_surface = pygame.Surface((internal_width, internal_height)) # For rendering
    balls_menu_surface = pygame.Surface((internal_width / 3, internal_height)) # For rendering
    screen = pygame.display.set_mode(screen_size) # pygame.FULLSCREEN

    running = True
    new = True # Change when adding saving
    menu_type = "Main"
    enter_press_override = False
    max_fps = 60
    dt = 0

    while running:
        # Reset
        if new:
            player_money = 100
            player_money_per_click = 1
            new_ball_cost = 10
            balls = []
            unresolved_balls = []
            legendary_ball_count = 0
            epic_ball_count = 0
            rare_ball_count = 0
            common_ball_count = 0
            new = False

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player_money += player_money_per_click
                elif event.button == 3:
                    if menu_type == "Main":
                        menu_type = "Balls"
                    elif menu_type == "Balls":
                        menu_type = "Main"
        # Handle keypresses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
    
        if keys[pygame.K_RETURN]:
            if not enter_pressed:
                enter_pressed = True
                enter_timer = time.monotonic()
                if player_money >= new_ball_cost:
                    player_money -= new_ball_cost
                    new_ball_cost = (len(balls) ** 2) + 10
                    unresolved_balls.append(0)
                    enter_interval_timer = time.monotonic()
            elif not enter_press_override:
                if player_money >= new_ball_cost and time.monotonic() - enter_interval_timer >= 0.1:
                    player_money -= new_ball_cost
                    new_ball_cost = (len(balls) ** 2) + 10
                    unresolved_balls.append(0)
                    enter_interval_timer = time.monotonic()
            else:
                if time.monotonic() - enter_timer >= 0.5:
                    enter_pressed = False
                    enter_press_override = True
        else:
            enter_pressed = False
            enter_press_override = False
        
        if keys[pygame.K_LCTRL] and keys[pygame.K_q]:
            player_money += 100000
        
        if len(unresolved_balls) > 0:
            for _ in unresolved_balls:
                new_ball = Ball()
                if new_ball.rarity == "Common":
                    common_ball_count += 1
                elif new_ball.rarity == "Rare":
                    rare_ball_count += 1
                elif new_ball.rarity == "Epic":
                    epic_ball_count += 1
                else:
                    legendary_ball_count += 1
                balls.append(new_ball)
                unresolved_balls.remove(0)

        for ball in balls:
            player_money += ball.check_for_payount()

        # Render in 640x360
        internal_surface.fill((180, 180, 180)) # Sub-background
        # background.game_update(internal_surface)
        money_text_surface = font.render(f"Money :  {player_money}", False, (0, 0, 0))
        ball_cost_text_surface = font.render(f"Ball Cost : {new_ball_cost}", False, (0, 0, 0))
        owned_balls_text_surface = font.render(f"Owned Balls : {len(balls)}", False, (0, 0, 0))
        balls_menu_text_surface = font.render("Balls Menu", False, (0, 0, 0))
        # Balls Menu
        if menu_type == "Balls":
            common_ball_count_text_surface = font.render(f"Common Balls : {common_ball_count}", False, (0, 0, 0))
            rare_ball_count_text_surface = font.render(f"Rare Balls : {rare_ball_count}", False, (0, 0, 0))
            epic_ball_count_text_surface = font.render(f"Epic Balls : {epic_ball_count}", False, (0, 0, 0))
            legendary_ball_count_text_surface = font.render(f"Legendary Balls : {legendary_ball_count}", False, (0, 0, 0))
            if len(balls) > 0:
                most_recent_ball_text_surface1 = font.render(f"Most Recent Ball :", False, (0, 0, 0))
                most_recent_ball_text_surface2 = font.render(f"        {balls[-1].rarity} Ball", False, (balls[-1].color))
            # # Blit to Balls Menu
            balls_menu_surface.fill((255, 255, 255)) # Sub-background
            balls_menu_surface.blit(common_ball_count_text_surface, (0, 40))
            balls_menu_surface.blit(rare_ball_count_text_surface, (0, 60))
            balls_menu_surface.blit(epic_ball_count_text_surface, (0, 80))
            balls_menu_surface.blit(legendary_ball_count_text_surface, (0, 100))
            if len(balls) > 0:
                balls_menu_surface.blit(most_recent_ball_text_surface1, (0, 140))
                balls_menu_surface.blit(most_recent_ball_text_surface2, (0, 160))
            internal_surface.blit(balls_menu_surface, ((internal_width / 3) * 2, 0))
        # Blit to internal_surface
        if menu_type == "Balls":
            internal_surface.blit(balls_menu_text_surface, ((internal_width / 3) * 2, 0))
        internal_surface.blit(money_text_surface, (0, 0))
        internal_surface.blit(ball_cost_text_surface, (0, 20))
        internal_surface.blit(owned_balls_text_surface, (0, 40))

        # Upscale to 1920x1080
        scaled_surface = pygame.transform.scale(internal_surface, screen_size)
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        # Tick Speed
        dt = clock.tick(max_fps) / 1000

    # Save


if __name__ == "__main__":
    main()