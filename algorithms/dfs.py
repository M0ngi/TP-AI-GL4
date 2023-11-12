from taquin import Taquin
from .base import BaseAlgorithm
import time


class Dfs(BaseAlgorithm):
    __NAME__ = "Depth First Search"

    def __init__(self, taquin: Taquin):
        self.taquin = taquin
        self.goal = taquin.get_solution()
        self.closed: list[Taquin] = []
        self.path: list[Taquin] = []

    def solve(self, timeout = 60):
        start = time.time()
        self.closed = [self.taquin]
        if self._dfs(start+timeout, self.taquin):
            self.path+= [self.taquin]
            self.path = self.path[::-1]
            return self.path
        return None

    def _dfs(self, time_limit, parent):
        if parent.is_goal():
            while parent.parent:
                self.path.append(parent)
                parent = parent.parent
            return True
        
        end = time.time()
        if end > time_limit:
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
            if self._dfs(time_limit, st):
                return True 

    def get_cost(self, taquin: Taquin):
        state = taquin.get_state()
        h1 = sum([1 if self.goal[i][j] != state[i][j]
                 else 0 for i in range(taquin.size) for j in range(taquin.size)])
        return h1