"""
Data Analysis Module
Handles performance tracking, report generation, and data export functionality.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import csv
import os
import time
import math
import pygame
from datetime import datetime
from collections import deque
import sys

# Import from the same directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from game_config import *

def initialize_data_structures():
    """Initialize all data collection structures"""
    time_data = {
        "man_vs_man": deque(maxlen=200),
        "bot_vs_man": deque(maxlen=200),
        "bot_vs_bot": deque(maxlen=200)
    }

    player_movement_data = {
        "man_vs_man": deque(maxlen=1000),
        "bot_vs_man": deque(maxlen=1000),
        "bot_vs_bot": deque(maxlen=1000)
    }

    ball_position_data = {
        "man_vs_man": deque(maxlen=1000),
        "bot_vs_man": deque(maxlen=1000),
        "bot_vs_bot": deque(maxlen=1000)
    }

    game_stats = {
        "man_vs_man": {
            "goals": 0,
            "possession_time": {"blue": 0, "red": 0},
            "shots": 0,
            "passes": 0,
            "match_duration": 0
        },
        "bot_vs_man": {
            "goals": 0,
            "possession_time": {"blue": 0, "red": 0},
            "shots": 0,
            "passes": 0,
            "match_duration": 0
        },
        "bot_vs_bot": {
            "goals": 0,
            "possession_time": {"blue": 0, "red": 0},
            "shots": 0,
            "passes": 0,
            "match_duration": 0
        }
    }
    
    return time_data, player_movement_data, ball_position_data, game_stats

def collect_research_data(ball, blue_team, red_team, current_mode, frame_count, match_start_time,
                         player_movement_data, ball_position_data, game_stats, last_touch, 
                         possession_timer, last_possession):
    """Collect player movement and ball position data for research"""
    
    # Track possession
    if last_touch:
        if last_possession != last_touch:
            # Add previous possession time
            if last_possession:
                game_stats[current_mode]["possession_time"][last_possession] += possession_timer
            possession_timer = 0
            last_possession = last_touch
        possession_timer += 1
    
    # Collect player positions
    player_data = {
        "frame": frame_count,
        "time": time.time() - match_start_time,
        "blue_players": [(p.x, p.y) for p in blue_team],
        "red_players": [(p.x, p.y) for p in red_team],
        "ball_position": (ball.x, ball.y),
        "ball_velocity": (0, 0)  # Note: ball_vel not passed to this function
    }
    
    player_movement_data[current_mode].append(player_data)
    ball_position_data[current_mode].append((ball.x, ball.y))
    
    return possession_timer, last_possession

def generate_comparison_report(time_data, game_stats, player_movement_data):
    """Generate a comprehensive comparison report in text format"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"ROBOSOCCER PERFORMANCE COMPARISON REPORT\n"
    report += f"Generated on: {timestamp}\n"
    report += "=" * 60 + "\n\n"
    
    for mode in ["man_vs_man", "bot_vs_man", "bot_vs_bot"]:
        if time_data[mode]:
            report += f"MODE: {mode.upper().replace('_', ' ')}\n"
            report += "-" * 40 + "\n"
            
            # Basic statistics
            avg_time = np.mean(time_data[mode])
            max_time = np.max(time_data[mode])
            min_time = np.min(time_data[mode])
            total_frames = len(time_data[mode])
            
            report += f"Performance Metrics:\n"
            report += f"  Average Frame Time: {avg_time:.6f} seconds\n"
            report += f"  Maximum Frame Time: {max_time:.6f} seconds\n"
            report += f"  Minimum Frame Time: {min_time:.6f} seconds\n"
            report += f"  Total Frames: {total_frames}\n"
            
            # Game statistics
            stats = game_stats[mode]
            report += f"Game Statistics:\n"
            report += f"  Total Goals: {stats['goals']}\n"
            report += f"  Blue Possession: {stats['possession_time']['blue']} frames\n"
            report += f"  Red Possession: {stats['possession_time']['red']} frames\n"
            report += f"  Match Duration: {stats['match_duration']:.2f} seconds\n"
            
            # Player movement analysis
            if player_movement_data[mode]:
                total_distance = 0
                for i in range(1, len(player_movement_data[mode])):
                    frame_data = player_movement_data[mode][i]
                    prev_frame_data = player_movement_data[mode][i-1]
                    
                    for j in range(len(frame_data["blue_players"])):
                        dx = frame_data["blue_players"][j][0] - prev_frame_data["blue_players"][j][0]
                        dy = frame_data["blue_players"][j][1] - prev_frame_data["blue_players"][j][1]
                        total_distance += math.sqrt(dx*dx + dy*dy)
                    
                    for j in range(len(frame_data["red_players"])):
                        dx = frame_data["red_players"][j][0] - prev_frame_data["red_players"][j][0]
                        dy = frame_data["red_players"][j][1] - prev_frame_data["red_players"][j][1]
                        total_distance += math.sqrt(dx*dx + dy*dy)
                
                report += f"  Total Player Distance: {total_distance:.2f} pixels\n"
            
            report += "\n"
    
    # Comparative analysis
    report += "COMPARATIVE ANALYSIS\n"
    report += "-" * 40 + "\n"
    
    modes_with_data = [mode for mode in time_data.keys() if time_data[mode]]
    if len(modes_with_data) > 1:
        # Find best performing mode (lowest average frame time)
        best_mode = min(modes_with_data, key=lambda x: np.mean(time_data[x]))
        report += f"Most Efficient Mode: {best_mode.replace('_', ' ').title()}\n"
        
        # Compare frame times
        report += "Frame Time Comparison:\n"
        for mode in modes_with_data:
            avg = np.mean(time_data[mode])
            report += f"  {mode.replace('_', ' ').title()}: {avg:.6f}s\n"
        
        # Compare game activity
        report += "Game Activity Comparison:\n"
        for mode in modes_with_data:
            goals = game_stats[mode]["goals"]
            total_possession = game_stats[mode]["possession_time"]["blue"] + game_stats[mode]["possession_time"]["red"]
            if total_possession > 0:
                blue_possession_pct = (game_stats[mode]["possession_time"]["blue"] / total_possession) * 100
                red_possession_pct = (game_stats[mode]["possession_time"]["red"] / total_possession) * 100
                report += f"  {mode.replace('_', ' ').title()}: {goals} goals, Blue {blue_possession_pct:.1f}% - Red {red_possession_pct:.1f}% possession\n"
    
    return report

