"""
Main Game Controller
Orchestrates the entire soccer game using modular components.
"""

"""
Main Game Controller
Orchestrates the entire soccer game using modular components.
"""

import pygame
import sys
import time
import random
import os

# Import from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from game_config import *
from physics import (reset_positions, move_ai, handle_ball_collision, 
                     keep_players_in_bounds, handle_player_input)
from game_rules import handle_out_of_bounds, execute_set_piece
from graphics import (draw_mode_selection, draw_field, draw_players_and_ball, 
                      draw_time_complexity_graph, draw_set_piece_indicator, 
                      draw_ui_elements, draw_pause_screen, draw_performance_report)
from data_analysis import (initialize_data_structures, collect_research_data,
                           export_performance_data, export_comparison_report,
                           generate_performance_report)

def initialize_game():
    """Initialize all game objects and data structures"""
    # Initialize ball
    ball = pygame.Rect(WIDTH//2 - BALL_RADIUS, HEIGHT//2 - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)
    ball_vel = [random.choice([-BALL_SPEED, BALL_SPEED]), random.choice([-BALL_SPEED, BALL_SPEED])]

    # Create players (2 per team for all modes)
    blue_team = [pygame.Rect(FIELD_X + 50, FIELD_Y + 150 + i*150, PLAYER_RADIUS*2, PLAYER_RADIUS*2) for i in range(2)]
    red_team = [pygame.Rect(FIELD_X + FIELD_WIDTH - 70, FIELD_Y + 150 + i*150, PLAYER_RADIUS*2, PLAYER_RADIUS*2) for i in range(2)]

    # Scores
    blue_score = 0
    red_score = 0

    # Game state
    game_paused = False
    goal_timer = 0
    set_piece_timer = 0
    set_piece_type = None  # 'corner', 'throw_in', 'goal_kick'
    set_piece_team = None  # 'blue' or 'red'
    set_piece_start_positions = {"blue": [], "red": []}  # Track starting positions for movement detection
    last_touch = None  # Track which team last touched the ball

    # Initialize data structures
    time_data, player_movement_data, ball_position_data, game_stats = initialize_data_structures()

    current_mode = None  # Start with no mode selected
    analysis_start_time = 0
    match_start_time = 0
    match_duration = 0
    show_results = False
    frame_count = 0
    possession_timer = 0
    last_possession = None

    # Create audience
    audience = create_audience()

    return (ball, ball_vel, blue_team, red_team, blue_score, red_score, game_paused, goal_timer,
            set_piece_timer, set_piece_type, set_piece_team, set_piece_start_positions, last_touch,
            time_data, player_movement_data, ball_position_data, game_stats, current_mode,
            analysis_start_time, match_start_time, match_duration, show_results, frame_count,
            possession_timer, last_possession, audience)

def change_mode(new_mode, time_data, player_movement_data, ball_position_data, 
                blue_team, red_team, ball, ball_vel):
    """Change the current game mode"""
    current_mode = new_mode
    analysis_start_time = time.time()
    match_start_time = time.time()
    frame_count = 0
    
    # Clear data for the new mode
    time_data[current_mode].clear()
    player_movement_data[current_mode].clear()
    ball_position_data[current_mode].clear()
    
    # Reset to 2 players per team for all modes
    blue_team = [pygame.Rect(FIELD_X + 50, FIELD_Y + 150 + i*150, PLAYER_RADIUS*2, PLAYER_RADIUS*2) for i in range(2)]
    red_team = [pygame.Rect(FIELD_X + FIELD_WIDTH - 70, FIELD_Y + 150 + i*150, PLAYER_RADIUS*2, PLAYER_RADIUS*2) for i in range(2)]
    
    reset_positions(ball, ball_vel, blue_team, red_team)
    
    return current_mode, analysis_start_time, match_start_time, frame_count, blue_team, red_team

def main():
    """Main game loop"""
    print("Starting main game loop...")
    print("=== ROBOSOCCER GAME STARTED ===")
    print("Look for the game window titled 'RoboSoccer - 2v2'")
    print("If you can't see it, try Alt+Tab to find it")
    print("===============================")
    
    # Initialize everything
    (ball, ball_vel, blue_team, red_team, blue_score, red_score, game_paused, goal_timer,
     set_piece_timer, set_piece_type, set_piece_team, set_piece_start_positions, last_touch,
     time_data, player_movement_data, ball_position_data, game_stats, current_mode,
     analysis_start_time, match_start_time, match_duration, show_results, frame_count,
     possession_timer, last_possession, audience) = initialize_game()
    
    running = True
    match_start_time = time.time()
    data_exported = False
    mode_selection = True
    report_surface = None

    while running:
        frame_start_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not mode_selection:
                    # Return to mode selection
                    mode_selection = True
                    current_mode = None
                    show_results = False
                elif event.key == pygame.K_SPACE and not mode_selection:
                    game_paused = not game_paused
                elif event.key == pygame.K_r and not mode_selection:
                    blue_score = 0
                    red_score = 0
                    reset_positions(ball, ball_vel, blue_team, red_team)
                    data_exported = False
                    match_start_time = time.time()
                    frame_count = 0
                elif event.key == pygame.K_e and not mode_selection:
                    # Export report immediately (E key)
                    print("\n" + "="*60)
                    print("📊 EXPORTING REPORTS NOW...")
                    print("="*60)
                    export_performance_data(time_data, player_movement_data, ball_position_data, game_stats)
                    export_comparison_report(time_data, game_stats, player_movement_data)
                    print("✅ Reports exported successfully!")
                    print("="*60 + "\n")
                elif event.key == pygame.K_p and show_results:
                    # Check if click is on close button
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if WIDTH//2 - 50 <= mouse_x <= WIDTH//2 + 50 and HEIGHT - 100 <= mouse_y <= HEIGHT - 60:
                        show_results = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mode_selection:
                    # Mode selection screen
                    buttons = draw_mode_selection(screen)
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    for button_rect, mode in buttons:
                        if button_rect.collidepoint(mouse_x, mouse_y):
                            (current_mode, analysis_start_time, match_start_time, frame_count, 
                             blue_team, red_team) = change_mode(mode, time_data, player_movement_data, 
                                                              ball_position_data, blue_team, red_team, 
                                                              ball, ball_vel)
                            mode_selection = False
                elif show_results:
                    # Check if click is on close button
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if WIDTH//2 - 50 <= mouse_x <= WIDTH//2 + 50 and HEIGHT - 100 <= mouse_y <= HEIGHT - 60:
                        show_results = False

        if mode_selection:
            buttons = draw_mode_selection(screen)
            pygame.display.flip()
            continue

        if show_results:
            if not data_exported:
                export_performance_data(time_data, player_movement_data, ball_position_data, game_stats)
                export_comparison_report(time_data, game_stats, player_movement_data)
                report_surface = generate_performance_report(time_data, player_movement_data, ball_position_data)
                data_exported = True
                
            draw_performance_report(screen, report_surface, blue_score, red_score)
            pygame.display.flip()
            continue

        if game_paused:
            draw_pause_screen(screen)
            pygame.display.flip()
            continue

        if goal_timer > 0:
            goal_timer -= 1

        # Handle set pieces and out of bounds (including goals)
        if set_piece_type is not None:
            set_piece_completed = execute_set_piece(ball, ball_vel, blue_team, red_team, set_piece_team)
            if set_piece_completed:
                set_piece_type = None
                set_piece_team = None
                set_piece_timer = 0
                set_piece_start_positions = {"blue": [], "red": []}
        else:
            # Normal play - check for out of bounds and goals
            bounds_result = handle_out_of_bounds(ball, ball_vel, blue_team, red_team, blue_score, red_score, 
                                               last_touch, game_stats, current_mode, audience, cheer_sound)
            
            if bounds_result[0] != "in_play":
                (result_type, set_piece_type, set_piece_team, set_piece_timer, 
                 set_piece_start_positions, goal_timer, blue_score, red_score) = bounds_result

        keys = pygame.key.get_pressed()
        
        # Handle different game modes
        if current_mode == "bot_vs_bot":
            # All players are AI
            move_ai(blue_team, ball, is_red=False, set_piece_type=set_piece_type, set_piece_team=set_piece_team)
            move_ai(red_team, ball, is_red=True, set_piece_type=set_piece_type, set_piece_team=set_piece_team)
        elif current_mode == "bot_vs_man":
            # Handle manual controls for blue team
            handle_player_input(keys, current_mode, blue_team, red_team)
            # Red team is AI
            move_ai(red_team, ball, is_red=True, set_piece_type=set_piece_type, set_piece_team=set_piece_team)
        elif current_mode == "man_vs_man":
            # Handle manual controls for both teams
            handle_player_input(keys, current_mode, blue_team, red_team)

        # Keep players within field bounds
        keep_players_in_bounds(blue_team + red_team)

        # Ball movement with friction (only if not in set piece)
        if set_piece_type is None:
            ball.x += ball_vel[0]
            ball.y += ball_vel[1]
            ball_vel[0] *= FRICTION
            ball_vel[1] *= FRICTION

            # Handle collisions only during normal play
            last_touch = handle_ball_collision(ball, ball_vel, blue_team, red_team) or last_touch
        else:
            # During set piece, ball is completely stopped
            ball_vel[0], ball_vel[1] = 0, 0

        # Collect research data
        possession_timer, last_possession = collect_research_data(
            ball, blue_team, red_team, current_mode, frame_count, match_start_time,
            player_movement_data, ball_position_data, game_stats, last_touch, 
            possession_timer, last_possession
        )

        # Draw everything
        draw_field(screen, audience)
        draw_set_piece_indicator(screen, set_piece_type, set_piece_team)
        draw_players_and_ball(screen, ball, blue_team, red_team)
        draw_ui_elements(screen, blue_score, red_score, match_start_time, frame_count, 
                        player_movement_data, current_mode, time_data)

        # Calculate and store frame time for complexity analysis
        frame_time = time.time() - frame_start_time
        time_data[current_mode].append(frame_time)
        
        # Draw time complexity graph
        draw_time_complexity_graph(screen, time_data, current_mode)
        
        # End match after 3 minutes or when Q is pressed
        match_duration = time.time() - match_start_time
        if (match_duration >= 180 or keys[pygame.K_q]) and not show_results:
            # Finalize possession tracking
            if last_possession:
                game_stats[current_mode]["possession_time"][last_possession] += possession_timer
            game_stats[current_mode]["match_duration"] = match_duration
            show_results = True

        frame_count += 1
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()