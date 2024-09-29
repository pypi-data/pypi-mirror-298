#! /usr/bin/env python3

import unittest
import railwaypacriman.logger as lggr

class Join():
    def __init__(self):
        self.records = []

    def __str__(self):  # print() に放り込んだときに表示される文字列
        return self.records.__str__()

    def add(self, direction, activity):
        self.records.append([direction, activity])

    def unique_arrows(self):
        results = {}
        for i in self.records:
            results[tuple(i)] = 1
        return list(results.keys())

if __name__=="__main__":
    class TestJoin(unittest.TestCase):
        def test_init(self):
            j0 = Join()
            j0.add('up', 'run')

            actual = j0.unique_arrows()
            expected = [('up', 'run')]
            self.assertEqual(expected, actual)

            j0.add('down', 'run')
            actual = j0.unique_arrows()
            expected = [('up', 'run'), ('down', 'run')]
            self.assertEqual(expected, actual)

            j0.add('up', 'bike')
            actual = j0.unique_arrows()
            expected = [('up', 'run'), ('down', 'run'), ('up', 'bike')]
            self.assertEqual(expected, actual)

            j0.add('up', 'run')
            actual = j0.unique_arrows()
            expected = [('up', 'run'), ('down', 'run'), ('up', 'bike')]
            self.assertEqual(expected, actual)

        def test_str(self):
            j0 = Join()

            j0.add('up', 'run')
            expected = "[['up', 'run']]"
            actual = j0.__str__()
            self.assertEqual(expected, actual)

            j0.add('down', 'run')
            expected = "[['up', 'run'], ['down', 'run']]"
            actual = j0.__str__()
            self.assertEqual(expected, actual)

    unittest.main()

