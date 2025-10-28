"""
Graphics Module
Handles all rendering including field, players, ball, UI elements, and mode selection.
"""

import pygame
import math
import sys
import os

# Import from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from game_config import *

def draw_mode_selection(screen):
    """Draw the mode selection screen"""
    screen.fill(DARK_GRAY)
    
    # Title
    title_text = large_font.render("ROBOSOCCER - SELECT MODE", True, YELLOW)
    screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 100))
    
    # Mode buttons
    modes = [
        ("MAN vs MAN", "man_vs_man", BLUE),
        ("MAN vs BOT", "bot_vs_man", GREEN),
        ("BOT vs BOT", "bot_vs_bot", RED)
    ]
    
    buttons = []
    for i, (text, mode, color) in enumerate(modes):
        button_rect = pygame.Rect(WIDTH//2 - 150, 200 + i*120, 300, 80)
        buttons.append((button_rect, mode))
        
        # Draw button
        pygame.draw.rect(screen, color, button_rect, border_radius=15)
        pygame.draw.rect(screen, WHITE, button_rect, 3, border_radius=15)
        
        # Draw button text
        mode_text = font.render(text, True, WHITE)
        screen.blit(mode_text, (button_rect.centerx - mode_text.get_width()//2, 
                               button_rect.centery - mode_text.get_height()//2))
    
    # Instructions
    instr_text = small_font.render("Click on a mode to start the game", True, WHITE)
    screen.blit(instr_text, (WIDTH//2 - instr_text.get_width()//2, HEIGHT - 50))
    
    return buttons

def draw_field(screen, audience):
    """Draw the soccer field with markings"""
    # Draw stadium background
    screen.fill(GRAY)
    
    # Draw stands
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, WIDTH, FIELD_Y))
    pygame.draw.rect(screen, DARK_GRAY, (0, FIELD_Y + FIELD_HEIGHT, WIDTH, HEIGHT - FIELD_Y - FIELD_HEIGHT))
    
    # Draw audience
    for x, y, color, state in audience:
        if y < FIELD_Y:  # Top audience
            pygame.draw.circle(screen, color, (x, y), 5)
            if state == 1:  # Cheering
                pygame.draw.circle(screen, YELLOW, (x, y-5), 2)
            elif state == 2:  # Excited
                pygame.draw.circle(screen, YELLOW, (x, y-8), 3)
                pygame.draw.circle(screen, YELLOW, (x-3, y-5), 2)
                pygame.draw.circle(screen, YELLOW, (x+3, y-5), 2)
        else:  # Bottom audience
            pygame.draw.circle(screen, color, (x, y), 5)
            if state == 1:  # Cheering
                pygame.draw.circle(screen, YELLOW, (x, y+5), 2)
            elif state == 2:  # Excited
                pygame.draw.circle(screen, YELLOW, (x, y+8), 3)
                pygame.draw.circle(screen, YELLOW, (x-3, y+5), 2)
                pygame.draw.circle(screen, YELLOW, (x+3, y+5), 2)
    
    # Draw field
    pygame.draw.rect(screen, DARK_GREEN, (FIELD_X, FIELD_Y, FIELD_WIDTH, FIELD_HEIGHT))
    
    # Draw darker grass pattern
    for y in range(FIELD_Y, FIELD_Y + FIELD_HEIGHT, 20):
        for x in range(FIELD_X, FIELD_X + FIELD_WIDTH, 20):
            if (x + y) // 20 % 2 == 0:
                pygame.draw.rect(screen, LIGHT_GREEN, (x, y, 20, 20))
    
    # Field outline
    pygame.draw.rect(screen, WHITE, (FIELD_X, FIELD_Y, FIELD_WIDTH, FIELD_HEIGHT), 3)
    
    # Midfield line & circle
    pygame.draw.line(screen, WHITE, (WIDTH//2, FIELD_Y), (WIDTH//2, FIELD_Y + FIELD_HEIGHT), 2)
    pygame.draw.circle(screen, WHITE, (WIDTH//2, FIELD_Y + FIELD_HEIGHT//2), 70, 2)
    
    # Center spot
    pygame.draw.circle(screen, WHITE, (WIDTH//2, FIELD_Y + FIELD_HEIGHT//2), 5)
    
    # Goals (larger and more visible)
    pygame.draw.rect(screen, WHITE, (FIELD_X - 2, FIELD_Y + 140, 12, 170), 3)      # Left goal (thicker)
    pygame.draw.rect(screen, WHITE, (FIELD_X + FIELD_WIDTH - 10, FIELD_Y + 140, 12, 170), 3)  # Right goal (thicker)
    
    # Goal areas (penalty boxes)
    pygame.draw.rect(screen, WHITE, (FIELD_X, FIELD_Y + 100, 60, 250), 2)      # Left goal area
    pygame.draw.rect(screen, WHITE, (FIELD_X + FIELD_WIDTH - 60, FIELD_Y + 100, 60, 250), 2)  # Right goal area
    
    # Goal posts (make them more visible)
    pygame.draw.circle(screen, WHITE, (FIELD_X, FIELD_Y + 140), 5)  # Left top post
    pygame.draw.circle(screen, WHITE, (FIELD_X, FIELD_Y + 310), 5)  # Left bottom post
    pygame.draw.circle(screen, WHITE, (FIELD_X + FIELD_WIDTH, FIELD_Y + 140), 5)  # Right top post
    pygame.draw.circle(screen, WHITE, (FIELD_X + FIELD_WIDTH, FIELD_Y + 310), 5)  # Right bottom post
    
    # Corner arcs
    pygame.draw.arc(screen, WHITE, (FIELD_X - 20, FIELD_Y - 20, 40, 40), math.pi/2, math.pi, 2)
    pygame.draw.arc(screen, WHITE, (FIELD_X + FIELD_WIDTH - 20, FIELD_Y - 20, 40, 40), 0, math.pi/2, 2)
    pygame.draw.arc(screen, WHITE, (FIELD_X - 20, FIELD_Y + FIELD_HEIGHT - 20, 40, 40), math.pi, 3*math.pi/2, 2)
    pygame.draw.arc(screen, WHITE, (FIELD_X + FIELD_WIDTH - 20, FIELD_Y + FIELD_HEIGHT - 20, 40, 40), 3*math.pi/2, 2*math.pi, 2)

def draw_players_and_ball(screen, ball, blue_team, red_team):
    """Draw players and ball with better visuals"""
    # Ball with shadow effect
    pygame.draw.circle(screen, (80, 80, 80), (ball.centerx+2, ball.centery+2), BALL_RADIUS)
    pygame.draw.circle(screen, WHITE, ball.center, BALL_RADIUS)
    pygame.draw.circle(screen, (200, 200, 200), ball.center, BALL_RADIUS-4)
    # Ball pattern
    pygame.draw.line(screen, BLACK, (ball.centerx - 7, ball.centery), (ball.centerx + 7, ball.centery), 2)
    pygame.draw.line(screen, BLACK, (ball.centerx, ball.centery - 7), (ball.centerx, ball.centery + 7), 2)
    pygame.draw.circle(screen, BLACK, ball.center, 5, 1)
    
    # Players with team colors and details
    for i, p in enumerate(blue_team):
        pygame.draw.circle(screen, BLUE, p.center, PLAYER_RADIUS)
        pygame.draw.circle(screen, (30, 70, 200), p.center, PLAYER_RADIUS-4)
        # Player number
        num_text = small_font.render(str(i+1), True, WHITE)
        screen.blit(num_text, (p.centerx-5, p.centery-8))
        
    for i, p in enumerate(red_team):
        pygame.draw.circle(screen, RED, p.center, PLAYER_RADIUS)
        pygame.draw.circle(screen, (200, 30, 30), p.center, PLAYER_RADIUS-4)
        # Player number
        num_text = small_font.render(str(i+1), True, WHITE)
        screen.blit(num_text, (p.centerx-5, p.centery-8))

def draw_time_complexity_graph(screen, time_data, current_mode):
    """Draw a graph showing time complexity analysis"""
    if not time_data[current_mode]:
        return
    
    graph_width, graph_height = 250, 120
    graph_x, graph_y = WIDTH - graph_width - 10, 10
    
    # Draw graph background
    pygame.draw.rect(screen, (50, 50, 50), (graph_x, graph_y, graph_width, graph_height))
    pygame.draw.rect(screen, (100, 100, 100), (graph_x, graph_y, graph_width, graph_height), 1)
    
    # Draw title
    mode_text = small_font.render(f"Mode: {current_mode}", True, WHITE)
    screen.blit(mode_text, (graph_x + 5, graph_y + 5))
    
    # Draw data
    max_val = max(time_data[current_mode]) if max(time_data[current_mode]) > 0 else 1
    points = []
    
    for i, val in enumerate(time_data[current_mode]):
        x = graph_x + (i / len(time_data[current_mode])) * graph_width
        y = graph_y + graph_height - (val / max_val) * graph_height
        points.append((x, y))
    
    if len(points) > 1:
        pygame.draw.lines(screen, YELLOW, False, points, 2)
    
    # Draw scale
    scale_text = small_font.render(f"Max: {max_val:.4f}s", True, WHITE)
    screen.blit(scale_text, (graph_x + 5, graph_y + graph_height - 15))
    
    # Draw current value
    current_val = time_data[current_mode][-1] if time_data[current_mode] else 0
    current_text = small_font.render(f"Current: {current_val:.4f}s", True, WHITE)
    screen.blit(current_text, (graph_x + 5, graph_y + graph_height - 30))

def draw_set_piece_indicator(screen, set_piece_type, set_piece_team):
    """Draw set piece indicator if active"""
    if set_piece_type is not None and set_piece_team:
        team_color = BLUE if set_piece_team == "blue" else RED
        
        # Main message - specific to set piece type
        if set_piece_type == "kick_off":
            set_piece_text = font.render(f"{set_piece_team.upper()} TEAM KICK OFF", True, team_color)
        elif set_piece_type == "corner_kick":
            set_piece_text = font.render(f"{set_piece_team.upper()} TEAM CORNER KICK", True, team_color)
        elif set_piece_type == "goal_kick":
            set_piece_text = font.render(f"{set_piece_team.upper()} TEAM GOAL KICK", True, team_color)
        else:  # throw_in
            set_piece_text = font.render(f"{set_piece_team.upper()} TEAM THROW-IN", True, team_color)
        screen.blit(set_piece_text, (WIDTH//2 - set_piece_text.get_width()//2, FIELD_Y + 20))
        
        # Show that teams have been positioned automatically
        if set_piece_type == "kick_off":
            reset_text = small_font.render("Midfield kick-off - all players reset to positions", True, YELLOW)
        elif set_piece_type == "corner_kick":
            opposite_team = "RED" if set_piece_team == "blue" else "BLUE"
            reset_text = small_font.render(f"Corner kick - {opposite_team} team reset, {set_piece_team.upper()} at corner", True, YELLOW)
        elif set_piece_type == "goal_kick":
            opposite_team = "RED" if set_piece_team == "blue" else "BLUE"
            reset_text = small_font.render(f"Goal kick - {opposite_team} team reset, {set_piece_team.upper()} near goal", True, YELLOW)
        else:
            opposite_team = "RED" if set_piece_team == "blue" else "BLUE"
            reset_text = small_font.render(f"Throw-in - {opposite_team} team reset, {set_piece_team.upper()} at sideline", True, YELLOW)
        screen.blit(reset_text, (WIDTH//2 - reset_text.get_width()//2, FIELD_Y + 50))
        
        # Instructions - different for each set piece type
        if set_piece_type == "kick_off":
            instruction_text = small_font.render("Player is ready - TOUCH BALL to restart kick-off", True, WHITE)
        elif set_piece_type == "corner_kick":
            instruction_text = small_font.render("Corner kick - TOUCH BALL to take corner", True, WHITE)
        elif set_piece_type == "goal_kick":
            instruction_text = small_font.render("Goal kick - TOUCH BALL to clear from goal", True, WHITE)
        else:
            instruction_text = small_font.render("Throw-in - TOUCH BALL to restart play", True, WHITE)
        screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2, FIELD_Y + 80))

def draw_ui_elements(screen, blue_score, red_score, match_start_time, frame_count, 
                    player_movement_data, current_mode, time_data):
    """Draw all UI elements including scores, timer, controls, etc."""
    import time
    
    # Scores
    score_text = font.render(f"{blue_score} : {red_score}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - 40, 20))
    
    # Match timer
    match_duration = time.time() - match_start_time
    minutes = int(match_duration // 60)
    seconds = int(match_duration % 60)
    timer_text = small_font.render(f"Time: {minutes:02d}:{seconds:02d}", True, WHITE)
    screen.blit(timer_text, (WIDTH - timer_text.get_width() - 10, HEIGHT - 30))
    
    # Controls help - make red team controls VERY clear
    if current_mode == "man_vs_man":
        # Blue team controls
        blue_controls = small_font.render("BLUE TEAM: WASD (Player 1) | Arrow Keys (Player 2)", True, BLUE)
        screen.blit(blue_controls, (10, HEIGHT - 60))
        
        # Red team controls - make them stand out
        red_controls = small_font.render("RED TEAM: IJKL (Player 1) | YUOP (Player 2)", True, RED)
        screen.blit(red_controls, (10, HEIGHT - 40))
        
        # Game controls
        game_controls = small_font.render("SPACE: Pause | R: Reset | E: Export Report | ESC: Mode Select", True, WHITE)
        screen.blit(game_controls, (10, HEIGHT - 20))
        
    elif current_mode == "bot_vs_man":
        controls_text = small_font.render("BLUE TEAM (YOU): WASD (Player 1) | Arrow Keys (Player 2) | Red Team = AI", True, WHITE)
        screen.blit(controls_text, (10, HEIGHT - 40))
        game_controls = small_font.render("SPACE: Pause | R: Reset | E: Export Report | ESC: Mode Select", True, WHITE)
        screen.blit(game_controls, (10, HEIGHT - 20))
    else:
        controls_text = small_font.render("Both teams AI | SPACE: Pause | R: Reset | E: Export Report | ESC: Menu", True, WHITE)
        screen.blit(controls_text, (10, HEIGHT - 30))
    
    # Current mode display and description
    if current_mode == "man_vs_man":
        mode_text = small_font.render("Mode: MAN vs MAN - Both teams controlled by humans", True, YELLOW)
        screen.blit(mode_text, (WIDTH - mode_text.get_width() - 10, HEIGHT - 80))
        
        # Show player assignments
        blue_assign = small_font.render("Blue Team: You control both players", True, BLUE)
        screen.blit(blue_assign, (WIDTH - blue_assign.get_width() - 10, HEIGHT - 100))
        
        red_assign = small_font.render("Red Team: Friend controls both players", True, RED)
        screen.blit(red_assign, (WIDTH - red_assign.get_width() - 10, HEIGHT - 120))
        
    elif current_mode == "bot_vs_man":
        mode_text = small_font.render("Mode: HUMAN vs AI - You are Blue Team", True, YELLOW)
        screen.blit(mode_text, (WIDTH - mode_text.get_width() - 10, HEIGHT - 80))
    else:
        mode_text = small_font.render("Mode: AI vs AI - Watch the robots play!", True, YELLOW)
        screen.blit(mode_text, (WIDTH - mode_text.get_width() - 10, HEIGHT - 80))
    
    # Data collection info
    data_text = small_font.render(f"Frames: {frame_count} | Data Points: {len(player_movement_data[current_mode])}", True, GREEN)
    screen.blit(data_text, (10, 10))

def draw_pause_screen(screen):
    """Display pause message"""
    pause_text = font.render("PAUSED - Press SPACE to continue", True, WHITE)
    screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - 24))