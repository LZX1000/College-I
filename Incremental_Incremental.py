import pygame
import random
import time
import ctypes
from typing import List

def main():
    class Upgrade:
        def __init__(self, name, type, cost, max_level, description, level=0) -> None:
            self.name = name
            self.type = type
            self.cost = cost
            self.level = level
            self.max_level = max_level
            self.description = description

    class Ball:
        def __init__(self) -> None:
            rarity = random.randint(1, 100)
            if rarity <= 75:
                self.rarity = "Common"
                self.color = (0, 0, 0)
                self.money_value = 1
            elif rarity <= 95:
                self.rarity = "Rare"
                self.color = (0, 0, 255)
                self.money_value = 5
            elif rarity <= 99:
                self.rarity = "Epic"
                self.color = (255, 0, 255)
                self.money_value = 25
            else:
                self.rarity = "Legendary"
                self.color = (255, 0, 0)
                self.money_value = 100
            
            self.time = time.monotonic()
        
        def check_for_payount(self) -> int:
            if time.monotonic() - self.time >= 5:
                self.time = time.monotonic()
                return self.money_value
            return 0
        
    class BallsMenuButton(pygame.sprite.Sprite):
        def __init__(
            self,
            menu_surface: pygame.Surface,
            menu_offset: List[int] | None = [0, 0]
        ) -> None:
            super().__init__()

            self.text_surface = font.render("Balls", False, (0, 0, 0))
            self.rect = pygame.Rect(
                menu_offset[0],
                menu_offset[1],
                menu_surface.get_width() / 2,
                30
            )
        
        def debug(self, surface: pygame.Surface) -> None:
            pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)

    class UpgradesMenuButton(pygame.sprite.Sprite):
        def __init__(
            self,
            surface: pygame.Surface,
            offset: List[int] | None = [0, 0]
        ) -> None:
            super().__init__()
            
            self.text_surface = font.render("Upgrades", False, (0, 0, 0))
            self.rect = pygame.Rect(
                offset[0] + surface.get_width() / 2,
                offset[1],
                surface.get_width() / 2,
                30
            )

        def debug(self, surface: pygame.Surface) -> None:
            pygame.draw.rect(surface, (0, 255, 0), self.rect, 1)

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
    # pixelation_factor = 2
    # # Surfaces
    internal_surface = pygame.Surface((internal_width, internal_height)) # For rendering
    menu_surface = pygame.Surface((internal_width / 3, internal_height)) # For rendering
    screen = pygame.display.set_mode(screen_size) # pygame.FULLSCREEN

    running = True
    new = True # Change when adding saving
    debug_mode = False
    menu_type = "Balls"
    menu_offset = ((internal_width / 3) * 2, 0)
    balls_menu_button = BallsMenuButton(menu_surface, menu_offset)
    upgrades_menu_button = UpgradesMenuButton(menu_surface, menu_offset)
    max_fps = 60
    dt = 0

    initialized_upgrades = []
    '''********************Add this to a startup file later********************'''
    upgrades = [
        ("Money Per Click", "money", 10, 10, "Increase money per click by 1"),
        ("Ball Value", "money", 10, 10, "Increase ball value by 1")
    ]
    '''************************************************************************'''

    for upgrade in upgrades:
        initialized_upgrades.append(Upgrade(upgrade[0], upgrade[1], upgrade[2], upgrade[3], upgrade[4]))

    upgrades = initialized_upgrades

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

        scaled_mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (
            scaled_mouse_pos[0] * internal_width / screen_size[0],
            scaled_mouse_pos[1] * internal_height / screen_size[1]
            )
        keys = pygame.key.get_pressed()

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if balls_menu_button.rect.collidepoint(mouse_pos):
                        menu_type = "Balls"
                    elif upgrades_menu_button.rect.collidepoint(mouse_pos):
                        menu_type = "Upgrades"
                    else:
                        player_money += player_money_per_click
                elif event.button == 3:
                    if menu_type == "Upgrades":
                        menu_type = "Balls"
                    elif menu_type == "Balls":
                        menu_type = "Upgrades"
        # Handle keypresses
        if keys[pygame.K_ESCAPE]:
            running = False
    
        if keys[pygame.K_RETURN]:
            if not enter_pressed:
                enter_pressed = True
                enter_timer = time.monotonic()
                if player_money >= new_ball_cost:
                    player_money -= new_ball_cost
                    new_ball_cost = int(round(len(balls) ** 2) / 2 + 11)
                    unresolved_balls.append(0)
                    enter_interval_timer = time.monotonic()
            elif not enter_press_override:
                if player_money >= new_ball_cost and time.monotonic() - enter_interval_timer >= 0.1:
                    player_money -= new_ball_cost
                    new_ball_cost = int(round(len(balls) ** 2) / 2 + 11)
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

        if keys[pygame.K_LCTRL] and keys[pygame.K_SPACE]:
            if not space_pressed:
                space_pressed = True
                if debug_mode:
                    debug_mode = False
                else:
                    debug_mode = True
        else:
            space_pressed = False
        
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
            menu_surface.fill((255, 255, 255)) # Sub-background
            menu_surface.blit(common_ball_count_text_surface, (0, 40))
            menu_surface.blit(rare_ball_count_text_surface, (0, 60))
            menu_surface.blit(epic_ball_count_text_surface, (0, 80))
            menu_surface.blit(legendary_ball_count_text_surface, (0, 100))
            if len(balls) > 0:
                menu_surface.blit(most_recent_ball_text_surface1, (0, 140))
                menu_surface.blit(most_recent_ball_text_surface2, (0, 160))
        elif menu_type == "Upgrades":
            # upgrade_text_surfaces = []
            # for i, upgrade in enumerate(upgrades):
            #     upgrade_text_surface = font.render(f"{upgrade.name} : {upgrade.cost} : {upgrade.type}", False, (0, 0, 0))
                
            # # Blit to Upgrades Menu
            menu_surface.fill((255, 255, 255)) # Sub-background
        menu_surface.blit(balls_menu_button.text_surface, (0, 0))
        menu_surface.blit(upgrades_menu_button.text_surface, (menu_surface.get_width() / 2, 0))
        # Blit to internal_surface
        internal_surface.blit(menu_surface, ((internal_width / 3) * 2, 0))
        # # Text
        internal_surface.blit(money_text_surface, (0, 0))
        internal_surface.blit(ball_cost_text_surface, (0, 20))
        internal_surface.blit(owned_balls_text_surface, (0, 40))
        # Debug
        if debug_mode:
            # Menu buttons
            balls_menu_button.debug(internal_surface)
            upgrades_menu_button.debug(internal_surface)
            # Mouse
            pygame.draw.circle(internal_surface, (0, 0, 0), mouse_pos, 2)

        # Upscale to 1920x1080
        scaled_surface = pygame.transform.scale(internal_surface, screen_size)
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        # Tick Speed
        dt = clock.tick(max_fps) / 1000

    # Save


if __name__ == "__main__":
    main()