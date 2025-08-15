from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = 'farming_simulation_secret_key'

# FarmObject = Crops & Animals
class FarmObject:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def to_dict(self):
        return {
            'name': self.name,
            'value': self.value,
            'type': self.__class__.__name__
        }

class Animal(FarmObject):
    def __init__(self, name, value, age):
        super().__init__(name, value)
        self.age = age
    
    def to_dict(self):
        data = super().to_dict()
        data['age'] = self.age
        return data

class Crop(FarmObject):
    def __init__(self, name, value, growth_time):
        super().__init__(name, value)
        self.growth_time = growth_time
    
    def to_dict(self):
        data = super().to_dict()
        data['growth_time'] = self.growth_time
        return data

class Tool(FarmObject):
    def __init__(self, name, value):
        super().__init__(name, value)

# Initialize farm grid in session
def get_farm_grid():
    if 'farm_grid' not in session:
        session['farm_grid'] = {}
    return session['farm_grid']

# Predefined farm objects
FARM_OBJECTS = {
    'animals': [
        {'name': 'Cow', 'value': 500, 'age': 2, 'emoji': '🐄'},
        {'name': 'Chicken', 'value': 50, 'age': 1, 'emoji': '🐔'},
        {'name': 'Pig', 'value': 200, 'age': 1, 'emoji': '🐷'},
        {'name': 'Sheep', 'value': 150, 'age': 2, 'emoji': '🐑'}
    ],
    'crops': [
        {'name': 'Wheat', 'value': 30, 'growth_time': 5, 'emoji': '🌾'},
        {'name': 'Corn', 'value': 25, 'growth_time': 7, 'emoji': '🌽'},
        {'name': 'Tomato', 'value': 15, 'growth_time': 4, 'emoji': '🍅'},
        {'name': 'Carrot', 'value': 10, 'growth_time': 3, 'emoji': '🥕'}
    ],
    'tools': [
        {'name': 'Tractor', 'value': 2000, 'emoji': '🚜'},
        {'name': 'Hoe', 'value': 50, 'emoji': '🪓'},
        {'name': 'Watering Can', 'value': 25, 'emoji': '🪣'},
        {'name': 'Shovel', 'value': 30, 'emoji': '🪣'}
    ]
}

@app.route('/')
def home():
    farm_grid = get_farm_grid()
    return render_template('index.html', farm_objects=FARM_OBJECTS, farm_grid=farm_grid)

@app.route('/add_object', methods=['POST'])
def add_object():
    data = request.get_json()
    object_type = data.get('type')
    object_name = data.get('name')
    grid_position = data.get('position')
    
    farm_grid = get_farm_grid()
    
    # Find the object definition
    object_def = None
    for category in FARM_OBJECTS.values():
        for obj in category:
            if obj['name'] == object_name:
                object_def = obj
                break
    
    if not object_def:
        return jsonify({'success': False, 'message': 'Object not found'})
    
    # Check if position is already occupied
    if str(grid_position) in farm_grid:
        return jsonify({'success': False, 'message': 'Position already occupied'})
    
    # Create the object
    if object_type == 'Animal':
        farm_obj = Animal(object_def['name'], object_def['value'], object_def['age'])
    elif object_type == 'Crop':
        farm_obj = Crop(object_def['name'], object_def['value'], object_def['growth_time'])
    else:
        farm_obj = Tool(object_def['name'], object_def['value'])
    
    # Store in grid
    farm_grid[str(grid_position)] = {
        **farm_obj.to_dict(),
        'emoji': object_def['emoji']
    }
    session['farm_grid'] = farm_grid
    
    return jsonify({'success': True, 'object': farm_grid[str(grid_position)]})

@app.route('/remove_object', methods=['POST'])
def remove_object():
    data = request.get_json()
    grid_position = data.get('position')
    
    farm_grid = get_farm_grid()
    
    if str(grid_position) in farm_grid:
        removed_object = farm_grid.pop(str(grid_position))
        session['farm_grid'] = farm_grid
        return jsonify({'success': True, 'removed': removed_object})
    
    return jsonify({'success': False, 'message': 'No object at this position'})

@app.route('/move_object', methods=['POST'])
def move_object():
    data = request.get_json()
    from_position = data.get('from_position')
    to_position = data.get('to_position')
    
    farm_grid = get_farm_grid()
    
    # Check if source position has an object
    if str(from_position) not in farm_grid:
        return jsonify({'success': False, 'message': 'No object at source position'})
    
    # Check if destination position is already occupied
    if str(to_position) in farm_grid:
        return jsonify({'success': False, 'message': 'Destination position already occupied'})
    
    # Move the object
    object_data = farm_grid.pop(str(from_position))
    farm_grid[str(to_position)] = object_data
    session['farm_grid'] = farm_grid
    
    return jsonify({'success': True, 'object': object_data})

@app.route('/get_grid')
def get_grid():
    return jsonify(get_farm_grid())       

if __name__ == '__main__':
    app.run(debug=True)
