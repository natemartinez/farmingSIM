import sqlite3
import json
from datetime import datetime

class FarmDatabase:
    def __init__(self, db_name='farm_game.db'):
        self.db_name = db_name
        self.init_database()

    def get_connection(self):
        """Create a database connection"""
        return sqlite3.connect(self.db_name)

    def init_database(self):
        """Initialize the database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # User profiles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Game state table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_state (
                state_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                gold INTEGER DEFAULT 100,
                wood INTEGER DEFAULT 50,
                stone INTEGER DEFAULT 25,
                food INTEGER DEFAULT 0,
                seeds INTEGER DEFAULT 10,
                water INTEGER DEFAULT 100,
                day INTEGER DEFAULT 1,
                season TEXT DEFAULT 'Spring',
                farm_level INTEGER DEFAULT 1,
                land_size INTEGER DEFAULT 100,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')

        # Grid placements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS grid_placements (
                placement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                grid_x INTEGER NOT NULL,
                grid_y INTEGER NOT NULL,
                object_type TEXT NOT NULL,
                object_name TEXT NOT NULL,
                growth_stage INTEGER DEFAULT 0,
                planted_day INTEGER DEFAULT 0,
                data TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')

        # Animals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS farm_animals (
                animal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                animal_type TEXT NOT NULL,
                count INTEGER DEFAULT 0,
                total_production INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')

        conn.commit()
        conn.close()

    def create_user(self, username):
        """Create a new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username) VALUES (?)', (username,))
            user_id = cursor.lastrowid

            # Initialize game state for new user
            cursor.execute('''
                INSERT INTO game_state (user_id) VALUES (?)
            ''', (user_id,))

            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()

    def get_user_id(self, username):
        """Get user ID by username"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

    def get_game_state(self, user_id):
        """Get the current game state for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT gold, wood, stone, food, seeds, water, day, season, farm_level, land_size
            FROM game_state WHERE user_id = ?
        ''', (user_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return {
                'gold': result[0],
                'wood': result[1],
                'stone': result[2],
                'food': result[3],
                'seeds': result[4],
                'water': result[5],
                'day': result[6],
                'season': result[7],
                'farm_level': result[8],
                'land_size': result[9]
            }
        return None

    def update_game_state(self, user_id, resources):
        """Update game state resources"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE game_state
            SET gold = ?, wood = ?, stone = ?, food = ?, seeds = ?, water = ?,
                day = ?, season = ?, farm_level = ?, land_size = ?, updated_at = ?
            WHERE user_id = ?
        ''', (
            resources.get('gold', 0),
            resources.get('wood', 0),
            resources.get('stone', 0),
            resources.get('food', 0),
            resources.get('seeds', 0),
            resources.get('water', 0),
            resources.get('day', 1),
            resources.get('season', 'Spring'),
            resources.get('farm_level', 1),
            resources.get('land_size', 100),
            datetime.now(),
            user_id
        ))
        conn.commit()
        conn.close()

    def save_grid_placement(self, user_id, grid_x, grid_y, object_type, object_name, data=None):
        """Save an object placement on the grid"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # First check if there's already something at this position
        cursor.execute('''
            SELECT placement_id FROM grid_placements
            WHERE user_id = ? AND grid_x = ? AND grid_y = ?
        ''', (user_id, grid_x, grid_y))

        if cursor.fetchone():
            # Update existing placement
            cursor.execute('''
                UPDATE grid_placements
                SET object_type = ?, object_name = ?, data = ?
                WHERE user_id = ? AND grid_x = ? AND grid_y = ?
            ''', (object_type, object_name, json.dumps(data) if data else None, user_id, grid_x, grid_y))
        else:
            # Insert new placement
            cursor.execute('''
                INSERT INTO grid_placements (user_id, grid_x, grid_y, object_type, object_name, data)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, grid_x, grid_y, object_type, object_name, json.dumps(data) if data else None))

        conn.commit()
        conn.close()

    def get_grid_placements(self, user_id):
        """Get all grid placements for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT grid_x, grid_y, object_type, object_name, growth_stage, planted_day, data
            FROM grid_placements WHERE user_id = ?
        ''', (user_id,))
        results = cursor.fetchall()
        conn.close()

        placements = []
        for row in results:
            placements.append({
                'grid_x': row[0],
                'grid_y': row[1],
                'object_type': row[2],
                'object_name': row[3],
                'growth_stage': row[4],
                'planted_day': row[5],
                'data': json.loads(row[6]) if row[6] else None
            })
        return placements

    def remove_grid_placement(self, user_id, grid_x, grid_y):
        """Remove an object from the grid"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM grid_placements
            WHERE user_id = ? AND grid_x = ? AND grid_y = ?
        ''', (user_id, grid_x, grid_y))
        conn.commit()
        conn.close()

    def update_animals(self, user_id, animal_type, count):
        """Update animal count for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT animal_id FROM farm_animals
            WHERE user_id = ? AND animal_type = ?
        ''', (user_id, animal_type))

        if cursor.fetchone():
            cursor.execute('''
                UPDATE farm_animals SET count = ?
                WHERE user_id = ? AND animal_type = ?
            ''', (count, user_id, animal_type))
        else:
            cursor.execute('''
                INSERT INTO farm_animals (user_id, animal_type, count)
                VALUES (?, ?, ?)
            ''', (user_id, animal_type, count))

        conn.commit()
        conn.close()

    def get_animals(self, user_id):
        """Get all animals for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT animal_type, count FROM farm_animals WHERE user_id = ?
        ''', (user_id,))
        results = cursor.fetchall()
        conn.close()

        animals = {}
        for row in results:
            animals[row[0]] = row[1]
        return animals
