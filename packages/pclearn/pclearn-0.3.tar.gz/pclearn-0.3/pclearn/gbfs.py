graph = {
    "A": ({"B": 1, "C": 4}, 3),
    "B": ({"A": 1, "D": 2, "E": 5}, 2),
    "C": ({"A": 4, "F": 7}, 6),
    "D": ({"B": 2}, 4),
    "E": ({"B": 5, "F": 1}, 1),
    "F": ({"C": 7, "E": 1}, 0)
}

def greedy_search(graph, current, destination, path):
    if current == destination:
        return path
    print(f"Exploring node {current}, path so far: {path}")
    q = {}
    for neighbor, cost in graph[current][0].items():
        if neighbor not in path:
            q[neighbor] = graph[neighbor][1]
            print(f"Neighbor {neighbor} with h(n) = {q[neighbor]}")
    if not q:
        return None
    next_node = min(q, key=q.get)
    print(f"Selecting {next_node} as the next node to explore with h(n) = {q[next_node]}")
    return greedy_search(graph, next_node, destination, path + [next_node])
source = input("Enter source vertex: ").strip()
destination = input("Enter destination vertex: ").strip()
path = greedy_search(graph, source, destination, [source])
if path:
    print("Path found:", path)
else:
    print("Path not found!")
