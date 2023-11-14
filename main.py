from algorithms import AStar, Dfs, IterativeDfs
from taquin import Taquin
import time


algorithmMap = {
    1: AStar,
    2: Dfs,
    3: IterativeDfs,
}

def main():
    global algorithmMap

    size = int(input('Board Size: '))
    timeout = int(input('Timeout in seconds: '))

    taquin = Taquin(size)
    taquin.shuffle_board(100)

    for idx, alg in algorithmMap.items():
        print(f"{idx}. {alg.__NAME__}")

    idx = int(input('>>> '))

    solver = algorithmMap[idx](taquin, True)

    print(taquin)
    print("Started")
    start = time.time()
    path = solver.solve(timeout)
    duration = time.time() - start
    
    if path is None:
        path = []
        print("Could not solve board")
    
    for p in path:
        print(p)
    
    print(f"Solved in {duration} seconds.")

if __name__ == "__main__":
    main()