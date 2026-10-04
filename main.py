"""AI Campus Route Navigator - Assignment X_03."""
from campus_map import CampusMap
from search import SearchEngine
from agents import Pathfinder, Orbit
from experiment import Experiment

EXPERIMENT_PAIRS = [
    ("Reception of Calcutta University","Library"),
    ("Canteen, CU Technology Campus","New Building 2 (Workshop Building)"),
    ("Entry Gate 1 (G1)","CSE Laboratory"),
    ("Auditorium Hall","CSE_AKC Seminar Hall"),
    ("Library","Canteen, CU Technology Campus"),
    ("Entry Gate 4 (G4)","New Building 2 (Workshop Building)"),
]

def print_result(agent,result):
    print(f"\n{agent.name}")
    print("Route:", " -> ".join(result.path) if result.path else "NO ROUTE")
    print(f"Cost: {result.cost:.2f} m")
    print(f"Nodes explored: {result.nodes_explored}")
    print(f"Time: {result.execution_time:.8f} s")

def main():
    campus=CampusMap("campus.json")
    engine=SearchEngine(campus)
    pathfinder=Pathfinder("PATHFINDER",engine)
    orbit=Orbit("ORBIT",engine)

    print("AI CAMPUS ROUTE NAVIGATOR")
    print("="*80)
    print("Available locations:")
    for n in campus.nodes: print(" -",n)

    start=input("\nEnter starting location: ").strip()
    goal=input("Enter destination: ").strip()
    try:
        print_result(pathfinder,pathfinder.route(start,goal))
        print_result(orbit,orbit.route(start,goal))
    except ValueError as e:
        print("Error:",e)
        return

    print("\nRunning predefined experiments...")
    exp=Experiment(campus,"results/results.csv")
    rows=exp.run(EXPERIMENT_PAIRS)
    print(f"Saved {len(rows)} agent-route records to results/results.csv")

if __name__=="__main__":
    main()
