import random as rand
import load_input

vertices, Edges = load_input.max_cut("input_format")


def checkEdge(S, T):
    Sum = 0
    for (ai, aj), w in Edges:
        if (ai in S and aj in T) or (ai in T and aj in S):
            Sum += w
    return Sum


def checkNeighbors(S, T, solution):
    Sn = S.copy()
    Tn = T.copy()
    Schosen = Sn.copy()
    Tchosen = Tn.copy()
    for a in S:
        Sn.remove(a)
        Tn.append(a)
        new_solution = checkEdge(Sn, Tn)
        # print(f"Neighbor partition: {Sn} | {Tn}")
        # print(f"Current cut value: {new_solution}")
        if solution <= new_solution:
            Schosen = Sn.copy()
            Tchosen = Tn.copy()
            solution = new_solution
        Sn = S.copy()
        Tn = T.copy()
    for a in T:
        Tn.remove(a)
        Sn.append(a)
        new_solution = checkEdge(Sn, Tn)
        # print(f"Neighbor partition: {Sn} | {Tn}")
        # print(f"Current cut value: {new_solution}")
        if solution <= new_solution:
            Schosen = Sn.copy()
            Tchosen = Tn.copy()
            solution = new_solution
        Sn = S.copy()
        Tn = T.copy()
    return Schosen, Tchosen, solution


def random_iteration(num_vertices):
    rand.shuffle(vertices)
    S = []
    T = []
    # Split at the second place
    for i in range(num_vertices):
        if i < 3:
            S.append(vertices[i])
        else:
            T.append(vertices[i])
    # Check for Cuts on edges
    Schosen = S.copy()
    Tchosen = T.copy()
    # print(f"Current partition: {S} | {T}")
    # print(f"Current cut value: {checkEdge(S, T)}")
    solution = checkEdge(S, T)
    # Check for neighbors:
    improved = True
    highestSolution = solution
    while improved:
        # print("========== Climbing ?")
        improved = False
        Schosen, Tchosen, highestSolution = checkNeighbors(
            S, T, solution)
        if highestSolution > solution:
            improved = True
            # print(f"-- Yes, Climbing")
            S = Schosen.copy()
            T = Tchosen.copy()
            solution = highestSolution
        else:
            # print(f"-- No, :(")
            break
    return highestSolution


HighestSolution = 0

for i in range(150):
    solution = random_iteration(len(vertices))
    if HighestSolution < solution:
        HighestSolution = solution
print(f"{HighestSolution}")
