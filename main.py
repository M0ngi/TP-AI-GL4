from algorithms import AStar, Dfs, IterativeDfs
from taquin import Taquin


algorithmMap = {
    1: AStar,
    2: Dfs,
    3: IterativeDfs,
}

def main():
    global algorithmMap

    size = int(input('Board Size: '))

    taquin = Taquin(size)
    taquin.shuffle_board(100)

    for idx, alg in algorithmMap.items():
        print(f"{idx}. {alg.__NAME__}")

    idx = int(input('>>> '))

    solver = algorithmMap[idx](taquin)

    print(taquin)

    path = solver.solve()
    for p in path:
        print(p)

if __name__ == "__main__":
    main()