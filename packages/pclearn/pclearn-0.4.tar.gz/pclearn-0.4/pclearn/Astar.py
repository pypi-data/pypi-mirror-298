graph = {
    "A": ({"B": 1, "C": 4}, 3),
    "B": ({"A": 1, "D": 2, "E": 5}, 2),
    "C": ({"A": 4, "F": 7}, 6),
    "D": ({"B": 2}, 4),
    "E": ({"B": 5, "F": 1}, 1),
    "F": ({"C": 7, "E": 1}, 0)
}

def get_min(q):
    return min(q, key=lambda x: sum(q[x]))
def a_star(graph, current, destination, path, current_cost, q):
    print(f"Exploring node {current}, connected nodes with h(n) values:")    
    for neighbor, cost in graph[current][0].items():    
        if neighbor not in path:
            q[neighbor] = (graph[neighbor][1], cost)
            total_cost = current_cost + sum(q[neighbor])
            print(f"{neighbor} -> h(n) = {q[neighbor][0]}, path cost = {q[neighbor][1]}, A* value = {total_cost}")
    while q:
        next_node = get_min(q)
        print(f"Selecting node with minimum A* value: {next_node}")
        print("__________________________________________________")       
        if next_node == destination:
            return path + [destination]
        
        next_cost = current_cost + q[next_node][1]
        del q[next_node]
        
        new_path = a_star(graph, next_node, destination, path + [next_node], next_cost, q)
        if new_path:
            return new_path      
    return []
source = input("Enter source vertex: ").strip()
destination = input("Enter destination vertex: ").strip()
heuristic = int(input("Enter given heuristic value for source: "))
path = a_star(graph, source, destination, [], 0, {source: (heuristic, 0)})
if path:
    print("Path found:", path)
else:
    print("Path not found")
