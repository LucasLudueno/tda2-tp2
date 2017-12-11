import csv
import random
import sys
import os


def is_valid(n, edges, colors):
    for v in range(n):
        for w in edges[v]:
            if colors[v] == colors[w]:
                return False
    return True


def gen(n, e):
    edges = [[False] * n for _ in range(n)]

    for _ in range(e):
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        while edges[i][j] or i == j:
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)
        edges[i][j] = True
        edges[j][i] = True
    return edges


def degrees(n, edges):
    return list(map(len, edges))


def greedy(n, edges, sorting):
    colors = [None] * n
    all_colors = set(list(range(n)))
    color_count = [0] * n
    p = sorting
    for v in p:
        s = {colors[j] for j in edges[v] if colors[j] is not None}

        available_colors = all_colors - s
        # colors[v] = max(available_colors, key=lambda c: color_count[v])
        colors[v] = min(available_colors)
        # for color in all_colors:
        #     if color not in s:
        #         colors[v] = color
        #         break

        color_count[colors[v]] += 1
    return colors


def greedy_random(n, edges):
    p = list(range(n))
    random.shuffle(p)
    return greedy(n, edges, p)


def greedy_ldf(n, edges):
    degs = degrees(n, edges)
    p = list(range(n))
    p.sort(key=lambda v: degs[v], reverse=True)
    return greedy(n, edges, p)


def greedy_sdf(n, edges):
    degs = degrees(n, edges)
    p = list(range(n))
    p.sort(key=lambda v: degs[v])
    return greedy(n, edges, p)


def greedy_sdo(n, edges):
    colors = [None] * n
    all_colors = range(n)

    neighbours_colours = [set() for _ in range(n)]
    saturation = [0 for _ in range(n)]
    u = set(range(n))
    degs = degrees(n, edges)
    while len(u) > 0:
        s = list(u)
        # Sort uncoloured vertices by saturation degree
        s.sort(key=lambda v: (saturation[v], degs[v]), reverse=True)
        v = s[0]  # Vertex with highest saturation degree
        my_color = None
        for color in all_colors:
            if color not in neighbours_colours[v]:
                colors[v] = color
                my_color = color
                break

        for w in edges[v]:
            neighbours_colours[w].add(my_color)
            saturation[w] = len(neighbours_colours[w])
        u.remove(v)
    return colors


def greedy_ido(n, edges):
    colors = [None] * n
    all_colors = range(n)

    coloured_neighbours = [0 for _ in range(n)]
    u = set(range(n))
    degs = degrees(n, edges)
    while len(u) > 0:
        s = list(u)
        # Sort uncoloured vertices by number of coloured neighbours
        s.sort(key=lambda v: (coloured_neighbours[v], degs[v]), reverse=True)
        v = s[0]  # Vertex with highest number of coloured neighbours
        u.remove(v)

        # Colours already used by neighbours
        s = {colors[j] for j in edges[v] if colors[j] is not None}

        for color in all_colors:
            if color not in s:
                colors[v] = color
                break

        for w in edges[v]:
            coloured_neighbours[w] += 1
    return colors


def rlf(n, edges):
    colors = [None] * n
    x = set(list(range(n)))
    y = set()
    current_color = -1
    while len(x) > 0:
        current_color += 1
        first = True
        v = -1
        while len(x) > 0:
            # Choose v

            # Neighbours of vertices in graph induced by x
            neighbours_x = {w: set(edges[w]) & x for w in x}
            if first:
                # The first vertex to be added is the vertex with highest degree in the graph induced by x
                as_list = list(x)
                # Ordered by decreasing degree in graph induced by x
                as_list.sort(key=lambda w: len(neighbours_x[w]), reverse=True)
                # Vertex with highest degree in graph induced by x
                v = as_list[0]

                first = False
            else:
                as_list = list(x)
                neighbours = {w: (set(edges[w]) & y) for w in x}
                as_list.sort(key=lambda w: (
                    len(neighbours[w]), -len(neighbours_x[w])), reverse=True)
                v = as_list[0]
            colors[v] = current_color
            # Neighbours can't be coloured with this same colour

            # Y = U2 = Uncoloured nodes adjacent to at least one coloured node
            y = y.union(neighbours_x[v])

            # X = U1 = Uncoloured nodes not adjacent to any coloured node
            x = x - y - {v}

        x = y
        y = set()
    return colors


def load_graph(filename):

    file = open(filename, 'r')
    lines = file.readlines()
    edges = []
    n = 0
    e = 0
    for line in lines:
        line = line.split()
        if len(line) == 0:
            continue
        if (line[0] == 'p'):
            n = int(line[2])
            edges = [[] for _ in range(n)]
        if (line[0] == 'e'):
            v = int(line[1]) - 1
            w = int(line[2]) - 1
            edges[v].append(w)
            edges[w].append(v)
            e += 1
    return n, e, edges


