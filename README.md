# FarmingSIM - Interactive Farming Simulation Game

A comprehensive web-based farming simulation game built with Flask, featuring an interactive grid system, drag-and-drop object placement, and a complete economic system.

## Features

### Core Systems

1. **Interactive Grid System (20x20)**
   - Click-to-place object system
   - Visual feedback for valid/invalid placements
   - Hover effects showing placement preview
   - Right-click to remove objects

2. **Drag-and-Drop Functionality**
   - Click on crops, animals, or buildings from menus
   - Object follows cursor
   - Click grid cell to place
   - Press ESC to cancel placement

3. **Crop System**
   - 6 different crop types: Wheat, Corn, Tomato, Carrot, Pumpkin, Strawberry
   - Each crop has unique properties:
     - Growth time (days to mature)
     - Cost (gold + seeds)
     - Revenue on harvest
     - Water requirements per day
   - Visual growth representation on grid

4. **Animal System**
   - 5 animal types: Cow, Chicken, Sheep, Pig, Horse
   - Each animal generates daily revenue
   - Upkeep costs (food expenses)
   - Production tracking (milk, eggs, wool, etc.)
   - Space requirements on grid

5. **Building System**
   - 6 building types: House, Barn, Well, Fence, Silo, Windmill
   - Buildings provide bonuses:
     - Storage capacity increases
     - Water generation (wells)
     - Revenue multipliers (silos)
     - Production speed boosts (windmills)

6. **Economic System**
   - Real-time resource tracking: Gold, Wood, Stone, Food, Seeds, Water
   - Daily revenue calculation from animals
   - Daily expense tracking (animal upkeep)
   - Net income display
   - Resource validation before purchases

7. **Land Management**
   - 100 total land capacity (default)
   - Each object requires specific land amount
   - Cannot exceed land capacity
   - Visual representation of occupied land

8. **Database Persistence**
   - SQLite database for game state
   - User profiles with unique sessions
   - Grid placements saved
   - Resources and game progress saved
   - Auto-save on every action

9. **Tooltips**
   - Hover over placed objects for information
   - Shows object name, stats, and revenue/costs
   - Real-time information updates

## File Structure

```
farmingSIM_claude/
├── app.py                 # Main Flask application with API endpoints
├── database.py            # SQLite database management
├── game_models.py         # Crop, Animal, Building data models
├── farm_game.db          # SQLite database file (auto-created)
├── templates/
│   └── index.html        # Main game interface
├── static/
│   └── style.css         # Game styling
└── README.md             # This file
```

## Installation

1. Make sure Python 3 is installed
2. Install Flask:
   ```bash
   pip install flask
   ```

3. Run the application:
   ```bash
   cd farmingSIM_claude
   python app.py
   ```

4. Open browser to: `http://127.0.0.1:5001`

## How to Play

### Getting Started
1. The game starts with initial resources: 100 gold, 50 wood, 25 stone, 10 seeds, 100 water
2. Use the menu buttons in the bottom-right to access different menus

### Placing Objects

**Crops:**
1. Click the "Actions" menu button (🌱)
2. Select a crop type from the menu
3. Your cursor will show the crop icon
4. Click any grid cell to plant
5. Costs will be automatically deducted

**Animals:**
1. Click the "Animals" menu button (🐄)
2. Select an animal type
3. Click grid cell to place
4. Animal will generate daily revenue

**Buildings:**
1. Click the "Buildings" menu button (🏠)
2. Select a building type
3. Click grid cell to place
4. Buildings provide passive bonuses

### Removing Objects
- Right-click any placed object to remove it
- Confirm the removal dialog

### Managing Resources
- Click "Resources" menu (🪙) to view current resources
- Resources update in real-time after placements
- Check "Production" menu (📊) for revenue/expense breakdown

### Saving Game
- Game auto-saves after every action
- Click "Info" menu (ℹ️) → "Save Game" for manual save

## Game Mechanics

