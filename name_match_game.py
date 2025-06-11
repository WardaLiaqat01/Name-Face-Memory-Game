#!/usr/bin/env python3
"""
Name Match Memory Game - A CLI game to help users remember people's names and faces.
"""

import os
import random
import json
import argparse
from datetime import datetime
import time
from typing import Dict, List, Tuple

class NameMatchGame:
    """Main game class for the Name Match Memory Game."""
    
    def __init__(self, data_file: str = "people_data.json"):
        """Initialize the game with data file path."""
        self.data_file = data_file
        self.people_data = self._load_data()
        self.stats = self._load_stats()
    
    def _load_data(self) -> List[Dict]:
        """Load people data from JSON file or return empty list if file doesn't exist."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error reading {self.data_file}. Starting with empty data.")
                return []
        return []
    
    def _save_data(self) -> None:
        """Save people data to JSON file."""
        with open(self.data_file, 'w') as f:
            json.dump(self.people_data, f, indent=2)
    
    def _load_stats(self) -> Dict:
        """Load game statistics from file or create new stats."""
        stats_file = "game_stats.json"
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {"games_played": 0, "correct_answers": 0, "total_questions": 0}
        return {"games_played": 0, "correct_answers": 0, "total_questions": 0}
    
    def _save_stats(self) -> None:
        """Save game statistics to file."""
        stats_file = "game_stats.json"
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
    
    def add_person(self, name: str, image_path: str) -> None:
        """Add a new person to the database."""
        # Check if image file exists
        if not os.path.exists(image_path):
            print(f"Error: Image file '{image_path}' not found.")
            return
        
        # Check if person already exists
        for person in self.people_data:
            if person["name"].lower() == name.lower():
                print(f"{name} already exists in the database.")
                return
        
        self.people_data.append({
            "name": name,
            "image_path": image_path,
            "added_date": datetime.now().strftime("%Y-%m-%d"),
            "times_shown": 0,
            "times_correct": 0
        })
        self._save_data()
        print(f"Added {name} to the database.")
    
    def remove_person(self, name: str) -> None:
        """Remove a person from the database."""
        initial_count = len(self.people_data)
        self.people_data = [p for p in self.people_data if p["name"].lower() != name.lower()]
        
        if len(self.people_data) < initial_count:
            self._save_data()
            print(f"Removed {name} from the database.")
        else:
            print(f"{name} not found in the database.")
    
    def list_people(self) -> None:
        """List all people in the database."""
        if not self.people_data:
            print("No people in the database yet.")
            return
        
        print("\n{:<20} {:<40} {:<15} {:<10} {:<10}".format(
            "Name", "Image Path", "Added Date", "Shown", "Correct"))
        print("-" * 95)
        
        for person in self.people_data:
            print("{:<20} {:<40} {:<15} {:<10} {:<10}".format(
                person["name"],
                person["image_path"],
                person["added_date"],
                person["times_shown"],
                person["times_correct"]
            ))
        print()
    
    def play_game(self, num_rounds: int = 5) -> None:
        """Play the name matching game with multiple choice options."""
        if len(self.people_data) < 4:
            print("You need at least 4 people in the database to play the game.")
            return
        
        num_rounds = min(num_rounds, len(self.people_data))
        score = 0
        
        # Select people for this game session, prioritizing those shown less frequently
        sorted_people = sorted(self.people_data, key=lambda x: x["times_shown"])
        game_people = sorted_people[:num_rounds]
        
        print(f"\n===== Name Match Memory Game =====")
        print(f"Match the face to the correct name!")
        print(f"You'll play {num_rounds} rounds.\n")
        
        for round_num, person in enumerate(game_people, 1):
            # Update times shown
            for p in self.people_data:
                if p["name"] == person["name"]:
                    p["times_shown"] += 1
            
            # Display question
            print(f"\nRound {round_num}/{num_rounds}")
            print(f"Who is this person? (Image: {person['image_path']})")
            
            # In a real implementation, you would display the image here
            # For CLI version, we'll just mention the image path
            
            # Generate options (3-4 name choices)
            options = [person["name"]]
            other_names = [p["name"] for p in self.people_data if p["name"] != person["name"]]
            
            # Determine number of options (3-4)
            num_options = min(4, len(self.people_data))
            options.extend(random.sample(other_names, num_options - 1))
            random.shuffle(options)
            
            # Display options
            for idx, option in enumerate(options, 1):
                print(f"{idx}. {option}")
            
            # Get user answer
            try:
                answer = input("\nEnter the number of your answer (1-4): ")
                
                # Check if answer is a valid option number
                if answer.isdigit() and 1 <= int(answer) <= len(options):
                    user_answer = options[int(answer)-1]
                    
                    # Check answer
                    if user_answer.lower() == person["name"].lower():
                        print("✓ Correct! Well done!")
                        score += 1
                        # Update person's stats
                        for p in self.people_data:
                            if p["name"] == person["name"]:
                                p["times_correct"] += 1
                    else:
                        print(f"✗ Incorrect. The correct answer is: {person['name']}")
                else:
                    print(f"Invalid input. The correct answer is: {person['name']}")
                
                time.sleep(1)  # Brief pause between rounds
                
            except (ValueError, IndexError):
                print(f"Invalid input. The correct answer is: {person['name']}")
        
        # Update game stats
        self.stats["games_played"] += 1
        self.stats["correct_answers"] += score
        self.stats["total_questions"] += num_rounds
        
        # Save updated data
        self._save_data()
        self._save_stats()
        
        # Show final score
        print("\n===== Game Over =====")
        print(f"Your final score: {score}/{num_rounds}")
        print(f"Accuracy: {(score/num_rounds)*100:.1f}%")
        
        if score == num_rounds:
            print("Perfect score! Amazing memory!")
        elif score >= num_rounds * 0.8:
            print("Great job! You're getting good at this!")
        elif score >= num_rounds * 0.6:
            print("Not bad! Keep practicing!")
        else:
            print("Keep practicing! You'll get better with time.")
    
    def show_stats(self) -> None:
        """Display game statistics."""
        print("\n===== Game Statistics =====")
        print(f"Games played: {self.stats['games_played']}")
        print(f"Total questions: {self.stats['total_questions']}")
        print(f"Correct answers: {self.stats['correct_answers']}")
        
        if self.stats['total_questions'] > 0:
            accuracy = (self.stats['correct_answers'] / self.stats['total_questions']) * 100
            print(f"Overall accuracy: {accuracy:.1f}%")
        
        # Show individual person stats
        if self.people_data:
            print("\n===== Individual Statistics =====")
            sorted_people = sorted(
                self.people_data,
                key=lambda x: x["times_correct"]/max(1, x["times_shown"]),
                reverse=True
            )
            
            print("{:<20} {:<10} {:<10} {:<10}".format("Name", "Shown", "Correct", "Accuracy"))
            print("-" * 50)
            
            for person in sorted_people:
                if person["times_shown"] > 0:
                    accuracy = (person["times_correct"] / person["times_shown"]) * 100
                    print("{:<20} {:<10} {:<10} {:<10.1f}%".format(
                        person["name"],
                        person["times_shown"],
                        person["times_correct"],
                        accuracy
                    ))
                else:
                    print("{:<20} {:<10} {:<10} {:<10}".format(
                        person["name"], "0", "0", "N/A"
                    ))

def main():
    """Main function to run the Name Match Memory Game."""
    parser = argparse.ArgumentParser(description="Name Match Memory Game")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Add person command
    add_parser = subparsers.add_parser("add", help="Add a new person")
    add_parser.add_argument("name", help="Person's name")
    add_parser.add_argument("image_path", help="Path to the person's image")
    
    # Remove person command
    remove_parser = subparsers.add_parser("remove", help="Remove a person")
    remove_parser.add_argument("name", help="Person's name to remove")
    
    # List people command
    subparsers.add_parser("list", help="List all people")
    
    # Play game command
    play_parser = subparsers.add_parser("play", help="Play the name matching game")
    play_parser.add_argument("-r", "--rounds", type=int, default=5,
                            help="Number of rounds to play (default: 5)")
    
    # Show stats command
    subparsers.add_parser("stats", help="Show game statistics")
    
    args = parser.parse_args()
    game = NameMatchGame()
    
    if args.command == "add":
        game.add_person(args.name, args.image_path)
    elif args.command == "remove":
        game.remove_person(args.name)
    elif args.command == "list":
        game.list_people()
    elif args.command == "play":
        game.play_game(args.rounds)
    elif args.command == "stats":
        game.show_stats()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
