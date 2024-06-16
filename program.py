# COMP30024 Artificial Intelligence, Semester 1 2024
# Project Part A: Single Player Tetress

from .core import PlayerColor, Coord, PlaceAction, Direction, Node
from .utils import render_board
import heapq
import math
import time







class Expansion_list:

    def __init__(self) -> None:
        self.Zero = []
        self.First = []
        self.Second = []
        self.Third = []


    def get_all_expansion(self):
        return self.Zero.append(self.First).append(self.Second).append(self.Third)



class Expansion:

    def __init__(self,initial_Coord=None):
        self.Coords = []  # Initialize Coords as an empty list
        self.length = 0
        self.score = 0
        self.prev = None
        if initial_Coord:
            self.add_coord(initial_Coord)

    def add_coord (self,c: Coord):
        self.Coords.append(c)
        self.length += 1

    # inherit function to show difference. for if not in purpose
    def __eq__(self,other) -> bool:
        for c in other.Coords:
            if c not in self.Coords:
                return False
        return True
    
    # convert expansion into place action
    def get_placeAction(self) -> PlaceAction:
        if self.length == 4:
            return PlaceAction(self.Coords[0],self.Coords[1],self.Coords[2],self.Coords[3])
        
    #def __getattribute__(self, __name: str) -> heapq.Any:
        #return self.Coords


def search(
    board: dict[Coord, PlayerColor], 
    target: Coord
) -> list[PlaceAction] | None:
    """
    This is the entry point for your submission. You should modify this
    function to solve the search problem discussed in the Part A specification.
    See `core.py` for information on the types being used here.

    Parameters:
        `board`: a dictionary representing the initial board state, mapping
            coordinates to "player colours". The keys are `Coord` instances,
            and the values are `PlayerColor` instances.  
        `target`: the target BLUE coordinate to remove from the board.
    
    Returns:
        A list of "place actions" as PlaceAction instances, or `None` if no
        solution is possible.
    """

    # The render_board() function is handy for debugging. It will print out a
    # board state in a human-readable format. If your terminal supports ANSI
    # codes, set the `ansi` flag to True to print a colour-coded version!
    start_time = time.time()
    print(render_board(board, target, ansi=False))
    

    #print(render_board(board, target, ansi=False))

    # Do some impressive AI stuff here to find the solution...
    # ...
    # ... (your solution goes here!)
    # ...
    
    open_list = []
    possible_expansions = get_all_expansion(board)
    possible_actions = []
    for e in possible_expansions:
        possible_actions.append(e.get_placeAction())

    for a in possible_actions:
        node = Node(board, a, None, 0, heuristic(a, target, board))
        heapq.heappush(open_list, node)
    
    path = astar(board, target, open_list)

    
    if path:
        for p in path:
            board_update(p, board, target)
            print(render_board(board, target, ansi=False))
    
    end_time = time.time()
    print(start_time - end_time)
    # Here we're returning "hardcoded" actions as an example of the expected
    # output format. Of course, you should instead return the result of your
    # search algorithm. Remember: if no solution is possible for a given input,
    # return `None` instead of a list.
    return path

#update the board after placing an action
def board_update(action: PlaceAction, board: dict[Coord, PlayerColor], target: Coord):
    ischanged = 0

    board[action.c1] = PlayerColor.RED
    board[action.c2] = PlayerColor.RED
    board[action.c3] = PlayerColor.RED
    board[action.c4] = PlayerColor.RED

    coords = action.coords
    for c in coords:
        if c.r == target.r or c.c == target.c:
            ischanged = 1

    for c in coords:
        row_need_clear = 1
        column_need_clear = 1
        if c not in board:
            continue

        curr_c = c + Direction.Right
        while(curr_c != c):
            if curr_c not in board:
                row_need_clear = 0
                break
            curr_c += Direction.Right
        
        curr_c = c + Direction.Down
        while(curr_c != c):
            if curr_c not in board:
                column_need_clear = 0
                break
            curr_c += Direction.Down
                
        if(row_need_clear == 1):
            ischanged = 1
            curr_c = c + Direction.Right
            while(curr_c != c):
                del board[curr_c]
                curr_c += Direction.Right
        if(column_need_clear == 1):
            ischanged = 1
            curr_c = c + Direction.Down
            while(curr_c != c):
                del board[curr_c]
                curr_c += Direction.Down
        if(row_need_clear == 1 or column_need_clear == 1):
            del board[c]
        
    return ischanged



#stage1 heuristic function
#the smallest manhattan distance to any miss blocks that need to be filled to clear the target
#plus the number of missing blocks    
def heuristic(a: PlaceAction, target: Coord, board: dict[Coord, PlayerColor]):
    sub_board = board.copy()
    board_update(a, sub_board, target)
    if target not in sub_board:
        return 0

    miss_blocks = [[], []]
    get_miss_block(sub_board, target, miss_blocks)

    heuristic = 11 * 2 + 11
    row_cost, column_cost = estimate_fill_cost(target, sub_board)

    coords = []
    coords.append(a.c1)
    coords.append(a.c2)
    coords.append(a.c3)
    coords.append(a.c4)
    for c in coords:
        for m in miss_blocks[0]: 
            distance = manhattan(c, m)
            if distance > 0:
                distance -= 1
            curr_h = math.ceil(distance / 4) + row_cost    
            if curr_h <= heuristic:
                heuristic = curr_h

        for m_ in miss_blocks[1]:
            distance = manhattan(c, m_)
            if distance > 0:
                distance -= 1
            curr_h = math.ceil(distance / 4) + column_cost
            if curr_h <= heuristic:
                heuristic = curr_h

    return heuristic

