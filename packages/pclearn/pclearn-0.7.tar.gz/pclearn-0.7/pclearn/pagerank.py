def page_rank(dic, k):
    inbound = {}
    for i in dic:
        inbound[i] = []
        for j in dic:
            if i in dic[j]:
                inbound[i].append(j)
    rank = {i: 1 / len(dic) for i in dic.keys()}
    new_r = {i: None for i in dic.keys()}
    for iteration in range(k):
        print(f"\nIteration {iteration + 1}:")
        for j in inbound:
            temp = 0
            for link in inbound[j]:
                temp += rank[link] / len(dic[link])
            new_r[j] = round(temp, 4)
        for page, value in new_r.items():
            print(f"Page {page}: {value}")
        rank = new_r.copy()
    return dict(sorted(rank.items(), key=lambda item: item[1]))
dic = {
    "A": ["C", "B"],
    "B": ["D"],
    "C": ["A", "B", "D"],
    "D": ["C"]
}
print("\nFinal PageRank Results:", page_rank(dic, k=5))
