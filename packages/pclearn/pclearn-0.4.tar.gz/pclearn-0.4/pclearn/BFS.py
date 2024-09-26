from queue import Queue

adj_list = {
    'A': ['C', 'D', 'B'],
    'C': ['A', 'K'],
    'D': ['A', 'K', 'L'],
    'K': ['C', 'D', 'L'],
    'L': ['K', 'D', 'J'],
    'J': ['M'],
    'B': ['A'],
    'M': ['J']
}

visited = {}
level = {}
parent = {}
bfs_traversal = []
queue = Queue()

for node in adj_list.keys():
    visited[node] = False
    parent[node] = None
    level[node] = -1

source = input("Enter the Source node: ")
visited[source] = True
level[source] = 0
queue.put(source)

while not queue.empty():
    u = queue.get()
    bfs_traversal.append(u)
    for v in adj_list[u]:
        if not visited[v]:
            visited[v] = True
            parent[v] = u
            level[v] = level[u] + 1
            queue.put(v)

print("BFS traversal:", bfs_traversal)

target = input("Enter the exact node to reach: ")
path = []

if visited[target]:
    node = target
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()

print("Minimum path from Source to Destination:", ' -> '.join(path))
