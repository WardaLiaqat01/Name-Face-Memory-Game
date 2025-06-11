# 🧠 Name-Face Match Memory Game 🎮

A web-based memory game built with Flask that helps users learn and recall people's names and faces.  
✨ **Perfect for networking events, classrooms, or just improving your memory skills!**

## 🌟 Overview & Purpose

The **Name Match Memory Game** is designed to help users improve their ability to remember people's names by associating them with faces. This interactive web application presents users with face images and multiple name options, challenging them to select the correct match. With immediate feedback and score tracking, users can monitor their progress and gradually improve their name-face memory skills.

## 🔑 Key Features

- 🎯 **Interactive start page** with game instructions and face previews  
- ❓ **Multiple choice format** with 3-4 name options per face  
- ✔️ **Immediate feedback** on whether answers are correct or incorrect  
- 📊 **Score tracking** throughout the 5-round game session  
- 📈 **Game statistics** showing overall performance and best accuracy  
- 📱 **Responsive design** for both desktop and mobile play  
- 🛠️ **Customizable database** to add your own faces and names  

## 🎮 How the Game Works

The game uses Flask to serve web pages and manage game state through sessions:

1. The application loads people data from a JSON file containing IDs and names  
2. When a game starts, it randomly selects faces and generates multiple-choice options  
3. User selections are processed server-side to determine correctness  
4. Session variables track progress through the 5-round game  
5. Statistics are stored in a separate JSON file for persistent tracking  

```python
# Example of how a game round is generated
def get_game_round(self, num_options=4):
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
    }
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.6 or higher 🐍
- Flask 🌐

### Installation

Clone the repository or download the source code:

```bash
git clone https://github.com/yourusername/name-face-match-memory.git
cd name-face-match-memory
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install Flask:

```bash
pip install flask
```

Make sure you have face images in the `static/images/` directory.

## 🚀 Running the Game

Start the Flask application:

```bash
python app.py
```

Open your web browser and navigate to:

```
http://127.0.0.1:5000/
```

Follow the on-screen instructions to play the game.

## 📂 Folder and File Structure

```
name-match-memory-game/
├── app.py                 # Main Flask application
├── people_data.json       # Database of people with IDs and names
├── game_stats.json        # Game statistics storage
├── static/
│   └── images/            # Face images (named by person ID)
└── templates/
    ├── start.html         # Welcome/start page
    ├── index.html         # Game interface
    └── result.html        # Feedback and results page
```

## 🔍 Key Files Explained

- `app.py`: Contains the Flask application and game logic
- `people_data.json`: Stores person information in JSON format
- `game_stats.json`: Tracks game statistics across sessions
- `templates/`: Contains HTML templates for the web interface

## 👥 Adding More People/Images

To add new people to the game:

1. Add their information to `people_data.json`:

```json
[
  {
    "id": "alice",
    "name": "Alice Johnson"
  },
  {
    "id": "bob",
    "name": "Bob Smith"
  },
  {
    "id": "new_person",
    "name": "New Person Name"
  }
]
```

2. Add their image to the `static/images/` directory:
   - The image filename must match the person's ID in the JSON file
   - For example: `static/images/new_person.jpg`

3. Restart the application if it's already running.

## 🚀 Future Improvement Ideas

- 🎚️ Difficulty levels: Add easy/medium/hard modes with varying time limits
- 👤 User accounts: Allow multiple users to track their individual progress
- 📚 Learning mode: Special mode that helps users study faces before testing
- 🏷️ Custom categories: Group people by categories (colleagues, friends, etc.)
- 🔁 Spaced repetition: Implement algorithms to show faces that users struggle with more frequently
- 📱 Mobile app: Convert to a progressive web app or native mobile application
- 📊 Expanded statistics: More detailed performance analytics and learning curves
- 👥 Multiplayer mode: Compete with friends to see who has the best name-face memory

## 🤝 Contributing

Feel free to contribute to this project by submitting pull requests or suggesting new features!  
All contributions are welcome - just open an issue or submit a PR!

