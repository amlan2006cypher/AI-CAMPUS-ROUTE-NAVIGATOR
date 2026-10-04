"""From-scratch Greedy Best-First Search and A* Search."""
from dataclasses import dataclass
import heapq
import itertools
import time

@dataclass
class SearchResult:
    path: list
    cost: float
    nodes_explored: int
    execution_time: float

class SearchEngine:
    def __init__(self, campus):
        self.campus = campus
        self._counter = itertools.count()

    def _reconstruct(self, parent, goal):
        path=[goal]
        while path[-1] in parent:
            path.append(parent[path[-1]])
        path.reverse()
        return path

    def greedy_best_first(self, start, goal):
        self.campus.validate_location(start); self.campus.validate_location(goal)
        t0=time.perf_counter()
        frontier=[]
        heapq.heappush(frontier,(self.campus.heuristic(start,goal), next(self._counter), start))
        parent={}
        visited=set()
        g={start:0.0}
        explored=0
        while frontier:
            _,_,current=heapq.heappop(frontier)
            if current in visited: continue
            visited.add(current); explored += 1
            if current == goal:
                path=self._reconstruct(parent,goal)
                return SearchResult(path,g[goal],explored,time.perf_counter()-t0)
            for nxt,w in self.campus.neighbors(current,goal):
                if nxt not in visited:
                    if nxt not in g or g[nxt] > g[current]+w:
                        g[nxt]=g[current]+w
                        parent[nxt]=current
                        heapq.heappush(frontier,(self.campus.heuristic(nxt,goal),next(self._counter),nxt))
        return SearchResult([],float("inf"),explored,time.perf_counter()-t0)

    def astar(self, start, goal):
        self.campus.validate_location(start); self.campus.validate_location(goal)
        t0=time.perf_counter()
        frontier=[]
        g={start:0.0}
        parent={}
        heapq.heappush(frontier,(self.campus.heuristic(start,goal),next(self._counter),start))
        closed=set()
        explored=0
        while frontier:
            f,_,current=heapq.heappop(frontier)
            if current in closed: continue
            closed.add(current); explored += 1
            if current == goal:
                path=self._reconstruct(parent,goal)
                return SearchResult(path,g[goal],explored,time.perf_counter()-t0)
            for nxt,w in self.campus.neighbors(current,goal):
                tentative=g[current]+w
                if nxt in closed and tentative >= g.get(nxt,float("inf")):
                    continue
                if tentative < g.get(nxt,float("inf")):
                    g[nxt]=tentative
                    parent[nxt]=current
                    score=tentative+self.campus.heuristic(nxt,goal)
                    heapq.heappush(frontier,(score,next(self._counter),nxt))
        return SearchResult([],float("inf"),explored,time.perf_counter()-t0)
