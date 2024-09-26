adj_list = {
    'A': ['B', 'C', 'D'],
    'B': ['E'],
    'C': ['F', 'G'],
    'D': ['C'],
    'E': ['H', 'F'],
    'F': ['B'],
    'H': [],
    'G': [],
}

def dls(s,g,path,level,max_depth):
    print("Current Level is ",level)
    print("Testing for ",g+" "+"node from "+s)
    path.append(s)
    e="Max depth limit reached "
    while True:
        if level>max_depth:
            print("Current level reches maximum depth ")
            return False
        break
    if s==g:
        print("Goal node Found")
        return path
    print("Goal Node Test Fail ")
    #for i in adj_list[s]:
    print("Expiring current node",s)
    print("------------------------")
    for neighbor in adj_list[s]:
        if dls(neighbor
               ,g,path,level+1,max_depth):
            return path
        path.pop()
        return False
    return False

s=input("Enter Source node")
g=input("Enter the goal node ")
max_depth=int(input("Enter Maximum depth limit "))
print()
path=list()
output=dls(s,g,path,0,max_depth)
if(output):
    print("There exist path from source to goal ")
    print("Path is ",path)
else:
    print("No path from source to goal in given depth limit ")
