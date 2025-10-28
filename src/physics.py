"""
Physics Module
Handles player movement, ball physics, collisions, and AI behavior.
"""

import pygame
import math
import random
import sys
import os

# Import from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from game_config import *

def reset_team_positions(team, is_red_team=False):
    """Reset a team to their original starting positions"""
    if is_red_team:
        # Red team starting positions (right side)
        for i, player in enumerate(team):
            player.x = FIELD_X + FIELD_WIDTH - 70
            player.y = FIELD_Y + 150 + i*150
    else:
        # Blue team starting positions (left side)
        for i, player in enumerate(team):
            player.x = FIELD_X + 50
            player.y = FIELD_Y + 150 + i*150

def reset_positions(ball, ball_vel, blue_team, red_team):
    """Reset ball and players after goal"""
    ball.x = WIDTH//2 - BALL_RADIUS
    ball.y = HEIGHT//2 - BALL_RADIUS
    ball_vel[0] = random.choice([-BALL_SPEED, BALL_SPEED])
    ball_vel[1] = random.choice([-BALL_SPEED, BALL_SPEED])
    
    # Reset player positions
    reset_team_positions(blue_team, is_red_team=False)
    reset_team_positions(red_team, is_red_team=True)

def move_ai(players, ball, is_red=False, set_piece_type=None, set_piece_team=None):
    """Simple but effective AI: chase ball and push towards opponent's goal"""
    # During set pieces, only allow AI to move if it's their team's turn
    if set_piece_type is not None:
        # Allow AI to move only during their own team's set piece (kick-off)
        if is_red and set_piece_team != "red":
            return  # Red AI stops if it's not their set piece
        elif not is_red and set_piece_team != "blue":
            return  # Blue AI stops if it's not their set piece
        # If it's their team's set piece, AI will move towards ball to restart
    
    for p in players:
        # Simple AI: go towards ball with some goal bias
        ball_distance = abs(p.centerx - ball.centerx) + abs(p.centery - ball.centery)
        
        # If close to ball, push it towards opponent's goal
        if ball_distance < 50:
            if is_red:
                # Red team pushes ball towards left (blue's goal)
                target_x = ball.x - 30
                target_y = ball.y
            else:
                # Blue team pushes ball towards right (red's goal)
                target_x = ball.x + 30
                target_y = ball.y
        else:
            # If far from ball, chase it directly
            target_x = ball.x + random.randint(-20, 20)
            target_y = ball.y + random.randint(-20, 20)
        
        # Move toward target with simple logic
        if p.centerx < target_x:
            p.x += PLAYER_SPEED - 1
        elif p.centerx > target_x:
            p.x -= PLAYER_SPEED - 1
            
        if p.centery < target_y:
            p.y += PLAYER_SPEED - 1
        elif p.centery > target_y:
            p.y -= PLAYER_SPEED - 1
            
        # Keep within field bounds
        if p.left < FIELD_X:
            p.left = FIELD_X
        if p.right > FIELD_X + FIELD_WIDTH:
            p.right = FIELD_X + FIELD_WIDTH
        if p.top < FIELD_Y:
            p.top = FIELD_Y
        if p.bottom > FIELD_Y + FIELD_HEIGHT:
            p.bottom = FIELD_Y + FIELD_HEIGHT

