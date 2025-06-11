# Name Match Memory Game - Web Version

A Flask web application that helps users remember people's names and faces.

## Features

- Display faces with 3-4 name options as radio buttons
- Immediate feedback on answers (correct or incorrect)
- Score tracking throughout the game
- 5 rounds per game session
- Final score and accuracy display at the end

## Installation

1. Make sure you have Python 3.6+ and Flask installed:
   ```
   pip install flask
   ```

2. Clone or download this repository

3. Add face images to the `static/images/` directory:
   - Images should be named according to the person's ID in `people_data.json`
   - For example: `alice.jpg`, `bob.jpg`, etc.

## Usage

1. Run the Flask application:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

3. Play the game by selecting the correct name for each face shown

## Data Structure

The game uses a simple JSON file (`people_data.json`) to store information about each person:

```json
[
  {
    "id": "alice",
    "name": "Alice Johnson"
  },
  {
    "id": "bob",
    "name": "Bob Smith"
  }
]
```

## Folder Structure

- `app.py`: Main Flask application
- `templates/index.html`: Game interface
- `templates/result.html`: Feedback after each answer
- `static/images/`: Directory containing face images
- `people_data.json`: Data file with person information

## Adding New People

To add new people to the game:

1. Add their information to `people_data.json` with a unique ID
2. Place their image in `static/images/` with the filename matching their ID (e.g., `john.jpg` for ID "john")

## Requirements

- Python 3.6+
- Flask
- Web browser with JavaScript enabled
