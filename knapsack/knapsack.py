import multiprocessing as mp
from multiprocessing import Pool

def resolveCombinations(combTuple):
    oneSolution = combTuple[0]
    multSolutions = combTuple[1]
    capacity = combTuple[2]
    results = []

    for solution in multSolutions:
        weight = oneSolution[0] + solution[0]
        value = oneSolution[1] + solution[1]

        if weight <= capacity:
            results.append((weight, value))

    return results

class Knapsack:
    """

    """

    def __init__(self, capacity, weights, values):
        self.capacity = capacity
        self.weights = weights
        self.values = values
        self.n = len(values)

    def naive(self):
        return self.resolveNaive(self.capacity, self.weights, self.values, self.n)

    def resolveNaive(self, capacity, weights, values, n):
        # Base Case
        if n == 0 or capacity == 0 :
            return 0
    
        # If weight of the nth item is more than Knapsack of capacity
        # W, then this item cannot be included in the optimal solution
        if (weights[n - 1] > capacity):
            return self.resolveNaive(capacity , weights , values , n - 1)
    
        # return the maximum of two cases:
        # (1) nth item included
        # (2) not included
        else:
            return max(values[n - 1] + self.resolveNaive(capacity-weights[n - 1] , weights , values , n - 1),
                    self.resolveNaive(capacity , weights , values , n - 1))

    def dynamic(self):
        K = [[0 for x in range(self.capacity + 1)] for x in range(self.n + 1)]
    
        # Build table K[][] in bottom up manner
        for i in range(self.n + 1):
            for w in range(self.capacity + 1):
                if i == 0 or w == 0:
                    K[i][w] = 0
                elif self.weights[i - 1] <= w:
                    K[i][w] = max(self.values[i - 1] + K[i - 1][w - self.weights[i - 1]],  K[i - 1][w])
                else:
                    K[i][w] = K[i - 1][w]
    
        return K[self.n][self.capacity]


    def noParallel(self):
        resultSet = self.resolveNoParalell(0, self.n - 1)

        return max(resultSet, key=lambda x:x[1])[1]

    def parallel(self):
        resultSet = self.resolveParalell(0, self.n - 1)

        return max(resultSet, key=lambda x:x[1])[1]

    def resolveNoParalell(self, i, j):
        result = []
        if i == j:
            weight = self.weights[i]
            value = self.values[i]

            result = [(0, 0)]

            if (weight <= self.capacity):
                result.append((weight, value))
        else:
            # Divide items
            g1 = self.resolveNoParalell(i, (i + j) / 2)
            g2 = self.resolveNoParalell((i + j) / 2 + 1, j)

            # Calculate combinations

            for s1 in g1:
                for s2 in g2:
                    weight = s1[0] + s2[0]
                    value = s1[1] + s2[1]

                    if weight <= self.capacity:
                        result.append((weight, value))

            # Remove repeated solutions

            # max = (9223372036854775807, 0)
            # result = []
            # for s1 in g1:
            #     for s2 in g2:
            #         weight = s1[0] + s2[0]
            #         value = s1[1] + s2[1]

            #         if weight >= max[0] and value <= max[1]:
            #             continue
            #         elif abs(weight - value) < abs(max[0] - max[1]):
            #             max = (weight, value)

            #         if weight <= self.capacity:
            #             result.append((weight, value))

        return result

    def resolveParalell(self, i, j, queueResult = None):
        result = []
        if i == j:
            weight = self.weights[i]
            value = self.values[i]

            result = [(0, 0)]

            if (weight <= self.capacity):
                result.append((weight, value))
        else:
            # Divide items
            queue = mp.Queue()
            pool = mp.Process(target = self.resolveParalell, args = (i, (i + j) / 2, queue, ))
            pool.start()
            g2 = self.resolveParalell((i + j) / 2 + 1, j)
            pool.join()
            g1 = queue.get()

            # Calculate combinations in parallel

            # combinations = []
            # for solution in g1:
            #     combinations.append([solution, g2, self.capacity])

            # pool = Pool(processes = 6)
            # combinationResults = pool.map(resolveCombinations, combinations)

            # for combination in combinationResults:
            #     result = result + combination

            # Calculate combinations
            for s1 in g1:
                for s2 in g2:
                    weight = s1[0] + s2[0]
                    value = s1[1] + s2[1]

                    if weight <= self.capacity:
                        result.append((weight, value))

            # Remove repeated solutions
        
        if (queueResult != None):
            queueResult.put(result)
        return result


    def parallelAprox(self):
        resultSet = self.resolveParalellAprox(0, self.n - 1)

        return max(resultSet, key=lambda x:x[1])[1]

    def merge(self, g1, g2, k, l):
        print k, l
        result = []

        if k == l:
            for s1 in g1:
                for s2 in g2:
                    weight = s1[0] + s2[0]
                    value = s1[1] + s2[1]

                    if weight <= self.capacity:
                        result.append((weight, value))
        else:
            # Divide items
            g3 = self.resolveParalellAprox(k, (k + l) / 2)
            g4 = self.resolveParalellAprox((k + l) / 2 + 1, l)

            h1 = self.merge(g1, g3, k, (k + l) / 2)
            h2 = self.merge(g1, g4, (k + l) / 2 + 1, l)

            dh1 = {h : True for h in h1}
            dh2 = {h : True for h in h2}

            # print "DICTIONARY", dh1, h1

            t = []
            for r in g1:
                for g in g3:
                    tuple = (r[0] + g[0], r[1] + g[1])
                    if dh1.has_key(tuple):
                        t.append(tuple)

                for g in g4:
                    tuple = (r[0] + g[0], r[1] + g[1])
                    if dh2.has_key(tuple):
                        t.append(tuple)
            
            for s1 in g2:
                for t1 in t:
                    weight = s1[0] + t1[0]
                    value = s1[1] + t1[1]

                    if weight <= self.capacity:
                        result.append((weight, value))
        
        return result


    def resolveParalellAprox(self, i, j):
        result = []
        if i == j:
            weight = self.weights[i]
            value = self.values[i]

            result = [(0, 0)]

            if (weight <= self.capacity):
                result.append((weight, value))
        else:
            # Divide items
            g1 = self.resolveParalellAprox(i, (i + j) / 2)
            g2 = self.resolveParalellAprox((i + j) / 2 + 1, j)

            # Divide g2
            result = self.merge(g1, g2, (i + j) / 2 + 1, j)
            print "RESULT", result

        return result
