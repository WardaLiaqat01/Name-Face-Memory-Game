#!/usr/bin/env python3
"""
Name Match Memory Game - Web version using Flask
"""

import os
import random
import json
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'name_match_memory_game_secret_key'  # For session management

# Configuration
DATA_FILE = 'people_data.json'
STATS_FILE = 'game_stats.json'

class NameMatchGame:
    """Main game class for the Name Match Memory Game."""
    
    def __init__(self, data_file=DATA_FILE):
        """Initialize the game with data file path."""
        self.data_file = data_file
        self.people_data = self._load_data()
        self.stats = self._load_stats()
    
    def _load_data(self):
        """Load people data from JSON file or return empty list if file doesn't exist."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    
    def _load_stats(self):
        """Load game statistics from file or create new stats."""
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {"games_played": 0, "correct_answers": 0, "total_questions": 0, "best_accuracy": 0}
        return {"games_played": 0, "correct_answers": 0, "total_questions": 0, "best_accuracy": 0}
    
    def _save_stats(self):
        """Save game statistics to file."""
        with open(STATS_FILE, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def get_people(self):
        """Return the list of people."""
        return self.people_data
    
    def get_random_people(self, count=5):
        """Return a random subset of people for display."""
        if len(self.people_data) <= count:
            return self.people_data
        return random.sample(self.people_data, count)
    
    def get_game_round(self, num_options=4):
        """Prepare a game round with a question and options."""
        if len(self.people_data) < num_options:
            return None, f"You need at least {num_options} people in the database to play the game."
        
        # Select a random person as the correct answer
        correct_person = random.choice(self.people_data)
        
        # Select other people for options (excluding the correct person)
        other_people = [p for p in self.people_data if p["id"] != correct_person["id"]]
        selected_others = random.sample(other_people, num_options - 1)
        
        # Combine correct person and others, then shuffle
        options = [correct_person] + selected_others
        random.shuffle(options)
        
        return {
            "correct_person": correct_person,
            "options": options
        }, None
    
    def get_stats(self):
        """Get game statistics."""
        return self.stats
    
    def update_stats(self, score, total_rounds):
        """Update game statistics after a game is completed."""
        self.stats["games_played"] += 1
        self.stats["correct_answers"] += score
        self.stats["total_questions"] += total_rounds
        
        # Calculate accuracy for this game
        accuracy = (score / total_rounds) * 100
        
        # Update best accuracy if this game was better
        if accuracy > self.stats["best_accuracy"]:
            self.stats["best_accuracy"] = accuracy
        
        self._save_stats()

# Create game instance
game = NameMatchGame()

@app.route('/')
def start():
    """Start page with game introduction."""
    random_people = game.get_random_people(5)
    stats = game.get_stats()
    return render_template('start.html', random_people=random_people, stats=stats)

@app.route('/game')
def index():
    """Home page - start a new game."""
    # Check if we have enough people in the database
    people = game.get_people()
    if len(people) < 4:
        return render_template('index.html', error="Need at least 4 people in the database to play.")
    
    # Initialize or reset game session
    session['current_round'] = 0
    session['score'] = 0
    session['total_rounds'] = 5
    
    # Start first round
    return redirect(url_for('play_round'))

@app.route('/play')
def play_round():
    """Play a round of the game."""
    # Get current game state
    current_round = session.get('current_round', 0)
    score = session.get('score', 0)
    total_rounds = session.get('total_rounds', 5)
    
    # Check if game is over
    if current_round >= total_rounds:
        # Update game stats before showing game over screen
        game.update_stats(score, total_rounds)
        return redirect(url_for('game_over'))
    
    # Get a new round
    round_data, error = game.get_game_round()
    if error:
        return render_template('index.html', error=error)
    
    # Increment round counter
    session['current_round'] = current_round + 1
    
    return render_template('index.html', 
                          round_data=round_data,
                          current_round=current_round + 1,
                          total_rounds=total_rounds,
                          score=score)

@app.route('/check', methods=['POST'])
def check_answer():
    """Check the user's answer and provide feedback."""
    # Get form data
    selected_id = request.form.get('selected_person')
    correct_id = request.form.get('correct_person')
    
    # Check if answer is correct
    is_correct = selected_id == correct_id
    
    # Update score if correct
    if is_correct:
        session['score'] = session.get('score', 0) + 1
    
    # Get person names for feedback
    people = game.get_people()
    selected_name = next((p['name'] for p in people if p['id'] == selected_id), "Unknown")
    correct_name = next((p['name'] for p in people if p['id'] == correct_id), "Unknown")
    
    return render_template('result.html',
                          is_correct=is_correct,
                          selected_name=selected_name,
                          correct_name=correct_name,
                          current_round=session.get('current_round', 0),
                          total_rounds=session.get('total_rounds', 5),
                          score=session.get('score', 0))

@app.route('/game_over')
def game_over():
    """Show game over screen with results."""
    score = session.get('score', 0)
    total_rounds = session.get('total_rounds', 5)
    
    # Calculate accuracy
    accuracy = 0
    if total_rounds > 0:
        accuracy = (score / total_rounds) * 100
    
    return render_template('result.html', 
                          game_over=True,
                          score=score, 
                          total_rounds=total_rounds,
                          accuracy=accuracy)

if __name__ == '__main__':
    app.run(debug=True)
