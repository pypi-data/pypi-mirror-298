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
dfs_traversal = []
stack = []
for node in adj_list.keys():
    visited[node] = False
    parent[node] = None
    level[node] = -1
source = input("Enter the exact Source node to start: ")
if source not in adj_list:
    print("Source node not found in the graph.")
else:
    visited[source] = True
    level[source] = 0
    stack.append(source)
    while stack:
        u = stack.pop()
        dfs_traversal.append(u)
        for v in adj_list[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                level[v] = level[u] + 1
                stack.append(v)
    print("DFS traversal:", dfs_traversal)    
    def path(target):
        if target not in adj_list:
            print("Destination node not found in the graph.")
        else:
            path = []
            if visited[target]:
                node = target
                while node is not None:
                    path.append(node)
                    node = parent[node]
                path.reverse()
            print("Minimum path from Source to Destination:", ' -> '.join(path) if path else "No path found.")    
target = input("Enter the exact Destination node to reach: ")
path(target)
