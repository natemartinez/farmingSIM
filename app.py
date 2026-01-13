from flask import Flask, render_template, request, jsonify, session
import random
from database import FarmDatabase
from game_models import CropType, AnimalType, BuildingType, GameEconomy

app = Flask(__name__)
app.secret_key = 'farming_simulation_secret_key'
db = FarmDatabase()


@app.route('/')
def home():
    # Initialize or get user
    if 'user_id' not in session:
        # Create default user for this session
        username = f"player_{random.randint(1000, 9999)}"
        user_id = db.create_user(username)
        if not user_id:
            user_id = db.get_user_id(username)
        session['user_id'] = user_id

    user_id = session['user_id']

    # Get game state from database
    game_state = db.get_game_state(user_id)
    if not game_state:
        game_state = {
            'gold': 100,
            'wood': 50,
            'stone': 25,
            'food': 0,
            'seeds': 10,
            'water': 100,
            'day': 1,
            'season': 'Spring',
            'farm_level': 1,
            'land_size': 100
        }
        db.update_game_state(user_id, game_state)

    # Get grid placements
    placements = db.get_grid_placements(user_id)

    # Get animals
    animals = db.get_animals(user_id)
    if not animals:
        animals = {'cow': 0, 'chicken': 0, 'sheep': 0, 'pig': 0, 'horse': 0}

    resources = {
        'gold': game_state['gold'],
        'wood': game_state['wood'],
        'stone': game_state['stone'],
        'food': game_state['food'],
        'seeds': game_state['seeds'],
        'water': game_state['water']
    }

    game_info = {
        'day': game_state['day'],
        'season': game_state['season'],
        'farm_level': game_state['farm_level'],
        'land_size': game_state['land_size']
    }

    # Get all available items for the UI
    crops = CropType.get_all_crops()
    animals_data = AnimalType.get_all_animals()
    buildings = BuildingType.get_all_buildings()

    return render_template('index.html',
                         resources=resources,
                         animals=animals,
                         game_info=game_info,
                         placements=placements,
                         crops=crops,
                         animals_data=animals_data,
                         buildings=buildings)


