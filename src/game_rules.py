"""
Game Rules Module
Handles goals, set pieces, out-of-bounds logic, and game state management.
"""

import pygame
import random
import sys
import os

# Import from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from game_config import *
from physics import reset_positions, reset_team_positions

def handle_out_of_bounds(ball, ball_vel, blue_team, red_team, blue_score, red_score, 
                        last_touch, game_stats, current_mode, audience, cheer_sound):
    """Handle when ball touches court border - trigger foul immediately"""
    set_piece_timer = 0
    set_piece_type = None
    set_piece_team = None
    goal_timer = 0
    set_piece_start_positions = {"blue": [], "red": []}

    # Check if ball touches any border line (trigger foul immediately on contact)
    if ball.left <= FIELD_X or ball.right >= FIELD_X + FIELD_WIDTH or \
       ball.top <= FIELD_Y or ball.bottom >= FIELD_Y + FIELD_HEIGHT:
        
        # Store the current ball position for exact placement
        out_x, out_y = ball.centerx, ball.centery
        
        # Determine what happened based on where ball went out
        if ball.left <= FIELD_X:  # Out on left side
            # Check for goal first - make goal area larger for better detection
            if FIELD_Y + 140 < ball.centery < FIELD_Y + 310:  # Goal area (made larger)
                # GOAL for RED team! Ball went into blue's goal
                red_score += 1
                game_stats[current_mode]["goals"] += 1
                goal_timer = goal_delay
                print(f"GOAL! Red team scores! Score: Blue {blue_score} - Red {red_score}")
                
                # Goal celebration
                for i in range(len(audience)):
                    if random.random() < 0.7:  # 70% chance to cheer for goal
                        audience[i] = (audience[i][0], audience[i][1], audience[i][2], 2)  # Excited state
                if cheer_sound:
                    cheer_sound.play()
                
                # Midfield restart - reset to center, blue team gets kick-off (team that conceded)
                reset_positions(ball, ball_vel, blue_team, red_team)
                set_piece_type = "kick_off"
                set_piece_team = "blue"  # Blue team gets the kick-off after conceding
                ball.centerx = WIDTH//2
                ball.centery = HEIGHT//2
                ball_vel[0], ball_vel[1] = 0, 0  # Stop ball completely for kick-off
                
                # Record starting positions for movement detection
                set_piece_start_positions = {
                    "blue": [(p.centerx, p.centery) for p in blue_team],
                    "red": [(p.centerx, p.centery) for p in red_team]
                }
                return "goal", set_piece_type, set_piece_team, set_piece_timer, set_piece_start_positions, goal_timer, blue_score, red_score
            else:
                # Ball crossed blue's goal line (not in goal) - corner kick or goal kick
                if last_touch == "red":
                    # Red touched last - GOAL KICK for blue team
                    set_piece_type = "goal_kick"
                    set_piece_team = "blue"
                    ball.centerx = FIELD_X + 30
                    ball.centery = FIELD_Y + FIELD_HEIGHT // 2
                    reset_team_positions(red_team, is_red_team=True)
                    blue_team[0].centerx = ball.centerx
                    blue_team[0].centery = ball.centery - 30
                    print("Goal kick for Blue team!")
                else:
                    # Blue touched last - CORNER KICK for red team
                    set_piece_type = "corner_kick"
                    set_piece_team = "red"
                    if out_y < FIELD_Y + FIELD_HEIGHT // 2:
                        ball.centerx = FIELD_X + 15  # Top-left corner
                        ball.centery = FIELD_Y + 15
                    else:
                        ball.centerx = FIELD_X + 15  # Bottom-left corner
                        ball.centery = FIELD_Y + FIELD_HEIGHT - 15
                    reset_team_positions(blue_team, is_red_team=False)
                    red_team[0].centerx = ball.centerx + 20
                    red_team[0].centery = ball.centery
                    print("Corner kick for Red team!")
                
                set_piece_timer = 0
                ball_vel[0], ball_vel[1] = 0, 0
                set_piece_start_positions = {
                    "blue": [(p.centerx, p.centery) for p in blue_team],
                    "red": [(p.centerx, p.centery) for p in red_team]
                }
                return "set_piece", set_piece_type, set_piece_team, set_piece_timer, set_piece_start_positions, goal_timer, blue_score, red_score
                    
        elif ball.right >= FIELD_X + FIELD_WIDTH:  # Out on right side
            # Check for goal first - make goal area larger for better detection
            if FIELD_Y + 140 < ball.centery < FIELD_Y + 310:  # Goal area (made larger)
                # GOAL for BLUE team! Ball went into red's goal
                blue_score += 1
                game_stats[current_mode]["goals"] += 1
                goal_timer = goal_delay
                print(f"GOAL! Blue team scores! Score: Blue {blue_score} - Red {red_score}")
                
                # Goal celebration
                for i in range(len(audience)):
                    if random.random() < 0.7:  # 70% chance to cheer for goal
                        audience[i] = (audience[i][0], audience[i][1], audience[i][2], 2)  # Excited state
                if cheer_sound:
                    cheer_sound.play()
                
                # Midfield restart - reset to center, red team gets kick-off (team that conceded)
                reset_positions(ball, ball_vel, blue_team, red_team)
                set_piece_type = "kick_off"
                set_piece_team = "red"  # Red team gets the kick-off after conceding
                ball.centerx = WIDTH//2
                ball.centery = HEIGHT//2
                ball_vel[0], ball_vel[1] = 0, 0  # Stop ball completely for kick-off
                
                # Record starting positions for movement detection
                set_piece_start_positions = {
                    "blue": [(p.centerx, p.centery) for p in blue_team],
                    "red": [(p.centerx, p.centery) for p in red_team]
                }
                return "goal", set_piece_type, set_piece_team, set_piece_timer, set_piece_start_positions, goal_timer, blue_score, red_score
            else:
                # Ball crossed red's goal line (not in goal) - corner kick or goal kick
                if last_touch == "blue":
                    # Blue touched last - GOAL KICK for red team
                    set_piece_type = "goal_kick"
                    set_piece_team = "red"
                    ball.centerx = FIELD_X + FIELD_WIDTH - 30
                    ball.centery = FIELD_Y + FIELD_HEIGHT // 2
                    reset_team_positions(blue_team, is_red_team=False)
                    red_team[0].centerx = ball.centerx
                    red_team[0].centery = ball.centery - 30
                    print("Goal kick for Red team!")
                else:
                    # Red touched last - CORNER KICK for blue team
                    set_piece_type = "corner_kick"
                    set_piece_team = "blue"
                    if out_y < FIELD_Y + FIELD_HEIGHT // 2:
                        ball.centerx = FIELD_X + FIELD_WIDTH - 15  # Top-right corner
                        ball.centery = FIELD_Y + 15
                    else:
                        ball.centerx = FIELD_X + FIELD_WIDTH - 15  # Bottom-right corner
                        ball.centery = FIELD_Y + FIELD_HEIGHT - 15
                    reset_team_positions(red_team, is_red_team=True)
                    blue_team[0].centerx = ball.centerx - 20
                    blue_team[0].centery = ball.centery
                    print("Corner kick for Blue team!")
                
                set_piece_timer = 0
                ball_vel[0], ball_vel[1] = 0, 0
                set_piece_start_positions = {
                    "blue": [(p.centerx, p.centery) for p in blue_team],
                    "red": [(p.centerx, p.centery) for p in red_team]
                }
                return "set_piece", set_piece_type, set_piece_team, set_piece_timer, set_piece_start_positions, goal_timer, blue_score, red_score
                    
        elif ball.centery <= FIELD_Y:  # Out on top
            # Place ball slightly inside field
            ball.centerx = max(FIELD_X + BALL_RADIUS, min(FIELD_X + FIELD_WIDTH - BALL_RADIUS, out_x))
            ball.centery = FIELD_Y + BALL_RADIUS + 15
            set_piece_type = "throw_in"
            # Opposite team of who last touched gets the ball
            set_piece_team = "red" if last_touch == "blue" else "blue"
            # Reset the team that caused the ball to go out
            if last_touch == "blue":
                reset_team_positions(blue_team, is_red_team=False)
                # Bring red player to ball position
                red_team[0].centerx = ball.centerx
                red_team[0].centery = ball.centery - (PLAYER_RADIUS + BALL_RADIUS + 10)
                print("Blue team sent back - Red player positioned at ball location")
            else:
                reset_team_positions(red_team, is_red_team=True)
                # Bring blue player to ball position
                blue_team[0].centerx = ball.centerx
                blue_team[0].centery = ball.centery - (PLAYER_RADIUS + BALL_RADIUS + 10)
                print("Red team sent back - Blue player positioned at ball location")
            
        elif ball.centery >= FIELD_Y + FIELD_HEIGHT:  # Out on bottom
            # Place ball slightly inside field
            ball.centerx = max(FIELD_X + BALL_RADIUS, min(FIELD_X + FIELD_WIDTH - BALL_RADIUS, out_x))
            ball.centery = FIELD_Y + FIELD_HEIGHT - BALL_RADIUS - 15
            set_piece_type = "throw_in"
            # Opposite team of who last touched gets the ball
            set_piece_team = "red" if last_touch == "blue" else "blue"
            # Reset the team that caused the ball to go out
            if last_touch == "blue":
                reset_team_positions(blue_team, is_red_team=False)
                # Bring red player to ball position
                red_team[0].centerx = ball.centerx
                red_team[0].centery = ball.centery + (PLAYER_RADIUS + BALL_RADIUS + 10)
                print("Blue team sent back - Red player positioned at ball location")
            else:
                reset_team_positions(red_team, is_red_team=True)
                # Bring blue player to ball position
                blue_team[0].centerx = ball.centerx
                blue_team[0].centery = ball.centery + (PLAYER_RADIUS + BALL_RADIUS + 10)
                print("Red team sent back - Blue player positioned at ball location")
        
        # Set timer for set piece and stop the ball
        set_piece_timer = 0  # No timer - manual restart only
        ball_vel[0], ball_vel[1] = 0, 0  # Stop the ball completely
        
        # Record starting positions for movement detection
        set_piece_start_positions = {
            "blue": [(p.centerx, p.centery) for p in blue_team],
            "red": [(p.centerx, p.centery) for p in red_team]
        }
        
        # Some audience members cheer
        for i in range(len(audience)):
            if random.random() < 0.3:  # 30% chance to cheer
                audience[i] = (audience[i][0], audience[i][1], audience[i][2], 1)
        
        # Play cheer sound
        if cheer_sound:
            cheer_sound.play()
        
        return "set_piece", set_piece_type, set_piece_team, set_piece_timer, set_piece_start_positions, goal_timer, blue_score, red_score
    
    return "in_play", None, None, 0, {"blue": [], "red": []}, 0, blue_score, red_score

def execute_set_piece(ball, ball_vel, blue_team, red_team, set_piece_team):
    """Handle set piece - wait for team to touch the ball before restarting play"""
    # Ball stays completely stopped during set piece
    ball_vel[0], ball_vel[1] = 0, 0

    # Only allow the team with possession to restart play by touching the ball
    if set_piece_team == "blue":
        allowed_players = blue_team
    else:
        allowed_players = red_team

    # Check if any player from the possessing team has touched the ball
    for player in allowed_players:
        # Check collision between player and ball
        if player.colliderect(ball):
            # Player touched ball - resume normal play
            print(f"Set piece ended! {set_piece_team} team player touched ball - play resumed")

            # Give the ball a small initial movement to restart play
            if set_piece_team == "blue":
                ball_vel[0] = random.uniform(1, 3)
                ball_vel[1] = random.uniform(-2, 2)
            else:
                ball_vel[0] = random.uniform(-3, -1)
                ball_vel[1] = random.uniform(-2, 2)

            return True

    return False