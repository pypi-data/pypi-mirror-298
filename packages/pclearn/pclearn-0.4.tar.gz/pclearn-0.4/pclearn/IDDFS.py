graph = {
    "M": ["N", "Q", "R"],
    "N": ["O", "Q", "M"],
    "R": ["M"],
    "O": ["P", "N"],
    "Q": ["M", "N", "P"],
    "P": ["O", "Q"]
}

def DFS(node, destination, depth, path):
    path.append(node)  # Add the current node to the path
    if node == destination:
        return True
    if depth > 0:
        for neighbor in graph.get(node, []):
            if DFS(neighbor, destination, depth - 1, path):
                return True
    path.pop()  # Remove the node from path if not part of the solution
    return False

def IDDFS(source, destination, maxDepth):
    for depth in range(maxDepth + 1):
        path = []  # Reset path for each depth iteration
        if DFS(source, destination, depth, path):
            return path  # Return the actual path if found
    return None

# Get user input
source = input('Enter source node: ').strip()
destination = input('Enter destination node: ').strip()
maxDepth = input('Enter maximum depth: ').strip()

# Validate input
if not source or not destination:
    print("Source and destination nodes must be provided.")
elif source not in graph or destination not in graph:
    print("Source and destination nodes must be valid nodes in the graph.")
elif not maxDepth.isdigit():
    print("Maximum depth must be a valid integer.")
else:
    maxDepth = int(maxDepth)
    path = IDDFS(source, destination, maxDepth)
    if path:
        print("Path exists:", " -> ".join(path))
    else:
        print("Path is not available.")