def estimate_fill_cost(target: Coord, board: dict[Coord, PlayerColor]):
    row_cost = 0
    column_cost = 0

    length = 0

    curr_coord = target + Direction.Right
    while curr_coord != target:
        if curr_coord not in board:
            length += 1
        else :
            row_cost += math.ceil(length / 4)
            length = 0
        curr_coord += Direction.Right
    row_cost += math.ceil(length / 4)
    length = 0

    curr_coord = target + Direction.Down
    while curr_coord != target:
        if curr_coord not in board:
            length += 1
        else :
            column_cost += math.ceil(length / 4)
            length = 0
        curr_coord += Direction.Down
    column_cost += math.ceil(length / 4)

    return row_cost, column_cost


#get all miss blocks that need to be filled to clear the target
def get_miss_block(board: dict[Coord, PlayerColor], target: Coord, miss_blocks: list[list[Coord], list[Coord]]):
    r = target.r
    c = target.c

    #same row
    for i in range(0, 11):
        if Coord(r, i) not in board:
            miss_blocks[0].append(Coord(r,i))


    #same column
    for j in range(0, 11):
        if Coord(j, c) not in board:
            miss_blocks[1].append(Coord(j, c))

# input a board state and list all possible next steps (in a list)
def get_all_expansion(board: dict[Coord, PlayerColor]):
    reds = get_all_red(board)
    spaces = get_all_space(board, reds)   #array of Coord
    expansions = [] 
    expansion_list = Expansion_list()
    temp = []
    for space in spaces :   # use space to create a new expansion to recurse
        expension = Expansion(space)
        expand(board,expansions,expension,expansion_list)
    return expansion_list.get_all_expansion()

def continue_expansion(board: dict[Coord, PlayerColor], action: PlaceAction):
    reds = action.coords
    spaces = get_all_space(board, reds)   #array of Coord
    expansions = [] 
    expansion_list = Expansion_list()
    for space in spaces :   # use space to create a new expansion to recurse
        expension = Expansion(space)
        expand(board,expansions,expension,expansion_list)
    return expansions

def expand(board,expansions,expansion,expansion_list):
    if expansion.length == 4:
        if expansion not in expansions:
            if expansion.score == 0:
                expansion_list.Zero.append(expansion)
            elif expansion.score == 1:
                expansion_list.First.append(expansion)
            elif expansion.score == 2:
                expansion_list.Second.append(expansion)
            elif expansion.score == 3:
                expansion_list.Third.append(expansion)

            
            expansions.append(expansion)
        return


    for c in expansion.Coords:
        for d in Direction:
            new_coord = c + d  
            if new_coord not in board and new_coord not in expansion.Coords:
                new_expansion = Expansion()
                new_expansion.Coords = expansion.Coords.copy()
                new_expansion.length = expansion.length
                new_expansion.score = expansion.score
                new_expansion.add_coord(new_coord)
                if(d == expansion.prev):
                    new_expansion.score += 1
                new_expansion.prev = d
                expand(board, expansions, new_expansion,expansion_list)




def get_all_red(board: dict[Coord, PlayerColor]):
    red = []
    for key in board:
        if str(board[key]) == "RED":
            red.append(key)
    return red

def get_all_space(board,red):
    spaces = []
    for r in red:
        for d in Direction:
            if r + d not in board and r + d not in spaces:
                spaces.append(r+d)
    return spaces



#the manhattan distance
def manhattan(c1: Coord, c2: Coord):
    v = abs(c1.r - c2.r)
    if(v > (c1-c2).r):
        v = (c1-c2).r

    h = abs(c1.c - c2.c)
    if(h > (c1-c2).c):
        h = (c1-c2).c
    
    return v + h

def astar(board: dict[Coord, PlayerColor], target: Coord, open_list):
    while(len(open_list) != 0):
        current_action = heapq.heappop(open_list)
        #close_list.append(current_node)
        sub_board = current_action.board.copy()
        ischanged = board_update(current_action.position, sub_board, target)
        #print(render_board(sub_board, target, ansi=False))
        if target not in sub_board:
            #get path
            path = []
            while(current_action.parent):
                path.append(current_action.position)
                current_action = current_action.parent
            path.append(current_action.position)
            return path[::-1]

        if(ischanged == 1):
            possible_expansions = get_all_expansion(sub_board)
        elif(ischanged == 0 and current_action.parent and current_action.h < current_action.parent.h):
            possible_expansions = continue_expansion(sub_board, current_action.position)
        else:
            possible_expansions = get_all_expansion(sub_board)

        
        #possible_expansions = get_all_expansion(sub_board)
        possible_actions = []
        for e in possible_expansions:
            possible_actions.append(e.get_placeAction())

        for a in possible_actions:
            node = Node(sub_board, a, current_action, current_action.g + 1, heuristic(a, target, sub_board))
            heapq.heappush(open_list, node)

    return
               



