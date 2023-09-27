# UI_crossroads_puzzle_maker
Helper tool for making crossroads puzzle with GUI. Exports color, position, size and direction of cars placed into JSON

Using the puzzle maker:
1. run the file
2. select colors from left panel
3. place tile with left click
4. to remove placed tiles select the light grey on the very right of the panel in the second row of colors
5. when done click save
6. the JSON file should appear in the main folder

## Limitations
- Don't try to save grids with tiles that are shorter than 2 pls
- One "car" per color
- grid needs to be in legal format for the game.. no diagonal tiles otherwise the JSON wont make sense of course


Vertical and horizontal buttons dont do anything.. so don't bother


## Requirements
The pygame libary is needed for running the maker.
To install all required modules, install them through cmd:
```
pip install -r requirements.txt
```
