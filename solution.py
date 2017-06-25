assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

# 1x1 boxes in Sudoku puzzle where each box contains 1 number. boxes = ['A1', 'A2', ..., 'I9']
boxes = cross(rows, cols)

# List of list containing 9 1x1 boxes in each row of the sudoku puzzle
row_units = [cross(r, cols) for r in rows]
# List of list containing 9 1x1 boxes in each column of the sudoku puzzle
column_units = [cross(rows, c) for c in cols]
# List of list containing 9 1x1 boxes in each 3x3 box of the sudoku puzzle
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# List of 2 lists containing 9 1x1 boxes along the diagonal and anti-diagonal of the sudoku puzzle
diag_units = [[x+y for x,y in zip(rows,cols)], [x+y for x,y in zip(rows,cols[::-1])]]

unitlist = row_units + column_units + square_units + diag_units
# Dictionary for all boxes containing all its constraining units as values
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
# Dictionary for all boxes containing all its constraining boxes as values
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

# Naked Twins Concept: http://www.sudokudragon.com/tutorialnakedtwins.htm
def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    naked_twin = {}
    for unit in unitlist:
        twin_dict = {}
        for box in unit:
            if (len(values[box])==2) and (not values[box] in twin_dict):
                twin_dict[values[box]] = [box]
            elif len(values[box])==2 and (values[box] in twin_dict):
                twin_dict[values[box]].append(box)
        #print ("twin", twin_dict)

        for key in twin_dict:
            #print ("key: ", key, twin_dict[key])
            if len(twin_dict[key])==2:
                if not key in naked_twin:
                    naked_twin[key] = [unit]
                else:
                    naked_twin[key].append(unit)

    #print ("naked_twins: ", naked_twin)
    for key in naked_twin:
        for unit in naked_twin[key]:
            for box in unit:
                if values[box]!=key:
                    assign_value(values, box, values[box].replace(key[0], ''))
                    assign_value(values, box, values[box].replace(key[1], ''))
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

# This function removes possible values for a box from values list contsrained by the peers dictionary for each box
def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

# This function checks if only 1 possible value is left for any of the box in its 'values' list and assigns the same.
def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

# This puzzle iteratively works on applying the constrained methods until there is no further update to the puzzle state
def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

# This method applies DFS technique to check if a certain value assignment leads us to a solution
def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)

    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
<<<<<<< HEAD
    values = {"G7": "1234568", "G6": "9", "G5": "35678", "G4": "23678", "G3":
    "245678", "G2": "123568", "G1": "1234678", "G9": "12345678", "G8":
    "1234567", "C9": "13456", "C8": "13456", "C3": "4678", "C2": "68",
    "C1": "4678", "C7": "13456", "C6": "368", "C5": "2", "A4": "5", "A9":
    "2346", "A8": "2346", "F1": "123689", "F2": "7", "F3": "25689", "F4":
    "23468", "F5": "1345689", "F6": "23568", "F7": "1234568", "F8":
    "1234569", "F9": "1234568", "B4": "46", "B5": "46", "B6": "1", "B7":
    "7", "E9": "12345678", "B1": "5", "B2": "2", "B3": "3", "C4": "9",
    "B8": "8", "B9": "9", "I9": "1235678", "I8": "123567", "I1": "123678",
    "I3": "25678", "I2": "123568", "I5": "35678", "I4": "23678", "I7":
    "9", "I6": "4", "A1": "2468", "A3": "1", "A2": "9", "A5": "3468",
    "E8": "12345679", "A7": "2346", "A6": "7", "E5": "13456789", "E4":
    "234678", "E7": "1234568", "E6": "23568", "E1": "123689", "E3":
    "25689", "E2": "123568", "H8": "234567", "H9": "2345678", "H2":
    "23568", "H3": "2456789", "H1": "2346789", "H6": "23568", "H7":
    "234568", "H4": "1", "H5": "35678", "D8": "1235679", "D9": "1235678",
    "D6": "23568", "D7": "123568", "D4": "23678", "D5": "1356789", "D2":
    "4", "D3": "25689", "D1": "123689"}
    display(values)
    display(naked_twins(values))
=======
>>>>>>> 8ff60a0a5f261b1e4c87f3f17a3d9524ac75893c

    #naked_twins(values)
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
