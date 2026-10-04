"""Experiment runner and CSV file handling."""
import csv
from pathlib import Path
from agents import Pathfinder, Orbit

class Experiment:
    def __init__(self,campus,output="results.csv"):
        self.campus=campus
        self.pathfinder=Pathfinder("PATHFINDER",__import__("search").SearchEngine(campus))
        self.orbit=Orbit("ORBIT",__import__("search").SearchEngine(campus))
        self.output=Path(output)

    def run(self,pairs):
        rows=[]
        for start,goal in pairs:
            for agent in (self.pathfinder,self.orbit):
                r=agent.route(start,goal)
                rows.append({
                    "route": f"{start} -> {goal}",
                    "agent": agent.name,
                    "source": start,
                    "destination": goal,
                    "path": " -> ".join(r.path),
                    "path_cost_m": round(r.cost,2),
                    "nodes_explored": r.nodes_explored,
                    "execution_time_s": f"{r.execution_time:.8f}"
                })
        self.output.parent.mkdir(parents=True,exist_ok=True)
        with self.output.open("w",newline="",encoding="utf-8") as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]))
            writer.writeheader(); writer.writerows(rows)
        return rows
