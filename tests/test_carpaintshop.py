# Copyright 2021 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import unittest
from carpaintshop import get_paint_shop_cqm, get_random_sequence

# Add the parent path so that the test file can be run as a script in
# addition to using "python -m unittest" from the root directory
example_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(example_dir)


class TestCarPaintShop(unittest.TestCase):
    def test_sequence(self):
        sequence, counts = get_random_sequence(10, unique_cars=5)
        self.assertEqual(len(sequence), 10)
        self.assertEqual(len(counts), 5)

    def test_solution(self):
        """Verify that the expected solution is obtained"""
        sequence = [1, 2, 3, 1, 2, 3]
        counts = {1: 1, 2: 1, 3: 1}
        cqm = get_paint_shop_cqm(sequence, counts, mode=1)

        sample = {0: 1, 1: 1, 2: 1, 3: 0, 4: 0, 5: 0}
        self.assertTrue(cqm.check_feasible(sample))
        self.assertAlmostEqual(cqm.objective.energy(sample), 1)
        sample = {0: 1, 1: 1, 2: 1, 3: 1, 4: 0, 5: 0}
        self.assertFalse(cqm.check_feasible(sample))
        self.assertAlmostEqual(cqm.objective.energy(sample), 1)
        sample = {0: 1, 1: 0, 2: 1, 3: 0, 4: 1, 5: 0}
        self.assertTrue(cqm.check_feasible(sample))
        self.assertAlmostEqual(cqm.objective.energy(sample), 5)

    def test_solution_mode2(self):
        """Verify that the expected solution is obtained"""
        sequence = [1, 2, 3, 1, 2, 3]
        counts = {1: 1, 2: 1, 3: 1}
        cqm = get_paint_shop_cqm(sequence, counts, mode=2)

        sample = {0: 1, 1: 1, 2: 1, 3: 0, 4: 0, 5: 0}
        self.assertTrue(cqm.check_feasible(sample))
        self.assertAlmostEqual(cqm.objective.energy(sample), -3)
        sample = {0: 1, 1: 1, 2: 1, 3: 1, 4: 0, 5: 0}
        self.assertFalse(cqm.check_feasible(sample))
        self.assertAlmostEqual(cqm.objective.energy(sample), -3)
        sample = {0: 1, 1: 0, 2: 1, 3: 0, 4: 1, 5: 0}
        self.assertTrue(cqm.check_feasible(sample))
        self.assertAlmostEqual(cqm.objective.energy(sample), 5)

    def test_solution2(self):
        """Verify that the expected solution is obtained"""
        sequence = [1, 2, 3, 1, 2, 3]
        counts = {1: 1, 2: 1, 3: 1}
        cqm, objective = get_paint_shop_cqm(sequence, counts, mode=1,
                                            return_objective=True)

        sample = {0: 1, 1: 1, 2: 1, 3: 0, 4: 0, 5: 0}
        self.assertTrue(cqm.check_feasible(sample))
        self.assertAlmostEqual(cqm.objective.energy(sample), 1)
        self.assertAlmostEqual(objective.energy(sample), 1)
        sample = {0: 1, 1: 1, 2: 1, 3: 1, 4: 0, 5: 0}
        self.assertFalse(cqm.check_feasible(sample))
        self.assertAlmostEqual(cqm.objective.energy(sample), 1)
        self.assertAlmostEqual(objective.energy(sample), 1)
        sample = {0: 1, 1: 0, 2: 1, 3: 0, 4: 1, 5: 0}
        self.assertTrue(cqm.check_feasible(sample))
        self.assertAlmostEqual(cqm.objective.energy(sample), 5)
        self.assertAlmostEqual(objective.energy(sample), 5)

    def test_solution2_mode2(self):
        """Verify that the expected solution is obtained"""
        sequence = [1, 2, 3, 1, 2, 3]
        counts = {1: 1, 2: 1, 3: 1}
        cqm, objective = get_paint_shop_cqm(sequence, counts, mode=2,
                                            return_objective=True)

        sample = {0: 1, 1: 1, 2: 1, 3: 0, 4: 0, 5: 0}
        self.assertTrue(cqm.check_feasible(sample))
        self.assertAlmostEqual(cqm.objective.energy(sample), -3)
        self.assertAlmostEqual(objective.energy(sample), 1)
        sample = {0: 1, 1: 1, 2: 1, 3: 1, 4: 0, 5: 0}
        self.assertFalse(cqm.check_feasible(sample))
        self.assertAlmostEqual(cqm.objective.energy(sample), -3)
        self.assertAlmostEqual(objective.energy(sample), 1)
        sample = {0: 1, 1: 0, 2: 1, 3: 0, 4: 1, 5: 0}
        self.assertTrue(cqm.check_feasible(sample))
        self.assertAlmostEqual(cqm.objective.energy(sample), 5)
        self.assertAlmostEqual(objective.energy(sample), 5)


if __name__ == '__main__':
    unittest.main()
