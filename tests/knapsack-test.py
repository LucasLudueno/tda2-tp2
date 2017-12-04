#!/usr/bin/python

import sys
import time
import random
import unittest
sys.path.insert(0, 'knapsack')

from knapsack import Knapsack

class TestKnapsackClass(unittest.TestCase):
    def test_knapsack(self):
        lamda = 0.2
        values = [] #[1, 10, 500, 30, 60, 100, 120]
        weigths = [] #[15, 150, 120, 100, 10, 20, 30]
        capacity = 200

        for i in range(50):
            values.append(random.randint(0, 300))
            weigths.append(random.randint(0, 300))

        # values = [300, 64, 198, 173, 111, 194, 41, 237, 189, 234, 246, 73, 236, 230, 213, 155, 8, 171, 119, 177, 179, 187, 150, 104, 165, 191, 149, 31, 284, 82, 77, 192, 104, 16, 125, 152, 83, 173, 143, 100, 240, 287, 12, 230, 134, 78, 97, 238, 255, 48, 208, 286, 163, 217, 119, 16, 246, 300, 79, 268]
        # weigths = [13, 176, 67, 158, 8, 272, 256, 202, 91, 64, 161, 135, 0, 215, 116, 20, 105, 49, 206, 131, 61, 177, 2, 260, 70, 11, 128, 256, 241, 274, 252, 18, 14, 114, 149, 117, 72, 274, 48, 148, 53, 183, 171, 278, 246, 179, 200, 139, 151, 264, 232, 230, 39, 51, 262, 108, 159, 235, 215, 98]

        knap = Knapsack(capacity, weigths, values)

        # start = time.time()
        # naive = knap.naive()
        # end = time.time()

        # print "Naive time: " + str(end - start)

        # start = time.time()
        # dynamic = knap.dynamic()
        # end = time.time()

        # print "Dynamic time: " + str(end - start)

        # start = time.time()
        # noParallel = knap.noParallel()
        # end = time.time()

        # print "No Parallel time: " + str(end - start)

        # start = time.time()
        # parallel = knap.parallel()
        # end = time.time()

        # print "Parallel time: " + str(end - start)

        # values = [v * lamda for v in values]
        # knap.values = values

        # start = time.time()
        # parallelAprox = knap.parallel() / lamda
        # end = time.time()

        # print "Parallel Aprox time: " + str(end - start)

        start = time.time()
        parallelBetterAprox = knap.parallelAprox()
        end = time.time()

        print "Parallel Better Aprox time: " + str(end - start)


        # self.assertEqual(naive, 220)
        # self.assertEqual(dynamic, parallel)
        self.assertEqual(200, parallel)
        # self.assertEqual(parallel, parallelAprox)


if __name__ == '__main__':
    unittest.main()