def handle_ball_collision(ball, ball_vel, blue_team, red_team):
    """Handle ball collision with players and walls"""
    last_touch = None
    
    # Bounce off walls with friction
    if ball.top <= FIELD_Y:
        ball.top = FIELD_Y
        ball_vel[1] = abs(ball_vel[1]) * FRICTION
    elif ball.bottom >= FIELD_Y + FIELD_HEIGHT:
        ball.bottom = FIELD_Y + FIELD_HEIGHT
        ball_vel[1] = -abs(ball_vel[1]) * FRICTION
        
    if ball.left <= FIELD_X:
        ball.left = FIELD_X
        ball_vel[0] = abs(ball_vel[0]) * FRICTION
    elif ball.right >= FIELD_X + FIELD_WIDTH:
        ball.right = FIELD_X + FIELD_WIDTH
        ball_vel[0] = -abs(ball_vel[0]) * FRICTION

    # Collision with players - improved physics
    for i, player in enumerate(blue_team + red_team):
        if player.colliderect(ball):
            # Track which team last touched the ball
            last_touch = "blue" if i < len(blue_team) else "red"
            
            # Red team passing logic
            if i >= len(blue_team):  # red player
                red_index = i - len(blue_team)
                if red_index == 0 and len(red_team) > 1:  # striker has ball
                    midfielder = red_team[1]
                    # Check if midfielder is in good position to pass (ahead and not too far in y)
                    if midfielder.centerx > ball.centerx + 50 and abs(midfielder.centery - ball.centery) < 100:
                        # Pass to midfielder
                        dx = midfielder.centerx - ball.centerx
                        dy = midfielder.centery - ball.centery
                        dist = math.sqrt(dx*dx + dy*dy)
                        if dist > 0:
                            dx /= dist
                            dy /= dist
                            ball_vel[0] = dx * BALL_SPEED * 1.2
                            ball_vel[1] = dy * BALL_SPEED * 1.2
                            print("Red team pass!")
                            continue  # Skip normal collision
            
            # Normal collision
            # Calculate direction from player to ball
            dx = ball.centerx - player.centerx
            dy = ball.centery - player.centery
            distance = max(1, math.sqrt(dx*dx + dy*dy))
            
            # Normalize direction
            dx /= distance
            dy /= distance
            
            # Apply force based on direction
            force = 1.5
            ball_vel[0] = dx * BALL_SPEED * force
            ball_vel[1] = dy * BALL_SPEED * force
            
            # Move ball outside player to prevent sticking
            overlap = PLAYER_RADIUS + BALL_RADIUS - distance
            if overlap > 0:
                ball.x += dx * overlap
                ball.y += dy * overlap
    
    return last_touch

def keep_players_in_bounds(players):
    """Keep players within field bounds"""
    for player in players:
        if player.left < FIELD_X:
            player.left = FIELD_X
        if player.right > FIELD_X + FIELD_WIDTH:
            player.right = FIELD_X + FIELD_WIDTH
        if player.top < FIELD_Y:
            player.top = FIELD_Y
        if player.bottom > FIELD_Y + FIELD_HEIGHT:
            player.bottom = FIELD_Y + FIELD_HEIGHT

def handle_player_input(keys, current_mode, blue_team, red_team):
    """Handle player input based on game mode"""
    if current_mode == "man_vs_man":
        # Manual control for blue players
        if keys[pygame.K_w]: blue_team[0].y -= PLAYER_SPEED
        if keys[pygame.K_s]: blue_team[0].y += PLAYER_SPEED
        if keys[pygame.K_a]: blue_team[0].x -= PLAYER_SPEED
        if keys[pygame.K_d]: blue_team[0].x += PLAYER_SPEED
        
        # Control for blue player 2
        if keys[pygame.K_UP]: blue_team[1].y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]: blue_team[1].y += PLAYER_SPEED
        if keys[pygame.K_LEFT]: blue_team[1].x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]: blue_team[1].x += PLAYER_SPEED
        
        # Manual control for red players
        if keys[pygame.K_i]: red_team[0].y -= PLAYER_SPEED
        if keys[pygame.K_k]: red_team[0].y += PLAYER_SPEED
        if keys[pygame.K_j]: red_team[0].x -= PLAYER_SPEED
        if keys[pygame.K_l]: red_team[0].x += PLAYER_SPEED
        
        if keys[pygame.K_u]: red_team[1].y -= PLAYER_SPEED
        if keys[pygame.K_o]: red_team[1].y += PLAYER_SPEED
        if keys[pygame.K_y]: red_team[1].x -= PLAYER_SPEED
        if keys[pygame.K_p]: red_team[1].x += PLAYER_SPEED
        
    elif current_mode == "bot_vs_man":
        # Manual control for blue players
        if keys[pygame.K_w]: blue_team[0].y -= PLAYER_SPEED
        if keys[pygame.K_s]: blue_team[0].y += PLAYER_SPEED
        if keys[pygame.K_a]: blue_team[0].x -= PLAYER_SPEED
        if keys[pygame.K_d]: blue_team[0].x += PLAYER_SPEED
        
        # Control for second blue player with arrow keys
        if keys[pygame.K_UP]: blue_team[1].y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]: blue_team[1].y += PLAYER_SPEED
        if keys[pygame.K_LEFT]: blue_team[1].x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]: blue_team[1].x += PLAYER_SPEED