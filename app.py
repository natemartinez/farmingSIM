from flask import Flask, render_template, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = 'farming_simulation_secret_key'


class Farm: 
    def __init__(self, gold, wood, stone, name):
        self.gold = gold
        self.wood = wood
        self.stone = stone
        self.name = name
        pass
class Animal: 
    def __init__(self, name, age, gender, production):
        self.name = name
        self.age = age
        self.gender = gender
        self.production = production # amount each animal produce
        pass

    def produce(self, item, amount):
        self.item = item
        self.amount = amount




@app.route('/')
def home():
    if 'farm_resources' not in session:
        session['farm_resources'] = {
            'gold': 100,
            'wood': 50,
            'stone': 25,
            'food': 0,
            'seeds': 10,
            'water': 100
        } # Stores these values in the web session
    
    if 'farm_animals' not in session:
        session['farm_animals'] = {
            'cows': 0,
            'chickens': 0,
            'sheep': 0
        }
    
    if 'game_info' not in session:
        session['game_info'] = {
            'day': 1,
            'season': 'Spring',
            'farm_level': 1
        }
    
    return render_template('index.html', 
                         resources=session['farm_resources'],
                         animals=session['farm_animals'],
                         game_info=session['game_info'])

if __name__ == '__main__':
    app.run(debug=True)
