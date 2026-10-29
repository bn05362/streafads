import pygame
from config import LEVELS, MAPS, clamp, play_sound, SOUND_FILES

class GameController:
    def __init__(self, game):
        self.game = game

    def handle_key(self, key):
        game = self.game

        if game.state == "MENU":
            if key == pygame.K_RETURN:
                game.start_match()
            elif key == pygame.K_c:
                game.state = "CHARACTER_SELECT"
            elif key == pygame.K_m:
                game.state = "MAP_SELECT"
            elif key == pygame.K_s:
                game.state = "SHOP"
            elif key == pygame.K_l:
                game.current_level_index = (game.current_level_index + 1) % len(LEVELS)
                game.load_current_level_boss()
            elif key == pygame.K_q:
                pygame.quit()
                import sys
                sys.exit()

        elif game.state == "MAP_SELECT":
            if key == pygame.K_ESCAPE:
                game.state = "MENU"
            elif key == pygame.K_1:
                game.selected_map_index = 0
                game.state = "MENU"
            elif key == pygame.K_2:
                game.selected_map_index = 1
                game.state = "MENU"
            elif key == pygame.K_3:
                game.selected_map_index = 2
                game.state = "MENU"

        elif game.state == "CHARACTER_SELECT":
            if key == pygame.K_ESCAPE:
                game.state = "MENU"
            elif key == pygame.K_1:
                game.selected_class_index = 0
                game.apply_selected_character()
                game.state = "MENU"
            elif key == pygame.K_2:
                game.selected_class_index = 1
                game.apply_selected_character()
                game.state = "MENU"
            elif key == pygame.K_3:
                game.selected_class_index = 2
                game.apply_selected_character()
                game.state = "MENU"

        elif game.state == "SHOP":
            if key == pygame.K_ESCAPE:
                game.state = "MENU"
            elif key == pygame.K_1:
                game.upgrade_weapon()
            elif key == pygame.K_2:
                game.upgrade_armor()

        elif game.state == "PLAYING":
            if key in (pygame.K_w, pygame.K_SPACE):
                if game.player.jump_count < game.player.max_jumps and not getattr(game.player, 'is_crouching', False):
                    game.player.vy = game.player.jump_force
                    game.player.jump_count += 1

            elif key == pygame.K_e:
                game.attack(game.player, game.enemy, "light")
            elif key == pygame.K_y:
                game.attack(game.player, game.enemy, "heavy")
            elif key == pygame.K_c:
                game.attack(game.player, game.enemy, "skill")
            
            elif key == pygame.K_x:
                if game.player_heal_uses > 0 and game.player_heal_amount_left <= 0:
                    game.player_heal_uses -= 1
                    game.player_heal_amount_left = 300
                    game.player_healing_timer = 3.0
                    game.add_floating_text("+300 HP", game.player.x, game.player.y - 100, (0, 255, 0))
                    play_sound(SOUND_FILES["victory"])

            elif key == pygame.K_f:
                wall_x = game.player.x + game.player.facing * 60
                if len(game.walls) >= 4:
                    game.walls.pop(0)

                game.walls.append({
                    "x": wall_x,
                    "y": 510, # GROUND_Y - 90
                    "w": 20,
                    "h": 90,
                    "hits_left": 4,
                    "timer": 5.0,
                    "color": MAPS[game.selected_map_index]["accent"]
                })
                game.add_floating_text("TƯỜNG CHẮN PHÍA TRƯỚC!", wall_x, 490, (0, 255, 255))

            elif key == pygame.K_r:
                wall_x = game.player.x - game.player.facing * 60
                if len(game.walls) >= 4:
                    game.walls.pop(0)

                game.walls.append({
                    "x": wall_x,
                    "y": 510,
                    "w": 20,
                    "h": 90,
                    "hits_left": 4,
                    "timer": 5.0,
                    "color": MAPS[game.selected_map_index]["accent"]
                })
                game.add_floating_text("TƯỜNG CHẮN PHÍA SAU!", wall_x, 490, (0, 255, 255))

            elif key == pygame.K_z:
                if game.player.stamina >= 12:
                    game.player.stamina -= 12
                    game.player.parry_timer = 0.4
                    play_sound(SOUND_FILES["parry"])
                    game.player.last_action = "PARRY!"
            
            elif key == pygame.K_v:
                if game.player_dodge_cd <= 0 and game.player.stamina >= 15:
                    game.player.stamina -= 15
                    game.player.dodge_timer = 0.4
                    game.player_dodge_cd = 0.5  # Cooldown 0.5s
                    game.player.x = clamp(game.player.x - game.player.facing * 70, 50, 950)
                    play_sound(SOUND_FILES["dodge"])
                    game.player.last_action = "DODGE!"
                    game.add_floating_text("NÉ THÀNH CÔNG!", game.player.x, game.player.y - 100, (0, 255, 255))
                    game.spawn_particles(game.player.x, game.player.y - 50, (0, 255, 255))

            elif key == pygame.K_1:
                game.player.stance = "HIGH"
            elif key == pygame.K_2:
                game.player.stance = "MID"
            elif key == pygame.K_3:
                game.player.stance, game.player.last_action = "LOW", "Thế LOW"
            elif key == pygame.K_ESCAPE:
                game.state = "MENU"

        elif game.state == "GAMEOVER":
            if key in (pygame.K_RETURN, pygame.K_SPACE):
                game.state = "MENU"

    def handle_mouse_click(self, button):
        game = self.game
        if game.state == "PLAYING" and button == 1:
            game.attack(game.player, game.enemy, "heavy")