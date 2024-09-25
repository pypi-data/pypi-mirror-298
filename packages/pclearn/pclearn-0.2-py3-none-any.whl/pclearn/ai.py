#best First Search
graph = {
    "Oradea": ({"Zerind": 71, "Sibiu": 151}, 380),
    "Zerind": ({"Oradea": 71, "Arad": 75}, 374),
    "Arad": ({"Zerind": 75, "Sibiu": 140 , "Timisoara": 118}, 399),
    "Timisoara": ({"Arad": 118, "Lugoj": 111}, 329),
    "Lugoj": ({"Timisoara": 111, "Mehadia": 70}, 244),
    "Mehadia": ({"Lugoj": 70, "Drobeta": 75}, 241),
    "Sibiu": ({"Oradea": 151, "Fagaras": 99, "Rimnicu Vilcea": 80, "Arad": 140}, 253),
    "Fagaras": ({"Sibiu": 99, "Bucharest": 211}, 176),
    "Rimnicu Vilcea": ({"Sibiu": 80, "Pitesti": 97, "Craiova": 146}, 193),
    "Bucharest": ({"Fagaras": 211, "Pitesti": 101, "Urziceni": 85, "Giurgiu": 90}, 0),
    "Pitesti": ({"Rimnicu Vilcea": 97, "Craiova": 138, "Bucharest": 101}, 100),
    "Craiova": ({"Rimnicu Vilcea": 146, "Pitesti": 138, "Drobeta": 120}, 160),
    "Drobeta": ({"Mehadia": 75, "Craiova": 120}, 242),
    "Urziceni": ({"Bucharest": 85, "Vaslui": 142, "Hirsova": 98}, 80),
    "Giurgiu": ({"Bucharest": 90}, 77),
    "Vaslui": ({"Iasi": 92, "Urziceni": 142}, 199),
    "Hirsova": ({"Urziceni": 98, "Eforie": 86}, 151),
    "Iasi": ({"Vaslui": 92, "Neamt": 87}, 226),
    "Eforie": ({"Hirsova": 86}, 161),
    "Neamt": ({"Iasi": 87}, 234)
    }
def greedy_search_rec(graph,prev,dist,path,q):
    print("Connected nodes of current node",prev,"with h(n) values:")
    for n in graph[prev][0]:
        if n not in path:
            q[n]=graph[n][1]
            print(n,"->",q[n])
    while q:
        mn=min(q,key=q.get)
        print("Taking minimum h(n) vertext: ",mn)
        print(mn)
        if dist==mn:
            return path+[dist]
        new_path=greedy_search_rec(graph,prev,dist,path+[mn],q)
        if new_path:
            return new_path
    return []
source=input("Enter Source vertex: ")
dist=input("Enter a Destination Vertex: ")
path=greedy_search_rec(graph,source,dist,[source],{})
if path:
    print(path)
else:
    print("Path Not Found")
