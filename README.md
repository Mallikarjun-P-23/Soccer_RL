# 🏆 RoboSoccer - 2v2 Soccer Game with Performance Analysis

A comprehensive, modular soccer simulation game built with Python and Pygame, featuring three distinct game modes and advanced performance analytics.

## 🚀 Quick Start

**To play the game, simply run:**
```bash
python run_game.py
```

## 📁 Project Structure

```
socer/
├── run_game.py              # 🚀 Main launcher - RUN THIS FILE
├── socerfull.py            # 📋 Your original file (preserved as backup)
├── README.md               # 📖 Complete documentation
├── src/                    # 📂 All working source files
│   ├── main_game.py        # 🎮 Main game controller
│   ├── game_config.py      # ⚙️ Game initialization & constants
│   ├── physics.py          # 🏃 Player movement & ball physics
│   ├── game_rules.py       # ⚽ Goals, set pieces & game rules
│   ├── graphics.py         # 🎨 All rendering & drawing
│   └── data_analysis.py    # 📊 Performance tracking & reports
├── reports/                # 📈 Auto-generated comparison reports
└── performance_data/       # 📊 CSV data files for analysis
```

## 🎮 Game Features

### Three Game Modes
1. **👥 MAN vs MAN** - Both teams controlled by human players
2. **🤖 MAN vs BOT** - Human vs AI competition  
3. **🔧 BOT vs BOT** - Watch AI teams compete

### Advanced Features
- **Real-time Performance Analysis** - Frame time tracking and optimization
- **Automatic Report Generation** - Comprehensive performance comparisons
- **Professional Soccer Field** - Realistic field with proper markings
- **Set Pieces** - Corner kicks, throw-ins, goal kicks, and kick-offs
- **Audience Animation** - Cheering crowd that reacts to game events

## 🎯 Controls

### Blue Team (Left Side)
- **Player 1**: `W A S D` keys for movement
- **Player 2**: `Arrow Keys` for movement

### Red Team (Right Side) 
- **Player 1**: `I J K L` keys for movement
- **Player 2**: `U Y O P` keys for movement

### Game Controls
- **SPACE**: Pause/Resume game
- **R**: Reset game and scores
- **E**: Export performance reports immediately
- **Q**: End match and show results
- **ESC**: Return to mode selection

## 📊 Performance Analytics

The game automatically tracks and analyzes:

### Real-time Metrics
- Frame rendering time analysis
- Player movement patterns
- Ball position tracking
- Possession statistics

### Generated Reports
- **Comparison Reports** (`.txt`) - Cross-mode performance analysis
- **CSV Data Files** - Raw performance data for further analysis
- **Visual Graphs** - Time complexity and movement analysis

Reports are automatically exported to:
- `reports/` folder - Text-based comparison analysis
- `performance_data/` folder - CSV files with raw data

## 🏗️ Technical Architecture

### Modular Design
The game is split into focused modules for maintainability:

- **`game_config.py`** - All constants, colors, and pygame initialization
- **`physics.py`** - Player movement, AI behavior, and collision detection
- **`game_rules.py`** - Goal detection, set pieces, and out-of-bounds logic
- **`graphics.py`** - All rendering functions and UI elements
- **`data_analysis.py`** - Performance tracking and report generation
- **`main_game.py`** - Game loop orchestration and event handling

### Dependencies
```
pygame>=2.0.0
numpy>=1.20.0
matplotlib>=3.3.0
```

## 🎨 Game Elements

### Field Features
- Professional soccer field with proper markings
- Goal posts and penalty areas
- Center circle and corner arcs
- Animated crowd in the stands

### Physics Engine
- Realistic ball physics with friction
- Player collision detection
- Boundary checking and set piece triggers
- AI pathfinding and strategic behavior

### Set Pieces
- **Kick-offs** after goals
- **Corner kicks** when ball crosses goal line
- **Throw-ins** for sideline violations  
- **Goal kicks** for defensive clearances

## 📈 Research Applications

This game serves as a research platform for:

### Performance Analysis
- Algorithmic complexity measurement
- Real-time system optimization
- Comparative mode analysis

### AI Behavior Studies
- Multi-agent coordination
- Strategic decision making
- Human vs AI performance comparison

### Data Collection
All gameplay generates structured data for analysis:
- Player movement vectors
- Ball trajectory patterns
- Time-series performance metrics
- Possession and scoring statistics

## 🛠️ Development

### Running in Development Mode
1. Ensure all dependencies are installed
2. Navigate to project directory
3. Run: `python run_game.py`

### Module Testing
Each module can be tested independently:
```python
# Test physics module
from src.physics import move_ai, handle_ball_collision

# Test graphics module  
from src.graphics import draw_field, draw_players_and_ball

# Test data analysis
from src.data_analysis import export_performance_data
```

## 📝 Game Rules

### Scoring
- Goals are scored when ball completely crosses goal line
- Automatic celebration and crowd reaction
- Score tracking with reset functionality

### Set Pieces
- Triggered automatically when ball goes out of bounds
- Teams are repositioned automatically
- Play resumes when possessing team touches the ball

### Match Duration
- Standard match is 3 minutes
- Can be ended early with 'Q' key
- Automatic report generation at match end

## 🎯 Future Enhancements

Potential areas for expansion:
- Tournament mode with multiple matches
- Advanced AI with machine learning
- Network multiplayer support
- 3D graphics upgrade
- Mobile platform adaptation

## 🤝 Contributing

This modular architecture makes it easy to contribute:
1. Fork the repository
2. Create a feature branch
3. Modify the relevant module
4. Test your changes
5. Submit a pull request

## 📄 License

Open source - feel free to use, modify, and distribute.

---

**🎮 Ready to play? Run `python run_game.py` and enjoy the game!**
