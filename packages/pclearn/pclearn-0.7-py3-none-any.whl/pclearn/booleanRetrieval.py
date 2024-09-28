def boolean(strs=[],files=[], query=''):
    if len(files)!=0 and len(strs)==0:
        strs = []
        for f in files:
            with open(f'{f}.txt', "r") as file:
                strs.append(file.read().strip())

    unique = set(' '.join(strs).split())
    bool_val = [{word: word in s.split() for word in unique} for s in strs]

    query = query.split()
    var_bool = []
    ope = []
    not_switch = False

    for term in query:
        if term in ('and', 'or'):
            ope.append(term)
        elif term == 'not':
            not_switch = True
        else:
            temp = [not doc[term] if not_switch else doc[term] for doc in bool_val]
            var_bool.append(temp)
            not_switch = False

    while len(var_bool) > 1:
        a, b = var_bool.pop(0), var_bool.pop(0)
        op = ope.pop(0)
        var_bool.insert(0, [i and j if op == 'and' else i or j for i, j in zip(a, b)])

    return 'document number:'+str([index + 1 for index, value in enumerate(var_bool[0]) if value])

#For User Input
s1 = "java is elegant"
s2 = "C++ is powerful"
s3 = "Rust is safe"
s4 = "Go is efficient"
s5 = "Kotlin is modern"
strs = [s1, s2, s3, s4, s5]
query = "is and not Kotlin and not C++"
print('Input ',boolean(strs=strs, query=query))



#Input from Files
files = ['d1','d2','d3','d4','d5']
query = 'not java and not Python and is'
print('File ',boolean(files=files, query=query))
