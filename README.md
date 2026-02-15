# Words Guessing Game - Pygame UI Version

A Wordle-style word guessing game with a graphical user interface built using Pygame.

## Features

- **Wordle-inspired visual design** with color-coded feedback
- **Dual input system**: Use physical keyboard or on-screen virtual keyboard
- **Customizable difficulty**: Choose attempts (1-10) and word length (3-11)
- **Color-coded feedback**:
  - Green: Letter in correct position
  - Yellow: Letter in word but wrong position
  - Gray: Letter not in word
- **Virtual keyboard tracking**: See which letters you've tried and their status

## Requirements

- Python 3.9+
- pygame

## Installation

```bash
pip install words_guessing_game_banbar1
```
+

## How to Run

After installing the package, create a file (e.g. `run_game.py`) with:
```python
from words_guessing_game_banbar1.main_game_func import main

if __name__ == "__main__":
    main()
```

Then run it:
```bash
python run_game.py
```

## How to Play

1. **Setup Screen**:
   - Select the number of attempts (1-10)
   - Select word length (3-11 characters)
   - Click "START GAME"

2. **Game Screen**:
   - Type your guess using your keyboard OR click letters on the virtual keyboard
   - Press ENTER or click "SUBMIT" to submit your guess
   - Watch the color-coded feedback:
     - Green tiles: Correct letter in correct position
     - Yellow tiles: Correct letter in wrong position
     - Gray tiles: Letter not in the word
   - Press ESC to restart the game

3. **End Screen**:
   - See your final result (Win or Lose)
   - View the correct word
   - Click "PLAY AGAIN" to start a new game
   - Click "EXIT" to quit

## Game Rules

- Words must be exactly the length you selected
- Words must contain only English letters (A-Z)
- Words must be in the English dictionary
- You have a limited number of attempts based on your selection

## Controls

### Physical Keyboard:
- **A-Z**: Type letters
- **BACKSPACE**: Delete last letter
- **ENTER**: Submit guess
- **ESC**: Return to setup screen

### Mouse:
- Click on virtual keyboard letters
- Click "SUBMIT" button to submit guess
- Click "back arrow" button to delete last letter

## File Structure

```
FirstGame/
├── pyproject.toml
├── README.md
├── src/
│   └── words_guessing_game_banbar1/
│       ├── __init__.py
│       ├── main_game_func.py       # Main game logic and entry point
│       ├── run_game.py             # Launcher script
│       ├── words.txt               # English word dictionary
│       ├── ui/                     # UI components
│       │   ├── __init__.py
│       │   ├── constants.py        # Colors, dimensions, fonts
│       │   ├── ui_components.py    # Reusable UI components
│       │   ├── setup_screen.py     # Setup screen
│       │   ├── game_screen.py      # Main game screen
│       │   └── end_screen.py       # Win/loss screen
│       └── functions/              # Game logic
│           ├── __init__.py
│           ├── find.py             # Word finding and matching
│           ├── validation.py       # Input validation
│           ├── word_loader.py      # Dictionary loader
│           ├── print.py            # Console output helpers
│           └── UserInputIntReader.py
└── tests/
    ├── conftest.py
    ├── test_game_logic.py
    └── test_game_manager.py
```

## Technical Notes

- Screen size: 600x800 pixels
- FPS: 60
- Word dictionary is bundled as `words.txt` inside the package

## Tips

- Start with easier settings (6 attempts, 5-letter words) to get familiar with the game
- Watch the virtual keyboard to track which letters you've already tried
- Common letters like E, A, R, I, O, T are good starting guesses

## Troubleshooting

**Issue**: Game window doesn't open
- Make sure pygame is installed: `pip install pygame`
- Check that your Python version is 3.9 or higher

**Issue**: "Word not in dictionary" error for common words
- The game uses a bundled English word list (`words.txt`)

## Credits

Created using:
- **Pygame**: Game framework
- Inspired by Wordle
