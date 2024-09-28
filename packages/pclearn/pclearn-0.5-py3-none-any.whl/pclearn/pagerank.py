def page_rank(dic,k):
    inbound = {}
    for i in dic:
        inbound[i]=[]
        for j in dic:
            if i in dic[j]:
                inbound[i].append(j)
    rank = {i:1/len(dic) for i in dic.keys()}
    new_r = {i:None for i in dic.keys()}
    for i in range(k):
        for j in inbound:
            temp = 0
            for k in inbound[j]:
                temp += (rank[k])/(len(dic[k]))
            new_r[j]=round(temp,4)
        rank=new_r.copy()
    return dict(sorted(rank.items(), key=lambda item: item[1]))
dic = {
"A":["C","B"],
"B":["D"],
"C":["A","B","D"],
"D":["C"]}
print(page_rank(dic,k=2))