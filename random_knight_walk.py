from collections import defaultdict
import random



# Exercise b) : Write a computer program that simulates the random knight’s walk.

def get_knight_moves(x: int, y: int, board_size: int = 8, blocked_squares: set[tuple[int,int]] = set(), torus: bool = False) -> list[tuple[int,int]]:
    """ 
    : Summary : Returns all valid knight moves from position (x, y) in a described chess board.
    
    : Arguments : 
        x : int = x position of the knight in the chess board. 
        y : int = y position of the knight in the chess board.
        board_size : int = square-shaped board side size (amount of squares in side). 
        blocked_squares : set[tuple[int,int]] = not available squares in the chess board. 
        torus : bool = indicator whether the chess board is normal or torus shaped.
        
    : Returns :
        list[tuple[int,int]] = a list containing all valid moves from the given set-up.
    """
    
    possible_moves : list[tuple[int,int]] = [(x+2,y+1), (x-2,y-1), (x+2,y-1), (x-2,y+1), 
                                             (x+1,y+2), (x-1,y-2), (x+1,y-2), (x-1,y+2)]
    valid_moves : list[tuple[int,int]] = []
    for mx, my in possible_moves:
        if torus:
            mx, my = ((mx - 1) % board_size) + 1, ((my - 1) % board_size) + 1
        if 1 <= mx <= board_size and 1 <= my <= board_size and (mx, my) not in blocked_squares:
            valid_moves.append((mx,my))
    return valid_moves

    
    
def simulate_knight_walk(steps: int, x: int, y: int, board_size: int = 8, blocked_squares: set[tuple[int,int]] = set(), torus: bool = False) -> dict[tuple[int,int],int]:
    """
    : Summary : Simulates a random knight's walk and returns the visited squares along with its visits; given a described chess board. 
    
    : Arguments : 
        steps : int = number of steps to simulate
        x : int = x position of the knight in the chess board. 
        y : int = y position of the knight in the chess board.
        board_size : int = square-shaped board side size (amount of squares in side). 
        blocked_squares : set[tuple[int,int]] = not available squares in the chess board. 
        torus : bool = indicator whether the chess board is normal or torus shaped.
        
    : Returns :
        dict[tuple[int,int], int] = a dictionary containing all visited squares from the given set-up, along with the number of visits taken.
    """
    
    visits : dict[tuple[int,int],int] = {}
    visits[(x,y)] = 1
    
    for i in range(steps):
        moves = get_knight_moves(x, y, board_size, blocked_squares, torus)
        if not moves:
            visits[(x,y)] = visits.get((x,y), 0) + steps + 1 - i
            break
        x, y = random.choice(moves)
        visits[(x,y)] = visits.get((x,y), 0) + 1
    return visits
    

def get_ring_distance(x: int, y: int, board_size: int = 8) -> int:
    return min(x, y, board_size - x + 1, board_size - y + 1)


def print_knight_walk_analysis(steps: int,  visits: dict[tuple[int,int],int], board_size: int = 8) -> None:
    """
    Analyzes knight walk visit density by Manhattan distance rings from center and prints it to the screen.
    
    Args:
        steps : int = number of steps to simulate
        board_size : int = square-shaped board side size (amount of squares in side). 
        visits : dict[tuple[int,int], int] = a dictionary containing all visited squares from the given set-up, along with the number of visits taken.
    """
    
    ring_data : dict[int, dict[str, int]] = defaultdict(lambda: {'squares': 0, 'visits': 0})    # this dictionary initialization avoids needing to manually create a new keys, creates default values when the key is not there 
    
    for x in range(1, board_size + 1):
        for y in range(1, board_size + 1):
            distance = get_ring_distance(x, y, board_size)   # Chebyshev distance
            ring_data[distance]['squares'] += 1
            ring_data[distance]['visits'] += visits.get((x, y), 0)


    print(f"{'Ring':>4} | {'Squares':>8} | {'Total Visits':>13} | {'Avg per Square':>16} | {'% of Steps':>11}")
    print("-" * 65)
    for dist in sorted(ring_data.keys()):
        data = ring_data[dist]
        avg = data['visits'] / data['squares']
        pct = (data['visits'] / steps) * 100
        print(f"{dist:>4} | {data['squares']:>8} | {data['visits']:>13} | {avg:>16.2f} | {pct:>10.2f}%")



def run_simulations(exercise: str, steps: list[int], starting_positions: list[tuple[tuple[int,int],str]], board_size: int = 8, blocked_squares: set[tuple[int,int]] = set(), torus: bool = False) -> None:
    
    print(f"Exercise {exercise}):\n\n")
    for s in steps:
        for (sx,sy), name in starting_positions:
            print(f"\nSimulation with {s} steps and knight starting at {name}:\n")
            v = simulate_knight_walk(s, sx, sy, board_size, blocked_squares, torus)
            print_knight_walk_analysis(s, v, board_size)
            print(f"Unique squares visited: {len(v)}.")
    print(f"\n\n")


       
# Run simulations
random.seed(2025)  # For reproducibility


# Exercise c) : Record the average number of visits to each square for a walk of 100, 10.000 and 1.000.000 steps.
# Board set-up: 8x8 board, knight stats at b1.

run_simulations(exercise="c",steps=[100, 10000, 1000000], starting_positions=[((2,1), "b1")], board_size=8, blocked_squares=set(), torus=False)

# Exercise d) : In your simulation, change the starting position from b1 to other fields such as d4 or a1.

run_simulations(exercise="d", steps=[100, 10000, 1000000], starting_positions=[((4,4), "d4"), ((1,1), "a1")], board_size=8, blocked_squares=set(), torus=False)

   
# Exercise e) : Simulate the random knight’s walk with your other piece placed on square d4. Add a second piece on e5 and discuss the results.

run_simulations(exercise="e.1", steps=[100, 10000, 1000000], starting_positions=[((2,1), "b1")], board_size=8, blocked_squares={(4,4)}, torus=False)     # d4 is blocked
run_simulations(exercise="e.2", steps=[100, 10000, 1000000], starting_positions=[   ((1,1), "a1")], board_size=8, blocked_squares={(4,4), (5,5)}, torus=False)  # d4 and e5 are blocked


# Exercise f) : Simulate the random knight’s walk with a board of size 50 × 50 for 1.000.000 steps.

run_simulations(exercise="f", steps=[100, 10000, 1000000], starting_positions=[((2,1), "b1")], board_size=50, blocked_squares=set(), torus=False)


# Exercise g) : Simulate the random knight’s walk on an 8 × 8 torus chess board.

run_simulations(exercise="g", steps=[100, 10000, 1000000], starting_positions=[((2,1), "b1")], board_size=8, blocked_squares=set(), torus=True)