### Crop Economics
- Each crop has a cost (gold + seeds)
- Crops take time to grow (growth_time in days)
- Harvest provides revenue
- Example: Wheat costs 10 gold + 1 seed, grows in 3 days, sells for 25 gold

### Animal Economics
- Animals cost gold to purchase
- Generate daily production value (revenue)
- Have daily upkeep costs (expenses)
- Example: Cow costs 150 gold, produces 15 gold/day, costs 5 gold/day upkeep = 10 gold net/day

### Land Requirements
- Each object requires grid space
- Small crops/animals: 1 cell
- Large objects: 4-9 cells
- Total capacity: 100 cells
- Plan your farm layout efficiently!

### Building Bonuses
- **Barn**: Increases storage and animal capacity
- **Well**: Generates 50 water per day
- **Silo**: +20% crop revenue multiplier
- **Windmill**: +50% production speed
- **House**: Provides housing
- **Fence**: Decoration

## API Endpoints

### POST /api/place_object
Place an object on the grid
```json
{
  "grid_x": 5,
  "grid_y": 10,
  "object_type": "crop",
  "object_name": "wheat"
}
```

### POST /api/remove_object
Remove an object from the grid
```json
{
  "grid_x": 5,
  "grid_y": 10
}
```

### GET /api/get_state
Get current game state, placements, and resources

### POST /api/save_game
Manually save the game

### GET /api/calculate_economy
Get revenue, expenses, and net income calculations

### POST /api/harvest_crop
Harvest a mature crop
```json
{
  "grid_x": 5,
  "grid_y": 10
}
```

## Data Models

### Crops
- `wheat`: 10g + 1s → 3 days → 25g
- `corn`: 15g + 1s → 4 days → 40g
- `tomato`: 20g + 2s → 5 days → 60g
- `carrot`: 8g + 1s → 2 days → 18g
- `pumpkin`: 30g + 2s → 6 days → 90g (requires 4 cells)
- `strawberry`: 25g + 2s → 4 days → 70g

### Animals
- `cow`: 150g → 15g/day revenue, 5g/day upkeep, 4 cells
- `chicken`: 50g → 8g/day revenue, 2g/day upkeep, 1 cell
- `sheep`: 100g → 12g/day revenue, 3g/day upkeep, 2 cells
- `pig`: 120g → 18g/day revenue, 4g/day upkeep, 3 cells
- `horse`: 200g → 0g/day revenue, 6g/day upkeep, 4 cells (utility)

### Buildings
- `house`: 50w + 30s + 100g, 4 cells
- `barn`: 75w + 50s + 150g, 9 cells
- `well`: 100s + 50g, 1 cell
- `fence`: 10w, 1 cell
- `silo`: 100w + 75s + 200g, 4 cells
- `windmill`: 150w + 100s + 300g, 4 cells

## Technical Details

### Frontend
- Vanilla JavaScript for interactivity
- Dynamic 20x20 grid generation
- Real-time cursor tracking for drag-and-drop
- Event-driven architecture
- Modal-based UI system

### Backend
- Flask web framework
- SQLite database
- RESTful API design
- Session-based user management
- Automatic database initialization

### Database Schema
- **users**: User profiles
- **game_state**: Resources, day, season, farm level
- **grid_placements**: Object positions on grid
- **farm_animals**: Animal counts and production

## Future Enhancements

Potential features to add:
- Day/night cycle with time progression
- Seasonal effects on crops
- Weather system
- Market system for trading
- Achievements and quests
- Multiplayer features
- Mobile responsive improvements
- Sound effects and music
- Tutorial system
- Advanced building upgrades

## Controls

- **Left Click**: Select from menu / Place object / Interact
- **Right Click**: Remove object
- **ESC**: Cancel placement / Close modals
- **Hover**: View tooltips

## Credits

Built with Flask, HTML5, CSS3, and JavaScript.
Database: SQLite3

## License

Educational project - feel free to modify and enhance!
