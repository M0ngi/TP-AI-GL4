from taquin import Taquin
from .base import BaseAlgorithm
import bisect
import time


class AStar(BaseAlgorithm): 
    __NAME__ = "A* Search"

    def __init__(self, taquin: Taquin):
        self.goal = taquin.get_solution()
        
        taquin.f = 0
        taquin.g = 0
        taquin.h = 0
        taquin.cost = self.get_cost(taquin)
        
        self.taquin: Taquin = taquin
        
        self.open: list[Taquin] = []
        self.closed_map_hash: dict[str, int] = {}

    def solve(self, timeout: int = 10):
        self.open.append(self.taquin)
        start = time.time()
        while len(self.open) > 0:
            end = time.time()
            if end - start > timeout:
                print("Timed out")
                return None
            
            current = self.open.pop(0)
            self.closed_map_hash[current.get_hash()] = 1
            if current.is_goal():
                path: list[Taquin] = [current]
                while current.parent:
                    path.append(current.parent)
                    current = current.parent
                return path[::-1]

            children: list[Taquin] = []
            for direction in Taquin.validDirections:
                child = current.move(direction)
                if child is not None:
                    self.update_cost(current, child)
                    children.append(child)

            for child in children:
                if child.get_hash() in self.closed_map_hash:
                    continue
                
                child.g = current.g + 1
                child.h = child.cost # self.get_cost(child)
                child.f = child.g + child.h
                child.parent = current
                if len([open_node for open_node in self.open if child == open_node and child.g > open_node.g]) > 0:
                    continue
                
                bisect.insort(self.open, child)

        self.path = None
        return None

    def get_cost(self, taquin: Taquin) -> int:
        state = taquin.get_state()
        h1 = sum([1 if self.goal[i][j] != state[i][j]
                 else 0 for i in range(taquin.size) for j in range(taquin.size)])
        return h1
    
    def update_cost(self, prev: Taquin, next: Taquin) -> None:
        # Tile 0 will always be moved.
        board_size = next.size
        prev_T0_x, prev_T0_y = prev.get_tile(0)
        next_T0_x, next_T0_y = next.get_tile(0) # This is the index of the tile we swapping with
        tile_value = prev._state[next_T0_x][next_T0_y]
        correct_x, correct_y = tile_value//board_size, tile_value % board_size
        
        diff = 0
        dbg = [0,0,0,0]
        if prev_T0_x == prev_T0_y == 0:
            # Was correct, now it's wrong
            diff += 1
            dbg[0] = 1
        
        if next_T0_x == next_T0_y == 0:
            # Was wrong, now it's correct
            dbg[1] = -1
            diff -= 1
        
        if correct_x == prev_T0_x and correct_y == prev_T0_y:
            # Now it's correct, 100% it was wrong
            dbg[2] = -1
            diff -= 1
        else:
            # Now, it's wrong
            if correct_x == next_T0_x and correct_y == next_T0_y:
                # It was correct! We made it worst
                diff += 1
            # If it was wrong, nothing changes
        
        next.cost = prev.cost + diff
