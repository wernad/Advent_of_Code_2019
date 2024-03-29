import intcode_computer as ic
from collections import defaultdict

puzzle_input = ic.load_input('13')

arcade = ic.IntcodeComputer(puzzle_input)
arcade.process_intcode()
arcade_output = arcade.output

count = 0
for i in range(2, len(arcade_output), 3):
    if arcade_output[i] == 2:
        count += 1

print('Part 1:', count)

puzzle_input[0] = 2
arcade.restart(puzzle_input)
arcade.toggle_feedback()

ball_pos = None
paddle_pos = None
score = 0
arcade.input = [0]
while arcade.turned_on:
    arcade.process_intcode()
    x = arcade.output[-1]

    arcade.process_intcode()
    y = arcade.output[-1]
    
    arcade.process_intcode()
    tile_id = arcade.output[-1]
    
    if tile_id == 3:
        paddle_pos = x
    elif tile_id == 4:
        ball_pos = x
    
    arcade.input = [0]
    if ball_pos != None and paddle_pos != None:
        if ball_pos < paddle_pos:
            arcade.input = [-1]
        elif ball_pos > paddle_pos:
            arcade.input = [1]
        ball_pos = None
    
    if x == -1 and y == 0:
        score = tile_id

print('Part 2:', score)