def export_comparison_report(time_data, game_stats, player_movement_data):
    """Export the comparison report to a text file"""
    try:
        # Create directory if it doesn't exist
        if not os.path.exists("reports"):
            os.makedirs("reports")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/comparison_report_{timestamp}.txt"
        
        report = generate_comparison_report(time_data, game_stats, player_movement_data)
        
        with open(filename, 'w') as f:
            f.write(report)
        
        print(f"Comparison report exported to: {filename}")
        return filename
    except Exception as e:
        print(f"Error exporting comparison report: {e}")
        return None

def generate_performance_report(time_data, player_movement_data, ball_position_data):
    """Generate a performance report with graphs for all modes"""
    if not any(time_data.values()):
        return None
    
    # Create a figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Performance Analysis - All Modes', fontsize=16)
    
    colors = ['blue', 'red', 'green']
    modes = list(time_data.keys())
    
    # Time complexity subplot
    for i, mode in enumerate(modes):
        if time_data[mode]:
            axes[0, 0].plot(range(len(time_data[mode])), time_data[mode], color=colors[i], linewidth=2, label=mode)
    axes[0, 0].set_title('Time Complexity')
    axes[0, 0].set_ylabel('Time (s)')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Player movement analysis subplot
    for i, mode in enumerate(modes):
        if player_movement_data[mode]:
            # Calculate total distance traveled by all players
            total_distances = []
            for j in range(1, len(player_movement_data[mode])):
                frame_data = player_movement_data[mode][j]
                prev_frame_data = player_movement_data[mode][j-1]
                frame_distance = 0
                
                # Calculate distance for blue players
                for k in range(len(frame_data["blue_players"])):
                    dx = frame_data["blue_players"][k][0] - prev_frame_data["blue_players"][k][0]
                    dy = frame_data["blue_players"][k][1] - prev_frame_data["blue_players"][k][1]
                    frame_distance += math.sqrt(dx*dx + dy*dy)
                
                # Calculate distance for red players
                for k in range(len(frame_data["red_players"])):
                    dx = frame_data["red_players"][k][0] - prev_frame_data["red_players"][k][0]
                    dy = frame_data["red_players"][k][1] - prev_frame_data["red_players"][k][1]
                    frame_distance += math.sqrt(dx*dx + dy*dy)
                
                total_distances.append(frame_distance)
            
            if total_distances:
                axes[0, 1].plot(range(len(total_distances)), total_distances, color=colors[i], linewidth=2, label=mode)
    
    axes[0, 1].set_title('Player Movement Analysis')
    axes[0, 1].set_ylabel('Distance per Frame (pixels)')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Ball position heatmap subplot
    for i, mode in enumerate(modes):
        if ball_position_data[mode]:
            ball_x = [pos[0] for pos in ball_position_data[mode]]
            ball_y = [pos[1] for pos in ball_position_data[mode]]
            axes[1, 0].scatter(ball_x, ball_y, color=colors[i], alpha=0.5, label=mode, s=1)
    
    axes[1, 0].set_title('Ball Position Heatmap')
    axes[1, 0].set_xlabel('X Position')
    axes[1, 0].set_ylabel('Y Position')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)
    
    # Statistics subplot
    stats_data = []
    for mode in modes:
        if time_data[mode]:
            avg_time = np.mean(time_data[mode])
            max_time = np.max(time_data[mode])
            min_time = np.min(time_data[mode])
            stats_data.append([mode, avg_time, max_time, min_time])
    
    if stats_data:
        stats_labels = [f"{mode}\nAvg: {avg:.4f}s" for mode, avg, max_t, min_t in stats_data]
        stats_values = [avg for mode, avg, max_t, min_t in stats_data]
        bars = axes[1, 1].bar(stats_labels, stats_values, color=colors[:len(stats_data)])
        axes[1, 1].set_title('Average Frame Time by Mode')
        axes[1, 1].set_ylabel('Time (s)')
        
        # Add value labels on bars
        for bar, val in zip(bars, stats_values):
            height = bar.get_height()
            axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 0.0001,
                           f'{val:.4f}s', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    
    # Convert the figure to a Pygame surface
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    
    # Create Pygame surface
    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    
    plt.close(fig)
    
    return surf

