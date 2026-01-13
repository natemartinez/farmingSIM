"""
Game models for crops, animals, and buildings with their properties
"""

class CropType:
    """Defines different crop types with their properties"""
    CROPS = {
        'wheat': {
            'name': 'Wheat',
            'icon': '🌾',
            'cost': {'gold': 10, 'seeds': 1},
            'growth_time': 3,  # days to mature
            'revenue': 25,  # gold per harvest
            'land_required': 1,  # grid cells needed
            'water_per_day': 5
        },
        'corn': {
            'name': 'Corn',
            'icon': '🌽',
            'cost': {'gold': 15, 'seeds': 1},
            'growth_time': 4,
            'revenue': 40,
            'land_required': 1,
            'water_per_day': 7
        },
        'tomato': {
            'name': 'Tomato',
            'icon': '🍅',
            'cost': {'gold': 20, 'seeds': 2},
            'growth_time': 5,
            'revenue': 60,
            'land_required': 1,
            'water_per_day': 8
        },
        'carrot': {
            'name': 'Carrot',
            'icon': '🥕',
            'cost': {'gold': 8, 'seeds': 1},
            'growth_time': 2,
            'revenue': 18,
            'land_required': 1,
            'water_per_day': 4
        },
        'pumpkin': {
            'name': 'Pumpkin',
            'icon': '🎃',
            'cost': {'gold': 30, 'seeds': 2},
            'growth_time': 6,
            'revenue': 90,
            'land_required': 4,  # 2x2 grid
            'water_per_day': 10
        },
        'strawberry': {
            'name': 'Strawberry',
            'icon': '🍓',
            'cost': {'gold': 25, 'seeds': 2},
            'growth_time': 4,
            'revenue': 70,
            'land_required': 1,
            'water_per_day': 6
        }
    }

    @staticmethod
    def get_crop(crop_type):
        """Get crop data by type"""
        return CropType.CROPS.get(crop_type)

    @staticmethod
    def get_all_crops():
        """Get all available crops"""
        return CropType.CROPS


class AnimalType:
    """Defines different animal types with their properties"""
    ANIMALS = {
        'cow': {
            'name': 'Cow',
            'icon': '🐄',
            'cost': {'gold': 150},
            'production': {'milk': 3},  # units per day
            'production_value': 15,  # gold per day
            'upkeep': 5,  # gold per day for food
            'land_required': 4,  # grid cells needed
            'food_per_day': 10
        },
        'chicken': {
            'name': 'Chicken',
            'icon': '🐔',
            'cost': {'gold': 50},
            'production': {'eggs': 1},
            'production_value': 8,
            'upkeep': 2,
            'land_required': 1,
            'food_per_day': 3
        },
        'sheep': {
            'name': 'Sheep',
            'icon': '🐑',
            'cost': {'gold': 100},
            'production': {'wool': 1},
            'production_value': 12,
            'upkeep': 3,
            'land_required': 2,
            'food_per_day': 6
        },
        'pig': {
            'name': 'Pig',
            'icon': '🐷',
            'cost': {'gold': 120},
            'production': {'meat': 2},
            'production_value': 18,
            'upkeep': 4,
            'land_required': 3,
            'food_per_day': 8
        },
        'horse': {
            'name': 'Horse',
            'icon': '🐴',
            'cost': {'gold': 200},
            'production': {},  # Utility animal, speeds up farming
            'production_value': 0,
            'upkeep': 6,
            'land_required': 4,
            'food_per_day': 12,
            'bonus': {'speed': 1.5}  # Work speed multiplier
        }
    }

    @staticmethod
    def get_animal(animal_type):
        """Get animal data by type"""
        return AnimalType.ANIMALS.get(animal_type)

    @staticmethod
    def get_all_animals():
        """Get all available animals"""
        return AnimalType.ANIMALS


class BuildingType:
    """Defines different building types with their properties"""
    BUILDINGS = {
        'house': {
            'name': 'House',
            'icon': '🏠',
            'cost': {'wood': 50, 'stone': 30, 'gold': 100},
            'land_required': 4,  # 2x2 grid
            'provides': {'housing': 1},
            'bonus': {}
        },
        'barn': {
            'name': 'Barn',
            'icon': '🏚️',
            'cost': {'wood': 75, 'stone': 50, 'gold': 150},
            'land_required': 9,  # 3x3 grid
            'provides': {'storage': 100},
            'bonus': {'animal_capacity': 5}
        },
        'well': {
            'name': 'Well',
            'icon': '⛲',
            'cost': {'stone': 100, 'gold': 50},
            'land_required': 1,
            'provides': {'water': 50},  # water per day
            'bonus': {}
        },
        'fence': {
            'name': 'Fence',
            'icon': '🪵',
            'cost': {'wood': 10},
            'land_required': 1,
            'provides': {'decoration': 1},
            'bonus': {}
        },
        'silo': {
            'name': 'Silo',
            'icon': '🏭',
            'cost': {'wood': 100, 'stone': 75, 'gold': 200},
            'land_required': 4,
            'provides': {'storage': 200},
            'bonus': {'crop_revenue': 1.2}  # 20% bonus to crop revenue
        },
        'windmill': {
            'name': 'Windmill',
            'icon': '💨',
            'cost': {'wood': 150, 'stone': 100, 'gold': 300},
            'land_required': 4,
            'provides': {'automation': 1},
            'bonus': {'production_speed': 1.5}
        }
    }

    @staticmethod
    def get_building(building_type):
        """Get building data by type"""
        return BuildingType.BUILDINGS.get(building_type)

    @staticmethod
    def get_all_buildings():
        """Get all available buildings"""
        return BuildingType.BUILDINGS


class GameEconomy:
    """Handles economic calculations"""

    @staticmethod
    def calculate_daily_revenue(crops, animals, buildings):
        """Calculate total daily revenue from all sources"""
        revenue = 0

        # Calculate animal revenue
        for animal_type, count in animals.items():
            animal_data = AnimalType.get_animal(animal_type)
            if animal_data:
                revenue += animal_data['production_value'] * count

        # Apply building bonuses
        crop_bonus = 1.0
        for building_type in buildings:
            building_data = BuildingType.get_building(building_type)
            if building_data and 'crop_revenue' in building_data.get('bonus', {}):
                crop_bonus *= building_data['bonus']['crop_revenue']

        return revenue

    @staticmethod
    def calculate_daily_expenses(animals):
        """Calculate total daily expenses (upkeep)"""
        expenses = 0

        for animal_type, count in animals.items():
            animal_data = AnimalType.get_animal(animal_type)
            if animal_data:
                expenses += animal_data['upkeep'] * count

        return expenses

    @staticmethod
    def can_afford(resources, cost):
        """Check if player has enough resources"""
        for resource, amount in cost.items():
            if resources.get(resource, 0) < amount:
                return False
        return True

    @staticmethod
    def deduct_cost(resources, cost):
        """Deduct cost from resources"""
        for resource, amount in cost.items():
            resources[resource] = resources.get(resource, 0) - amount
        return resources

    @staticmethod
    def calculate_land_usage(placements):
        """Calculate total land used"""
        return len(placements)
