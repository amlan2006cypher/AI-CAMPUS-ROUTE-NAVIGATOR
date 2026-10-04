"""Campus graph and routing-rule utilities."""
import json
from pathlib import Path
from math import hypot

CSE_NODES = {"CSE Laboratory", "CSE_AKC Seminar Hall", "CSE_Reflxon Room"}
ENTRY_NODES = {"Tower 2 Front Entry", "Tower 2 Rear Entry"}
LIFT = "Lift Area"

class CampusMap:
    def __init__(self, path="campus.json"):
        path = Path(path)
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        self.nodes = {item["name"]: (item["x"], item["y"]) for item in data["nodes"]}
        self.graph = {name: [] for name in self.nodes}
        for edge in data["edges"]:
            a,b,w = edge["from"], edge["to"], edge["weight_m"]
            self.graph[a].append((b,w))
            self.graph[b].append((a,w))

    def validate_location(self, name):
        if name not in self.nodes:
            raise ValueError(f"Unknown location: {name}")

    def heuristic(self, current, goal):
        """Map-based straight-line estimate. Same h is used by both agents."""
        x1,y1 = self.nodes[current]
        x2,y2 = self.nodes[goal]
        return 8.0 * hypot(x1-x2, y1-y2)

    def neighbors(self, current, goal):
        """Apply the assignment's CSE-zone entry/exit constraint."""
        if current in CSE_NODES:
            # Once inside the CSE zone, only CSE locations or Lift Area are legal.
            return [(n,w) for n,w in self.graph[current]
                    if n in CSE_NODES or n == LIFT]
        if current == LIFT:
            if goal in CSE_NODES:
                return [(n,w) for n,w in self.graph[current]
                        if n in CSE_NODES]
            return [(n,w) for n,w in self.graph[current]
                    if n not in CSE_NODES]
        return [(n,w) for n,w in self.graph[current]]
