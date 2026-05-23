"""
Flask Web Application for TSP CVNet
Displays the optimal route in a beautiful web interface
"""

from flask import Flask, render_template, jsonify
import json
import pulp
from typing import List, Tuple

app = Flask(__name__)

def load_data(json_path: str = "input_data.json") -> dict:
    """Loads and validates data from the JSON file."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File '{json_path}' not found.")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error reading JSON: {e}")

    required_fields = ["islands", "distances"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Required field '{field}' missing from JSON.")

    islands = data["islands"]
    dists = data["distances"]
    n = len(islands)

    if len(dists) != n or any(len(row) != n for row in dists):
        raise ValueError("The distance matrix must be square and compatible with the list of islands.")

    # Determine the starting island (depot)
    start_name = data.get("start_island", islands[0])
    try:
        start_idx = islands.index(start_name)
    except ValueError:
        raise ValueError(f"Start island '{start_name}' not found in the list of islands.")

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
    x = pulp.LpVariable.dicts(
        "x", 
        ((i, j) for i in range(n) for j in range(n) if i != j), 
        cat='Binary'
    )

    # Auxiliary variables u[i] (visit order)
    u = pulp.LpVariable.dicts(
        "u", 
        (i for i in range(n)), 
        lowBound=0, 
        upBound=n-1, 
        cat='Continuous'
    )

    # Objective function: minimize total distance
    prob += pulp.lpSum(dists[i][j] * x[i, j] for i in range(n) for j in range(n) if i != j)

    # Degree constraints (each island has one departure and one arrival)
    for i in range(n):
        prob += pulp.lpSum(x[i, j] for j in range(n) if j != i) == 1
        prob += pulp.lpSum(x[j, i] for j in range(n) if j != i) == 1

    # MTZ constraints for subtour elimination
    for i in range(n):
        for j in range(n):
            if i != j and i != depot and j != depot:
                prob += u[i] - u[j] + n * x[i, j] <= n - 1

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
        nxt = None
        for j in range(n):
            if j != current and pulp.value(x[current, j]) == 1:
                nxt = j
                break
        if nxt is None or nxt == depot:
            break
        route.append(nxt)
        current = nxt
    route.append(depot)

    return route, total_dist

@app.route('/')
def index():
    """Main page with the TSP result"""
    try:
        data = load_data()
        route, distance = solve_tsp_mtz(data)
        
        # Convert indices to island names
        route_names = [data["islands"][i] for i in route]
        
        return render_template(
            'index.html',
            route=route_names,
            distance=round(distance, 2),
            num_islands=data["n"]
        )
    except Exception as e:
        return render_template('error.html', error=str(e)), 500

@app.route('/api/result')
def api_result():
    """API endpoint that returns the TSP result as JSON"""
    try:
        data = load_data()
        route, distance = solve_tsp_mtz(data)
        route_names = [data["islands"][i] for i in route]
        
        return jsonify({
            'status': 'success',
            'route': route_names,
            'total_distance': round(distance, 2),
            'num_islands': data["n"]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
