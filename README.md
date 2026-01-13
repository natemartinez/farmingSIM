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

## Technical Details

### Frontend
- Vanilla JavaScript for interactivity
-  20x20 grid generation
- Real-time cursor tracking for drag-and-drop
- Event-driven architecture
- Modal-based UI system

### Backend
- Flask web framework
- SQLite database
- RESTful API design
- Session-based user management
- Automatic database initialization