def export_performance_data(time_data, player_movement_data, ball_position_data, game_stats):
    """Export performance data to CSV files"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create directory if it doesn't exist
        if not os.path.exists("performance_data"):
            os.makedirs("performance_data")
        
        # Export time complexity data
        for mode, data in time_data.items():
            if data:
                filename = f"performance_data/{mode}time{timestamp}.csv"
                with open(filename, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Frame', 'Time (s)'])
                    for i, val in enumerate(data):
                        writer.writerow([i, val])
        
        # Export player movement data
        for mode, data in player_movement_data.items():
            if data:
                filename = f"performance_data/{mode}movement{timestamp}.csv"
                with open(filename, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Frame', 'Time', 'Blue1_X', 'Blue1_Y', 'Blue2_X', 'Blue2_Y', 
                                   'Red1_X', 'Red1_Y', 'Red2_X', 'Red2_Y', 'Ball_X', 'Ball_Y'])
                    for frame_data in data:
                        row = [frame_data["frame"], frame_data["time"]]
                        for pos in frame_data["blue_players"]:
                            row.extend(pos)
                        for pos in frame_data["red_players"]:
                            row.extend(pos)
                        row.extend(frame_data["ball_position"])
                        writer.writerow(row)
        
        # Export ball position data
        for mode, data in ball_position_data.items():
            if data:
                filename = f"performance_data/{mode}ball{timestamp}.csv"
                with open(filename, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Frame', 'Ball_X', 'Ball_Y'])
                    for i, pos in enumerate(data):
                        writer.writerow([i, pos[0], pos[1]])
        
        # Export summary statistics
        summary_filename = f"performance_data/summary_{timestamp}.csv"
        with open(summary_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Mode', 'Frames', 'Avg Time (s)', 'Max Time (s)', 'Min Time (s)', 'Total Goals', 'Blue Possession', 'Red Possession'])
            
            for mode in time_data.keys():
                if time_data[mode]:
                    avg_time = np.mean(time_data[mode])
                    max_time = np.max(time_data[mode])
                    min_time = np.min(time_data[mode])
                    total_goals = game_stats[mode]["goals"]
                    blue_possession = game_stats[mode]["possession_time"]["blue"]
                    red_possession = game_stats[mode]["possession_time"]["red"]
                    writer.writerow([mode, len(time_data[mode]), avg_time, max_time, min_time, total_goals, blue_possession, red_possession])
        
        print(f"Performance data exported to performance_data/ directory with timestamp {timestamp}")
        return timestamp
    except Exception as e:
        print(f"Error exporting performance data: {e}")
        return None

def draw_performance_report(screen, report_surface, blue_score, red_score):
    """Draw the performance report on screen"""
    if report_surface:
        # Draw semi-transparent background
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 200))
        screen.blit(s, (0, 0))
        
        # Draw report
        screen.blit(report_surface, (WIDTH//2 - report_surface.get_width()//2, 
                                    HEIGHT//2 - report_surface.get_height()//2))
        
        # Draw close button
        pygame.draw.rect(screen, RED, (WIDTH//2 - 50, HEIGHT - 100, 100, 40))
        close_text = font.render("Close", True, WHITE)
        screen.blit(close_text, (WIDTH//2 - close_text.get_width()//2, HEIGHT - 100 + 20 - close_text.get_height()//2))
        
        # Draw match stats
        stats_text = font.render(f"Final Score: Blue {blue_score} - Red {red_score}", True, WHITE)
        screen.blit(stats_text, (WIDTH//2 - stats_text.get_width()//2, 20))
        
        # Draw export message
        export_text = small_font.render("Performance data and comparison report exported", True, YELLOW)
        screen.blit(export_text, (WIDTH//2 - export_text.get_width()//2, HEIGHT - 130))