from taquin import Taquin
from .base import BaseAlgorithm
import time


class IterativeDfs(BaseAlgorithm):
    __NAME__ = "Iterative Depth First Search"
    MAXLIM = 35

    def __init__(self, taquin: Taquin, quiz_cost: bool = False):
        taquin.cost = self.get_cost(taquin)
        self.taquin = taquin
        self.quiz_cost = quiz_cost
        
        self.goal = taquin.get_solution()
        self.closed = []
        self.path = []

    def solve(self, timeout=60):
        start = time.time()
        for lim in range(1, self.MAXLIM):
            end = time.time()
            if end - start > timeout:
                self.path = None
                return None
            
            self.closed = [self.taquin]
            if self._dfs(lim, self.taquin):
                self.path+= [self.taquin]
                self.path = self.path[::-1]
                return self.path
        return None

    def _dfs(self, lim, parent):
        if parent.is_goal():
            while parent.parent:
                self.path.append(parent)
                parent = parent.parent
            return True
        
        if lim <= 0:
            return False
        
        if parent.get_state() in self.closed:
            return False
        
        self.closed.append(parent.get_state())
        
        possibleMoves = []
        for direction in Taquin.validDirections:
            movedTile = parent.move(direction)
            if movedTile is None:
                continue
            
            self.update_cost(parent, movedTile)
            cost = movedTile.cost if self.quiz_cost else self.get_cost(movedTile)
            movedTile.parent = parent
            possibleMoves.append((cost, movedTile))

        possibleMoves = sorted(possibleMoves, key=lambda x: x[0], reverse=False )
        for _, st in possibleMoves:
            if self._dfs(lim-1, st):
                return True 

    def get_cost(self, taquin: Taquin):
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
