"""AI routing agents."""
class Agent:
    def __init__(self,name,search_engine):
        self.name=name
        self.search_engine=search_engine

    def route(self,start,goal):
        raise NotImplementedError

class Pathfinder(Agent):
    """PATHFINDER: Greedy Best-First Search, f(n)=h(n)."""
    def route(self,start,goal):
        return self.search_engine.greedy_best_first(start,goal)

class Orbit(Agent):
    """ORBIT: A* Search, f(n)=g(n)+h(n)."""
    def route(self,start,goal):
        return self.search_engine.astar(start,goal)