def decreasing(u, colors):
    colors_size = [0 for _ in range(len(set(colors)))]

    for color in colors:
        colors_size[color] += 1

    u.sort(key=lambda v: (colors_size[colors[v]], colors[v]), reverse=True)


def increasing(u, colors):
    colors_size = [0 for _ in range(len(set(colors)))]

    for color in colors:
        colors_size[color] += 1

    u.sort(key=lambda v: (colors_size[colors[v]], colors[v]))


def random_c(u, colors):
    list_colors = list(set(colors))
    random.shuffle(list_colors)  # Shuffle colors
    u.sort(key=lambda v: list_colors[colors[v]])


def reversed_c(u, colors):
    u.sort(key=lambda v: colors[v], reverse=True)


def iterated(n, edges, initial):
    colors = initial
    best = len(set(colors))
    best_i = 0
    for i in range(10000):
        u = list(range(n))

        r = random.randint(0, 16)

        if r < 7:
            decreasing(u, colors)
        elif r < 12:
            reversed_c(u, colors)
        elif r < 15:
            random_c(u, colors)
        else:
            increasing(u, colors)

        colors_prev = colors[:]
        colors = greedy(n, edges, u)
        l = len(set(colors))
        if (l < best):
            best = l
            best_i = i + 1
            # print("Iteration ", i, " new best ", best)
            # print("Coloured with \t\t", len(set(colors)))
            # print("Colouring is valid \t", is_valid(n, edges, colors))
    return colors, best_i


def test(name, fun, n, edges):
    print()
    print("***** " + name + " *****")
    colors = fun(n, edges)
    print("Coloured with \t\t", len(set(colors)))
    print("Colouring is valid \t", is_valid(n, edges, colors))
    return colors


def random_graph(n, p):
    e = 0
    edges = [set() for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                if random.random() < p:
                    e += 1
                    edges[i].add(j)
                    edges[j].add(i)
    print("Edges:", e)
    return edges


# n, e, edges = load_graph(sys.argv[1])


# print("Loaded graph with")
# print("Nodes: ", n)
# print("Edges: ", e)
# degs = degrees(n, edges)
# print("Minimum degree: ", min(degs))
# print("Maximum degree: ", max(degs))


# n = 2000
# p = 0.5

# edges = random_graph(n, p)

# test("Random", greedy_random, n, edges)
# test("Largest degree first", greedy_ldf, n, edges)
# # test("Smallest degree first", greedy_sdf, n, edges)
# colors = test("Saturation degree ordering", greedy_sdo, n, edges)
# print(set(colors))
# # test("Incidence degree ordering", greedy_ido, n, edges)
# colors = test("Recursive largest first", rlf, n, edges)
# print(set(colors))

# iterated(n, edges, colors)


def ig_sdo(n, edges):
    colors = greedy_sdo(n, edges)
    colors = iterated(n, edges, colors)
    return colors


def ig_rlf(n, edges):
    colors = rlf(n, edges)
    colors = iterated(n, edges, colors)
    return colors


def test_all(filename, writer):
    n, e, edges = load_graph(filename)

    algorithms = [greedy_random, greedy_ldf, greedy_ido, greedy_sdo, rlf]

    results = []
    for alg in algorithms:
        colors = alg(n, edges)
        results.append(len(set(colors)))
        print("Colors: ", len(set(colors)))
        if (not is_valid(n, edges, colors)):
            print("Invalid Colouring!!!")
            print("File: ", filename)
            print("Algorithm: ", alg)
            input()
        print("Finished algorithm")
    colors_sdo, i_sdo = ig_sdo(n, edges)

    if (not is_valid(n, edges, colors_sdo)):
        print("Invalid Colouring!!!")
        print("File: ", filename)
        print("Algorithm: IG_SDO")
        input()

    colors_rlf, i_rlf = ig_rlf(n, edges)

    if (not is_valid(n, edges, colors_rlf)):
        print("Invalid Colouring!!!")
        print("File: ", filename)
        print("Algorithm: IG_RLF")
        input()

    results.append(len(set(colors_sdo)))
    results.append(i_sdo)
    results.append(len(set(colors_rlf)))
    results.append(i_rlf)
    writer.writerow([os.path.basename(filename), n, e] + results)


output=open('output.csv', 'w')

writer=csv.writer(output)

algorithms=["File", "|V|", "|E|", "FF", "LDF",
              "IDO", "SDO", "RLF", "IGSDO", "i", "IGRLF", "i"]

writer.writerow(algorithms)

for filename in sys.argv[1:]:
    test_all(filename, writer)
    print("Done testing file \'" + filename + "\'")
