"""
Solution of the Traveling Salesman Problem (TSP) for CVNet.
Miller-Tucker-Zemlin (MTZ) formulation with PuLP.
Data loaded from an external JSON file.
"""

import json
import sys
import pulp
from typing import List, Dict, Tuple

def load_data(json_path: str) -> dict:
    """Loads and validates data from the JSON file."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        sys.exit(f"Error: File '{json_path}' not found.")
    except json.JSONDecodeError as e:
        sys.exit(f"Error reading JSON: {e}")

    required_fields = ["islands", "distances"]
    for field in required_fields:
        if field not in data:
            sys.exit(f"Required field '{field}' missing from JSON.")

    islands = data["islands"]
    dists = data["distances"]
    n = len(islands)

    if len(dists) != n or any(len(row) != n for row in dists):
        sys.exit("The distance matrix must be square and compatible with the list of islands.")

    # Determine the starting island (depot)
    start_name = data.get("start_island", islands[0])
    try:
        start_idx = islands.index(start_name)
    except ValueError:
        sys.exit(f"Start island '{start_name}' not found in the list of islands.")

    return {
        "islands": islands,
        "distances": dists,
        "n": n,
        "start_idx": start_idx
    }

def solve_tsp_mtz(data: dict) -> Tuple[List[int], float]:
    """
    Solves the TSP using the MTZ formulation.
    Returns the sequence of indices (closed cycle) and the total distance.
    """
    islands = data["islands"]
    n = data["n"]
    dists = data["distances"]
    depot = data["start_idx"]

    # Initialize problem
    prob = pulp.LpProblem("TSP_CVNet", pulp.LpMinimize)

    # Binary variables x[i,j]
    x = pulp.LpVariable.dicts("x", ((i, j) for i in range(n) for j in range(n) if i != j),
                              cat='Binary')

    # Auxiliary variables u[i] (visit order)
    u = pulp.LpVariable.dicts("u", (i for i in range(n)),
                              lowBound=0, upBound=n-1, cat='Continuous')

    # Objective function: minimize total distance
    prob += pulp.lpSum(dists[i][j] * x[i, j] for i in range(n) for j in range(n) if i != j)

    # Degree constraints (each island has one departure and one arrival)
    for i in range(n):
        prob += pulp.lpSum(x[i, j] for j in range(n) if j != i) == 1  # leaves i
        prob += pulp.lpSum(x[j, i] for j in range(n) if j != i) == 1  # enters i

    # MTZ constraints for subtour elimination
    for i in range(n):
        for j in range(1, n):  # avoid redundant constraint for j=0 (depot)
            if i != j and i != depot and j != depot:
                prob += u[i] - u[j] + n * x[i, j] <= n - 1
    # (The depot node can interact freely; the constraint above already covers pairs without depot)

    # Fix u value at depot to remove symmetries
    prob += u[depot] == 0

    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    if pulp.LpStatus[prob.status] != "Optimal":
        raise RuntimeError(f"No optimal solution found. Status: {pulp.LpStatus[prob.status]}")

    # Extract solution
    route = []
    total_dist = pulp.value(prob.objective)

    # Reconstruct the route starting from the depot
    current = depot
    route.append(current)
    while True:
        # find next node j such that x[current,j] == 1
        nxt = None
        for j in range(n):
            if j != current and pulp.value(x[current, j]) == 1:
                nxt = j
                break
        if nxt is None or nxt == depot:
            break
        route.append(nxt)
        current = nxt
    route.append(depot)  # close the cycle

    return route, total_dist

def print_result(route: List[int], islands: List[str], distance: float):
    """Displays the optimal route in a readable format."""
    print("\n--- Optimal Route for CVNet (TSP) ---")
    path = " -> ".join(islands[i] for i in route)
    print(path)
    print(f"Total distance: {distance:.2f} units\n")

def main():
    if len(sys.argv) < 2:
        json_path = "input_data.json"
    else:
        json_path = sys.argv[1]

    data = load_data(json_path)
    route, dist = solve_tsp_mtz(data)
    print_result(route, data["islands"], dist)

if __name__ == "__main__":
    main()