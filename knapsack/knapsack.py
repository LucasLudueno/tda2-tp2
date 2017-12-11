import multiprocessing as mp
from multiprocessing import Pool

# Dynamic resolution passing a list of params
def resolveDynamicParallel(params):
    capacity = params[0]
    weights = params[1]
    profits = params[2]
    n = params[3]

    return resolveDynamic(capacity, weights, profits, n)[n]

# Dynamic resolution passing params
def resolveDynamic(capacity, weights, values, n, queueResult = None):
    K = [[0 for x in range(capacity + 1)] for x in range(n + 1)]

    # Build table K[][] in bottom up manner
    for i in range(n + 1):
        for w in range(capacity + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif weights[i - 1] <= w:
                K[i][w] = max(values[i - 1] + K[i - 1][w - weights[i - 1]],  K[i - 1][w])
            else:
                K[i][w] = K[i - 1][w]

    if queueResult == None:
        return K
    queueResult.put(K)

# Combine profits in parallel
def combineProfitsParallel(profits, capacity, queueResult = None):
    if len(profits) == 1:
        if queueResult != None:
            return queueResult.put(profits[0])
        return profits[0]

    middle = int(len(profits) / 2)
    p1 = profits[0 : middle]
    p2 = profits[middle: ]

    queue = mp.Queue()
    pool = mp.Process(target = combineProfitsParallel, args = (p1, capacity, queue, ))
    pool.start()

    r1 = combineProfitsParallel(p2, capacity)
    r2 = queue.get()

    result = []

    for i in range(capacity + 1):
        maxProfit = 0

        for j in range(i + 1):
            value = r1[j] + r2[i - j]

            if value > maxProfit:
                maxProfit = value
            
        result.append(maxProfit)
    
    if queueResult != None:
        return queueResult.put(result)
    return result


class Knapsack:
    def __init__(self, capacity, weights, values):
        self.capacity = capacity
        self.weights = weights
        self.values = values
        self.n = len(values)

    # Naive
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

    # Dynamic
    def dynamic(self):
        solution = resolveDynamic(self.capacity, self.weights, self.values, self.n)

        return solution[self.n][self.capacity]

    # Bypercube
    def bipercube(self):
        processors = 2
        middle = int(self.n / processors)

        bWeights = self.weights[0 : middle]
        bProfits = self.values[0 : middle]
        dWeights = self.weights[middle:]
        dProfits = self.values[middle:]

        # Resolve parallel
        queue = mp.Queue()
        pool = mp.Process(target = resolveDynamic, args = (self.capacity, bWeights, bProfits, len(bWeights), queue, ))
        pool.start()

        d = resolveDynamic(self.capacity, dWeights, dProfits, len(dWeights))[len(dWeights)]
        b = queue.get()[len(bWeights)]

        # Join results
        result = []

        for i in range(self.capacity + 1):
            maxProfit = 0

            for j in range(i + 1):
                value = b[j] + d[i - j]

                if value > maxProfit:
                    maxProfit = value
                
            result.append(maxProfit)
        
        return result[-1]

    # Hypercube
    def hypercube(self, processors = 2):
        params = []

        # Divide processors
        division = int(self.n / processors)

        for proc in range(processors):
            init = proc * division
            end = (proc + 1) * division

            weights = []
            profits = []

            if proc == (processors - 1):
                weights = self.weights[init :]
                profits = self.values[init :]  
            else:
                weights = self.weights[init : end]
                profits = self.values[init : end]
            
            params.append([self.capacity, weights, profits, len(weights)])

        # Resolve parallel
        pool = Pool(processes = processors)
        dynamicResults = pool.map(resolveDynamicParallel, params)

        # Join results
        result = combineProfitsParallel(dynamicResults, self.capacity)

        return result[-1]


    # Peters and Rudolph
    def parallel(self):
        resultSet = self.resolveParalell(0, self.n - 1)

        return max(resultSet, key=lambda x:x[1])[1]

    def resolveParalell(self, i, j, queueResult = None):
        result = []
        
        if i == j:
            # Base case
            weight = self.weights[i]
            value = self.values[i]

            result = [(0, 0)]

            if (weight <= self.capacity):
                result.append((weight, value))
        else:
            # Resolve Parallel
            queue = mp.Queue()
            pool = mp.Process(target = self.resolveParalell, args = (i, (i + j) / 2, queue, ))
            pool.start()
            g2 = self.resolveParalell((i + j) / 2 + 1, j)
            g1 = queue.get()

            # Calculate combinations
            for s1 in g1:
                for s2 in g2:
                    weight = s1[0] + s2[0]
                    value = s1[1] + s2[1]

                    if weight <= self.capacity:
                        result.append((weight, value))

            # Remove repeated solutions
            result = list(set(result))
        
        if (queueResult != None):
            queueResult.put(result)
        return result


    # Peters and Rudolph Aprox approach
    def parallelAprox(self):
        resultSet = self.resolveParalellAprox(0, self.n - 1)

        return max(resultSet, key = lambda x:x[1])[1]

    def merge(self, g1, g2, k, l):
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

        return result
