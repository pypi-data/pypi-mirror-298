matrix = [
    [0, 1, 1, 1],
    [1, 0, 1, 1],
    [1, 0, 0, 1],
    [0, 0, 0, 1]
]

k =3
hub_score = [1] * len(matrix)
auth_score = [0] * len(matrix)

for iteration in range(k):
    # Calculate authority scores
    for i in range(len(matrix)):
        auth_score[i] = 0
        for j in range(len(matrix)):
            if matrix[j][i] == 1:  # Note the index [j][i] for authority score
                auth_score[i] += hub_score[j]
                
    sum_auth = sum(auth_score)
    if sum_auth != 0:
        for i in range(len(matrix)):
            auth_score[i] /= sum_auth

    # Calculate hub scores
    for i in range(len(matrix)):
        hub_score[i] = 0
        for j in range(len(matrix)):
            if matrix[i][j] == 1:  # Note the index [i][j] for hub score
                hub_score[i] += auth_score[j]
                
    sum_hub = sum(hub_score)
    if sum_hub != 0:
        for i in range(len(matrix)):
            hub_score[i] /= sum_hub

    print(f"Iteration {iteration + 1}:")
    print(f"  Hub Scores: {hub_score}")
    print(f"  Authority Scores: {auth_score}")
    print()

print("The max hub score is: ", max(hub_score))
print("The max auth score is: ", max(auth_score))
