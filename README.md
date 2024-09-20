# PongPygame
## Summary
"PongPygame" is a game developed by Johnny Nguyen made using Pygame. Pygame is a Python library that helps developers create games. "PongPygame" is inspired by the original arcade game "Pong", in which the player controls a rectangle that can only move up and down. The goal of the game is to prevent the ball from reaching your side of the screen by moving the rectangle to the ball. In "PongPygame", the player is against an opponent that will try to stop the ball from going onto their side and return the ball to the player's side. When a ball successfully hits the left or right side of the screen, a point will be added and the ball will be reset to the middle of the screen. 
![{50110219-9D6C-4AAD-89B5-0059C8252CBE}](https://github.com/user-attachments/assets/aabeda9b-d552-4b50-a4c5-da1efe2e1aa1)

## Elements
"PongPygame" showcases and utilizes various essential elements of game design.  
✓ Smart Collisions  
✓ Music (By Yutaka Hirasaka)  
✓ Movement  
✓ Random Direction    
✓ Timers  
✓ Knowledge of Rects and Sprites  
✓ Objected Oriented  
✓ Score is saved  
✓ Inheritance  

## Notes
- All sides of rectangle and ball collision are working.
- Timers used to ensure the ball doesn't instantly move upon resetting.
- FPS of the game does not affect gameplay elements.  

## Controls
W - Move up    
S - Move down    

## Running
To run, Python must be installed. In addition, Pygame-ce and pytmx must be installed.   
Pygame can be installed via   
```
pip install pygame-ce  
or   
pip3 install pygame-ce  
```

Afterwards, the game can be ran using 
```
python "main.py"  
or  
python3 "main.py"  
```
