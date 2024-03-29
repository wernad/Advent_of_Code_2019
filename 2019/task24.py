from copy import deepcopy

with open('puzzle_input/input24.txt') as file:
    puzzle_input = [pos for line in file.readlines() for pos in list(line.strip('\n'))]

def add_tuples(a,b):
    return tuple([i + j for i, j in zip(a, b)])

#Cellular automaton that stops when a layout repeats for the first time.
def find_layout(initial_layout):
    global directions, SQUARE_SIDE
    current_layout = initial_layout
    layouts = set()
    layouts.add(tuple(initial_layout))

    while True:
        new_layout = []
        for y in range(SQUARE_SIDE):
            for x in range(SQUARE_SIDE):

                neighbourhood = 0
                for i in directions:
                    if add_tuples(i, (x,y)) in current_layout:
                        neighbourhood += 1
                        
                if ((x,y) in current_layout and neighbourhood == 1) or ((x,y) not in current_layout and neighbourhood in {1,2}):
                    new_layout.append((x,y))

        new_layout = tuple(new_layout)
        if new_layout in layouts:
            return new_layout

        layouts.add(new_layout)
        current_layout = new_layout

#Cellular automaton which works on multiple layer, each layer is a key in a dictionary.
def calc_infestation(initial_layout):
    center = (2,2)
    left_center = (1,2)
    right_center = (3,2)
    top_center = (2,1)
    bottom_center = (2,3)

    #Used to check cells that are neighbours of inner/deeper layer.
    outer2inner = {
        left_center : list(zip([0]*5, range(5))),
        right_center : list(zip([4]*5, range(5))),
        top_center : list(zip(range(5), [0]*5)),
        bottom_center : list(zip(range(5), [4]*5))
    }

    global directions, SQUARE_SIDE
    layers = {0: initial_layout}

    for _ in range(200):
        #Variables that constrain how far we check each iteration. No need to check two empty layers.
        min_level, max_level = min(layers.keys()), max(layers.keys())
        if layers[min_level]:
            layers[min_level - 1] = []
            min_level -= 1
        if layers[max_level]:
            layers[max_level + 1] = []
            max_level += 1
        
        new_layers = dict()
        for level, layout in layers.items():
            new_layout = []
            for y in range(SQUARE_SIDE):
                for x in range(SQUARE_SIDE):
                    if (x,y) == center: #Inner layer position.
                        continue

                    neighbourhood = 0
                    for d in directions:
                        neighbour = add_tuples(d, (x,y))
                        if neighbour in layout and neighbour != center:
                            neighbourhood += 1

                    #Check inner cells of outer layer.     
                    if level != min_level:
                        if x == 0 and left_center in layers[level - 1]:
                            neighbourhood += 1
                        elif x == 4 and right_center in layers[level - 1]:
                            neighbourhood += 1
                        if y == 0 and top_center in layers[level - 1]:
                            neighbourhood += 1
                        elif y == 4 and bottom_center in layers[level - 1]:
                            neighbourhood += 1

                    #Check outer cells of inner layer.
                    if (x,y) in {(1,2), (3,2), (2,1), (2,3)} and level != max_level:
                        for inner_neighbour in outer2inner[(x,y)]:
                            if inner_neighbour in layers[level + 1]:
                                neighbourhood += 1

                    if ((x,y) in layout and neighbourhood == 1) or ((x,y) not in layout and neighbourhood in {1,2}):
                        new_layout.append((x,y))            
                        
            new_layers[level] = new_layout
        layers = new_layers
    return sum([len(layout) for layout in layers.values()])


directions = [(1,0), (-1,0), (0,1), (0,-1)]
SQUARE_SIDE = 5

initial_layout = []
for y in range(5):
    for x in range(5):
        if puzzle_input.pop(0) == '#':
            initial_layout.append((x,y))

first_duplicate = find_layout(initial_layout)

powers_of_two = []
for y in range(5):
    for x in range(5):
        if (x,y) in first_duplicate:
            powers_of_two.append(2**(x+y*SQUARE_SIDE))

print('Part 1:', sum(powers_of_two))
print('Part 2:', calc_infestation(initial_layout))