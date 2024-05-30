# Game Project

This is a game project built using Python and Pygame library. The game consists of various classes and modules to create a playable game environment.

## Installation

1. **Python**: Make sure you have Python installed. You can download it from [here](https://www.python.org/downloads/).

2. **Pygame**: This project uses Pygame library. You can install it via pip:

    ```
    pip install pygame
    ```

3. **Other Requirements**: Some images and audio files are required for the game. Make sure to place them in the appropriate directories: 
- audio files: package audio 
- img files: package img

## Usage

To run the game, execute the main Python script:

```
python main.py
```

### Controls

- **A, D keys** move character left, right
- **Spacebar**: Shoot
- **Mouse**: Menu navigation
- **Esc**: Exit game

### Gameplay

- Navigate through different levels by reaching the exit.
- Avoid obstacles and enemies - colliding with them hurts you!
- Collect diamonds for points.
- Shoot enemies to eliminate them.
- **Enemy types:** enemies with a red skull shoot faster and have more health points. Purple ones are even more deadly! However, killing them may reward you with more points and HP.
- Change the default configuration of game parameters in `config.py`.

To win enter the last exit (currently two maps)

### Notes

- level data (stored in `levelx_data.csv`) contain arrays of ints. Each number represents a different file (where -1 means no file). Refer to `world.py` for details.
- Ensure that all necessary files, including images and audio, are in the correct directories for the game to run smoothly.
- Customize game settings and behavior by modifying the appropriate constants and parameters in the code.

