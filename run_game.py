#!/usr/bin/env python3
"""
🚀 RoboSoccer Game Launcher
===========================

Main entry point for the modular RoboSoccer game.
Run this file to start the game!

Game Features:
- 3 Game Modes: Man vs Man, Man vs Bot, Bot vs Bot
- Real-time performance analysis
- Automatic report generation
- Professional soccer field with realistic physics

Controls:
- Blue Team: WASD (Player 1), Arrow Keys (Player 2)  
- Red Team: IJKL (Player 1), YUOP (Player 2)
- SPACE: Pause, R: Reset, E: Export Reports, ESC: Mode Select

Reports are automatically exported to:
- reports/ folder - Comparison analysis
- performance_data/ folder - CSV data files
"""

import sys
import os

# Add the src directory to Python path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Launch the RoboSoccer game"""
    print("🚀 Starting RoboSoccer...")
    print("📁 Loading modular game components...")
    
    try:
        # Import and run the main game
        from main_game import main as run_game
        print("✅ All modules loaded successfully!")
        print("🎮 Launching game window...")
        run_game()
        
    except ImportError as e:
        print(f"❌ Error importing game modules: {e}")
        print("📂 Make sure all files are in the src/ directory:")
        print("   - src/main_game.py")
        print("   - src/game_config.py") 
        print("   - src/physics.py")
        print("   - src/game_rules.py")
        print("   - src/graphics.py")
        print("   - src/data_analysis.py")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Error starting game: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()