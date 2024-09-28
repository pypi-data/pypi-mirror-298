def mapper(data):
    char_counts = {}
    for char in data:
        if char.isalpha():
            char = char.lower()
            char_counts[char] = char_counts.get(char, 0) + 1
    return char_counts

def reducer(data):
    char_counts = {}
    for count_dict in data:
        for char, count in count_dict.items():
            char_counts[char] = char_counts.get(char, 0) + count
    return char_counts

data=input("Enter the data:")
mapped_data = [mapper(data)]
reduced_data = reducer(mapped_data)
print(reduced_data)
