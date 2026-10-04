# Brief Report — AI Campus Route Navigator

## 1. Objective

The objective is to convert the supplied CU Technology Campus map into a weighted graph and compare two AI routing strategies:

- **PATHFINDER:** Greedy Best-First Search
- **ORBIT:** A* Search

The comparison focuses on route quality, computational effort, and the effect of the CSE-zone routing restriction.

## 2. Campus graph

The graph was constructed from the locations shown on the assignment map. No additional campus locations were introduced. Approximate walking distances were assigned to walkable connections and stored in `campus.json`.

The graph is deliberately kept outside the search code so that the map can be changed without rewriting the algorithms.

## 3. Heuristic

Both agents use the same map-based heuristic. Each location has approximate coordinates derived from the supplied map, and the heuristic estimates remaining distance using straight-line distance:

`h(n) = 8 × EuclideanDistance(n, goal)`

The same `h(n)` is supplied to both algorithms.

PATHFINDER uses:

`f(n) = h(n)`

ORBIT uses:

`f(n) = g(n) + h(n)`

where `g(n)` is the actual accumulated walking cost.

## 4. CSE-zone constraint

The three CSE locations are:

- CSE Laboratory
- CSE_AKC Seminar Hall
- CSE_Reflxon Room

Entry into the CSE zone must occur through a Tower 2 entry and Lift Area. While inside the CSE zone, the route may visit only CSE-labelled locations until it returns to Lift Area. Exiting then follows the reverse restriction.

The rule is enforced while generating valid neighbours, so an invalid route such as:

`Lift Area → CSE Laboratory → Garden Area`

cannot be produced.

## 5. Experimental setup

Eight source-destination pairs were tested:

1. Reception of Calcutta University → Library
2. Canteen, CU Technology Campus → New Building 2
3. Entry Gate 1 → CSE Laboratory
4. Auditorium Hall → CSE_AKC Seminar Hall
5. Library → Canteen
6. Entry Gate 4 → New Building 2
7. Power Area → Library
8. Entry Gate 2 → CSE_Reflxon Room

Both agents solved every pair.

## 6. Results

| Route | PATHFINDER cost | ORBIT cost | PATHFINDER nodes | ORBIT nodes | Different route? |
|---|---:|---:|---:|---:|---|
| Reception → Library | 465 m | 425 m | 5 | 11 | Yes |
| Canteen → New Building 2 | 255 m | 255 m | 3 | 7 | No |
| Entry Gate 1 → CSE Laboratory | 575 m | 575 m | 8 | 15 | No |
| Auditorium → CSE_AKC | 325 m | 325 m | 5 | 12 | No |
| Library → Canteen | 480 m | 440 m | 5 | 15 | Yes |
| Entry Gate 4 → New Building 2 | 350 m | 350 m | 4 | 5 | No |
| Power Area → Library | 390 m | 350 m | 4 | 11 | Yes |
| Entry Gate 2 → CSE_Reflxon | 310 m | 310 m | 5 | 8 | No |

### Aggregate observations

- PATHFINDER average path cost: **393.75 m**
- ORBIT average path cost: **378.75 m**
- PATHFINDER average nodes explored: **4.88**
- ORBIT average nodes explored: **10.50**
- Different routes: **3 of 8**
- On all three different-route cases, ORBIT produced the lower-cost route.

## 7. Analysis

### Does Greedy Best-First always find the shortest route?

No. In the Reception → Library, Library → Canteen, and Power Area → Library experiments, PATHFINDER selected a route that looked attractive according to the remaining-distance heuristic but had a higher total cost.

For example, for Reception → Library:

- PATHFINDER: 465 m
- ORBIT: 425 m

PATHFINDER selected the direct-looking Garden Area → Library connection. ORBIT instead accounted for the cost already travelled and selected a route through Lift Area before reaching Library.

### How does A* use the distance already travelled?

A* evaluates `g(n) + h(n)`. Therefore, a node with a good-looking heuristic can still be rejected when reaching it has already incurred too much cost.

This is the key difference from Greedy Best-First Search, whose priority contains only `h(n)`.

### When do the agents choose different paths?

They differed when the heuristic-favoured branch had a larger accumulated cost than an alternative branch. Three of the eight tested pairs produced different routes.

### How does the heuristic affect behaviour?

The heuristic strongly influences the order in which both algorithms expand nodes. Because both agents use the same heuristic, differences in behaviour are primarily caused by whether accumulated cost `g(n)` is included.

### What happens under the CSE constraint?

The search cannot leave the CSE zone directly for ordinary campus locations. It must return through Lift Area and then use a Tower 2 entry for outward travel. This makes the constraint part of the state-transition logic rather than merely a post-processing check.

## 8. Computational behaviour

PATHFINDER explored fewer nodes on average because it aggressively follows the location with the smallest estimated remaining distance.

ORBIT explored more nodes on this small graph because it considers both accumulated cost and estimated remaining cost. The additional exploration allowed it to find lower-cost routes in the three cases where the strategies diverged.

Individual execution times are extremely small because the graph contains only a few dozen nodes. Consequently, timing values are sensitive to operating-system scheduling and Python runtime noise. The node counts and route costs are more useful for interpreting the algorithmic difference.

## 9. Conclusion

The experiment demonstrates that **looking closest to the destination is not sufficient to guarantee the best complete route**.

PATHFINDER is computationally lighter on the tested graph, but its greedy decision rule can produce a higher-cost route. ORBIT performs more search but incorporates the cost already travelled and consequently produced lower-cost routes in every case where the two agents selected different paths.

The experiment also demonstrates why the campus graph, heuristic, and CSE routing constraint must be integrated into the search process rather than treating pathfinding as a simple shortest-path lookup.
