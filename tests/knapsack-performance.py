#!/usr/bin/python

import sys
import time
import random
import unittest
sys.path.insert(0, 'knapsack')

from knapsack import Knapsack

class TestKnapsackClass(unittest.TestCase):
    def test_knapsack(self):
        # Initial variables
        naive      = 0
        dynamic    = 0
        parallel   = 0
        bipercube  = 0
        hypercube2 = 0
        hypercube4 = 0
        hypercube6 = 0
        hypercube8 = 0
        
        # Problems to test
        problems = ['parallel']

        # File
        out = open("out.csv", 'w')  # csv output
        out.write(
            "Capacidad" + "\t" +
            "Elementos" + "\t" +
            "Naive" + "\t" +
            "Programacion dinamica" + "\t" +
            "2 procesadores" + "\t" +
            "4 procesadores" + "\t" +
            "6 procesadores" + "\t" +
            "8 procesadores" + "\t" +
            "Peters and Rudolph" + "\t" +
            "\n"
        )

        capacities = [100]
        elements = [100]

        for capacity in capacities:
            for element in elements:
                # Times
                naiveTime      = '-'
                dynamicTime    = '-'
                hypercube2Time = '-'
                hypercube4Time = '-'
                hypercube6Time = '-'
                hypercube8Time = '-'
                parallelTime   = '-'

                # Variables
                values =  []
                weigths = []

                # Construct the Knapsack
                for i in range(element):
                    values.append(random.randint(1, int(element / 2) ))
                    weigths.append(random.randint(1, int(element / 2) ))

                knap = Knapsack(capacity, weigths, values)

                # Resolve

                # Dynamic
                if 'dynamic' in problems:
                    start = time.time()
                    dynamic = knap.dynamic()
                    end = time.time()

                    dynamicTime = str(end - start)
                    print "Dynamic time: " + str(end - start)

                # Naive
                if 'naive' in problems:
                    start = time.time()
                    naive = knap.naive()
                    end = time.time()

                    naiveTime = str(end - start)
                    print "Naive time: " + str(end - start)

                # Parallel
                if 'parallel' in problems:
                    start = time.time()
                    parallel = knap.parallel()
                    end = time.time()

                    parallel = str(end - start)
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

                    hypercube2Time = str(end - start)
                    print "Hypercube 2 time: " + str(end - start)

                # 4 Processors
                if 'hypercube4' in problems:
                    start = time.time()
                    hypercube4 = knap.hypercube(4)
                    end = time.time()

                    hypercube4Time = str(end - start)
                    print "Hypercube 4 time: " + str(end - start)

                # 6 Processors
                if 'hypercube6' in problems:
                    start = time.time()
                    hypercube6 = knap.hypercube(6)
                    end = time.time()

                    hypercube6Time = str(end - start)
                    print "Hypercube 6 time: " + str(end - start)

                # 8 Processors
                if 'hypercube8' in problems:
                    start = time.time()
                    hypercube8 = knap.hypercube(8)
                    end = time.time()

                    hypercube8Time = str(end - start)
                    print "Hypercube 8 time: " + str(end - start)

                # File
                out.write(
                    str(capacity) + "\t" +
                    str(element) + "\t" +
                    str(naiveTime) + "\t" +
                    str(dynamicTime) + "\t" +
                    str(hypercube2Time) + "\t" +
                    str(hypercube4Time) + "\t" +
                    str(hypercube6Time) + "\t" +
                    str(hypercube8Time) + "\t" +
                    str(parallelTime) + "\t"
                )
                out.write("\n")

if __name__ == '__main__':
    unittest.main()
