#!/usr/bin/python

import sys
import time
import random
import unittest
sys.path.insert(0, 'knapsack')

from knapsack import Knapsack

class TestKnapsackClass(unittest.TestCase):
    def test_knapsack(self):
        # Problems to test
        problems = ['dynamic', 'bipercube', 'hypercube2', 'hypercube4', 'hypercube6', 'hypercube8']
        naive      = 0
        dynamic    = 0
        parallel   = 0
        bipercube  = 0
        hypercube2 = 0
        hypercube4 = 0
        hypercube6 = 0
        hypercube8 = 0

        # Variables
        capacity = 100
        elementCount = 100
        profitsRange = 100
        weigthsRange = 100

        values =  []
        weigths = []

        # Construct the Knapsack
        for i in range(elementCount):
            values.append(random.randint(1, profitsRange))
            weigths.append(random.randint(1, weigthsRange))

        knap = Knapsack(capacity, weigths, values)

        # Resolve

        # Dynamic
        start = time.time()
        dynamic = knap.dynamic()
        end = time.time()

        print "Dynamic time: " + str(end - start)

        # Naive
        if 'naive' in problems:
            start = time.time()
            naive = knap.naive()
            end = time.time()

            print "Naive time: " + str(end - start)

        # Parallel
        if 'parallel' in problems:
            start = time.time()
            parallel = knap.parallel()
            end = time.time()

            print "Parallel time: " + str(end - start)

        # Bipercube
        if 'bipercube' in problems:
            start = time.time()
            bipercube = knap.bipercube()
            end = time.time()

            print "Bipercube time: " + str(end - start)

        # Hypercube

        # 2 Processors
        if 'hypercube2' in problems:
            start = time.time()
            hypercube2 = knap.hypercube(2)
            end = time.time()

            print "Hypercube 2 time: " + str(end - start)

        # 4 Processors
        if 'hypercube4' in problems:
            start = time.time()
            hypercube4 = knap.hypercube(4)
            end = time.time()

            print "Hypercube 4 time: " + str(end - start)

        # 6 Processors
        if 'hypercube6' in problems:
            start = time.time()
            hypercube6 = knap.hypercube(6)
            end = time.time()

            print "Hypercube 6 time: " + str(end - start)

        # 8 Processors
        if 'hypercube8' in problems:
            start = time.time()
            hypercube8 = knap.hypercube(8)
            end = time.time()

            print "Hypercube 8 time: " + str(end - start)

        # Results

        # Naive
        if 'naive' in problems:
            self.assertEqual(naive, dynamic)

        # Parallel
        if 'parallel' in problems:
            self.assertEqual(parallel, dynamic)

        # Bipercube
        if 'bipercube' in problems:
            self.assertEqual(bipercube, dynamic)

        # 2 Processors
        if 'hypercube2' in problems:
            self.assertEqual(hypercube2, dynamic)

        # 4 Processors
        if 'hypercube4' in problems:
            self.assertEqual(hypercube4, dynamic)

        # 6 Processors
        if 'hypercube6' in problems:
            self.assertEqual(hypercube6, dynamic)

        # 8 Processors
        if 'hypercube8' in problems:
            self.assertEqual(hypercube8, dynamic)

        # self.assertEqual(parallel, parallelAprox)


if __name__ == '__main__':
    unittest.main()
