from taquin import Taquin
from .base import BaseAlgorithm
import time


class IterativeDfs(BaseAlgorithm):
    __NAME__ = "Iterative Depth First Search"
    MAXLIM = 35

    def __init__(self, taquin: Taquin):
        self.taquin = taquin
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
            
            cost = self.get_cost(movedTile)
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