@app.route('/api/place_object', methods=['POST'])
def place_object():
    """API endpoint to place an object on the grid"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'error': 'No user session'})

        data = request.json
        grid_x = data.get('grid_x')
        grid_y = data.get('grid_y')
        object_type = data.get('object_type')  # 'crop', 'animal', 'building'
        object_name = data.get('object_name')

        # Get current game state
        game_state = db.get_game_state(user_id)
        resources = {
            'gold': game_state['gold'],
            'wood': game_state['wood'],
            'stone': game_state['stone'],
            'food': game_state['food'],
            'seeds': game_state['seeds'],
            'water': game_state['water']
        }

        # Get object data and check costs
        cost = {}
        land_required = 1

        if object_type == 'crop':
            crop_data = CropType.get_crop(object_name)
            if not crop_data:
                return jsonify({'success': False, 'error': 'Invalid crop type'})
            cost = crop_data['cost']
            land_required = crop_data['land_required']

        elif object_type == 'animal':
            animal_data = AnimalType.get_animal(object_name)
            if not animal_data:
                return jsonify({'success': False, 'error': 'Invalid animal type'})
            cost = animal_data['cost']
            land_required = animal_data['land_required']

        elif object_type == 'building':
            building_data = BuildingType.get_building(object_name)
            if not building_data:
                return jsonify({'success': False, 'error': 'Invalid building type'})
            cost = building_data['cost']
            land_required = building_data['land_required']

        # Check if player can afford
        if not GameEconomy.can_afford(resources, cost):
            return jsonify({'success': False, 'error': 'Insufficient resources'})

        # Check land availability
        placements = db.get_grid_placements(user_id)
        land_used = GameEconomy.calculate_land_usage(placements)
        if land_used + land_required > game_state['land_size']:
            return jsonify({'success': False, 'error': 'Insufficient land'})

        # Deduct cost
        resources = GameEconomy.deduct_cost(resources, cost)

        # Save placement
        placement_data = {
            'land_required': land_required,
            'planted_day': game_state['day']
        }
        db.save_grid_placement(user_id, grid_x, grid_y, object_type, object_name, placement_data)

        # Update resources
        game_state['gold'] = resources['gold']
        game_state['wood'] = resources['wood']
        game_state['stone'] = resources['stone']
        game_state['food'] = resources['food']
        game_state['seeds'] = resources['seeds']
        game_state['water'] = resources['water']
        db.update_game_state(user_id, game_state)

        # If animal, update animal count
        if object_type == 'animal':
            animals = db.get_animals(user_id)
            current_count = animals.get(object_name, 0)
            db.update_animals(user_id, object_name, current_count + 1)

        return jsonify({
            'success': True,
            'resources': resources,
            'placement': {
                'grid_x': grid_x,
                'grid_y': grid_y,
                'object_type': object_type,
                'object_name': object_name
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/remove_object', methods=['POST'])
def remove_object():
    """API endpoint to remove an object from the grid"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'error': 'No user session'})

        data = request.json
        grid_x = data.get('grid_x')
        grid_y = data.get('grid_y')

        db.remove_grid_placement(user_id, grid_x, grid_y)

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/get_state', methods=['GET'])
def get_state():
    """API endpoint to get current game state"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'error': 'No user session'})

        game_state = db.get_game_state(user_id)
        placements = db.get_grid_placements(user_id)
        animals = db.get_animals(user_id)

        return jsonify({
            'success': True,
            'game_state': game_state,
            'placements': placements,
            'animals': animals
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/save_game', methods=['POST'])
def save_game():
    """API endpoint to manually save the game"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'error': 'No user session'})

        # Game is auto-saved with every action, so this just confirms
        return jsonify({'success': True, 'message': 'Game saved successfully'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/calculate_economy', methods=['GET'])
def calculate_economy():
    """API endpoint to calculate daily revenue and expenses"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'error': 'No user session'})

        animals = db.get_animals(user_id)
        placements = db.get_grid_placements(user_id)

        # Get building types from placements
        buildings = [p['object_name'] for p in placements if p['object_type'] == 'building']

        revenue = GameEconomy.calculate_daily_revenue({}, animals, buildings)
        expenses = GameEconomy.calculate_daily_expenses(animals)
        net_income = revenue - expenses

        return jsonify({
            'success': True,
            'revenue': revenue,
            'expenses': expenses,
            'net_income': net_income
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/api/harvest_crop', methods=['POST'])
def harvest_crop():
    """API endpoint to harvest a crop"""
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'success': False, 'error': 'No user session'})

        data = request.json
        grid_x = data.get('grid_x')
        grid_y = data.get('grid_y')

        # Get the placement
        placements = db.get_grid_placements(user_id)
        crop_placement = None
        for p in placements:
            if p['grid_x'] == grid_x and p['grid_y'] == grid_y and p['object_type'] == 'crop':
                crop_placement = p
                break

        if not crop_placement:
            return jsonify({'success': False, 'error': 'No crop found at this location'})

        crop_data = CropType.get_crop(crop_placement['object_name'])
        if not crop_data:
            return jsonify({'success': False, 'error': 'Invalid crop'})

        # Check if crop is mature
        game_state = db.get_game_state(user_id)
        current_day = game_state['day']
        planted_day = crop_placement.get('planted_day', 0)
        days_grown = current_day - planted_day

        if days_grown < crop_data['growth_time']:
            return jsonify({'success': False, 'error': 'Crop not ready for harvest'})

        # Harvest the crop
        revenue = crop_data['revenue']
        game_state['gold'] += revenue
        game_state['food'] += crop_data.get('food_value', 5)

        # Remove the crop from grid
        db.remove_grid_placement(user_id, grid_x, grid_y)

        # Update game state
        db.update_game_state(user_id, game_state)

        return jsonify({
            'success': True,
            'revenue': revenue,
            'resources': {
                'gold': game_state['gold'],
                'food': game_state['food']
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
