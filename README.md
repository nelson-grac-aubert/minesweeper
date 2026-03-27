# minesweeper

A minesweeper game built with Python using OOP, recursive functions, and the library pygame. 
Our humorous take on predatory game design, microtransactions and ads! 

## Features

- 3 difficulty modes increasing the grid size, mine count, and decreasing the timer. 
- Mines are generated on your first click, so it will always end up on a safe spot. 
- Restart the gmae at any time.
- Amazing ads to our old projects. 
- Amazing flag skings for sale. 
- All handmade Pixel Art sprites and visual assets using Aseprite. 

## Dependencies

This project has .exe releases for Windows user : just download the binary files, unzip and play our game directly from the executable app! 

For devs : 
Our project uses Python, with the library Pygame 

``` pip install pygame ``` 

Other libraries used that do not require installation : random, os, webbrowser, math

It can be built into the .exe using the library PyInstaller

``` pip install pyinstaller ```
``` pyinstaller --onefile --noconfirm --noconsole --name "Microtransacmine" --add-data "assets;assets" --icon "assets/images/logo.ico" main.py ```

## Difficulties encountered

- First time using recursion in a practical case.
- Connect logic to graphic.

## Future improvements 

- ADD MORE ADS ON EVERY AVAILABLE SPACE. ADD POP-UP UNSKIPPABLE ADS. ADD AN ACTUAL PAYMENT PLATFORM. INCREASE OUR PRICES. ADD A BATTLE PASS SUBSCRIPTION. 
- Replace timer and difficulty banner in Game Screen with handmade assets, why not develop fully custom font for that. 
- Add more grid shapes. 
- Add more interesting game mechanics building on the classic Minesweeper rules. 

## Authors 

- Cecilia Perana : Animated ad banner, heart-shaped board
- Adrien Meinier : Tile and board logic
- Nelson Grac-Aubert : Sprites and assets, main menu