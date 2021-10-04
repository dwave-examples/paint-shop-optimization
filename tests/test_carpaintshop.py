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
import uuid
import dimod
import unittest
from carpaintshop import get_paint_shop_cqm, get_random_sequence
from carpaintshop import get_paint_shop_bqm
from helper import bars_plot, load_from_yml, load_experiment_from_yml
from helper import save_sequence_to_yaml

# Add the parent path so that the test file can be run as a script in
# addition to using "python -m unittest" from the root directory
example_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(example_dir)


class TestCarPaintShop(unittest.TestCase):
    def test_sequence(self):
        sequence, counts = get_random_sequence(10, num_car_ensembles=5)
        self.assertEqual(len(sequence), 10)
        self.assertEqual(len(counts), 5)

    def test_solution(self):
        """Verify that the expected solution is obtained"""
        sequence = [1, 2, 3, 1, 2, 3]
        counts = {1: 1, 2: 1, 3: 1}
        cqm, _ = get_paint_shop_cqm(sequence, counts, mode=1)

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
        cqm, _ = get_paint_shop_cqm(sequence, counts, mode=2)

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
        cqm, objective = get_paint_shop_cqm(sequence, counts, mode=1)

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
        cqm, objective = get_paint_shop_cqm(sequence, counts, mode=2)

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

    def test_bqm(self):
        """Verify that the expected solution is obtained"""
        sequence = [1, 2, 3, 1, 2, 3]
        counts = {1: 1, 2: 1, 3: 1}
        cqm, objective = get_paint_shop_cqm(sequence, counts, mode=1)
        bqm = get_paint_shop_bqm(cqm, penalty=10)

        sample = {0: 1, 1: 1, 2: 1, 3: 0, 4: 0, 5: 0}
        self.assertAlmostEqual(bqm.energy(sample), 1)
        sample = {0: 1, 1: 1, 2: 1, 3: 1, 4: 0, 5: 0}
        self.assertAlmostEqual(bqm.energy(sample), 11)
        sample = {0: 1, 1: 0, 2: 1, 3: 0, 4: 1, 5: 0}
        self.assertAlmostEqual(bqm.energy(sample), 5)

    def test_bqm_mode2(self):
        """Verify that the expected solution is obtained"""
        sequence = [1, 2, 3, 1, 2, 3]
        counts = {1: 1, 2: 1, 3: 1}
        cqm, objective = get_paint_shop_cqm(sequence, counts, mode=2)
        bqm = get_paint_shop_bqm(cqm, penalty=10)

        sample = {0: 1, 1: 1, 2: 1, 3: 0, 4: 0, 5: 0}
        self.assertAlmostEqual(bqm.energy(sample), -3)
        sample = {0: 1, 1: 1, 2: 1, 3: 1, 4: 0, 5: 0}
        self.assertAlmostEqual(bqm.energy(sample), 7)
        sample = {0: 1, 1: 0, 2: 1, 3: 0, 4: 1, 5: 0}
        self.assertAlmostEqual(bqm.energy(sample), 5)


class TestHelper(unittest.TestCase):

    def test_smoke(self):
        bars_plot({0: 0, 1: 1, 2: 0, 3: 1}, show=False, save=False)

    def test_smoke_array(self):
        bars_plot([0, 1, 1, 1, 0, 0, 1], show=False, save=False)

    def test_image_saved(self):
        filename = str(uuid.uuid4())
        bars_plot({0: 0, 1: 1, 2: 0, 3: 1}, show=False, save=True,
                  name=filename)
        full_path = os.path.join('images', filename + '.png')
        self.assertTrue(os.path.exists(full_path))
        os.remove(full_path)

    def test_image_array_saved(self):
        filename = str(uuid.uuid4())
        bars_plot([0, 1, 1, 1, 0, 0, 1], show=False, save=True,
                  name=filename)
        full_path = os.path.join('images', filename + '.png')
        self.assertTrue(os.path.exists(full_path))
        os.remove(full_path)

    def test_image_array_saved_no_folder(self):
        filename = str(uuid.uuid4())
        folder = str(uuid.uuid4())
        if os.path.exists(folder):
            os.rmdir(folder)
        bars_plot([0, 1, 1, 1, 0, 0, 1], show=False, save=True,
                  name=filename, folder_name=folder)
        full_path = os.path.join(folder, filename + '.png')
        self.assertTrue(os.path.exists(full_path))
        os.remove(full_path)
        os.rmdir(folder)

    def test_image_sampleset(self):
        sampleset = dimod.SampleSet.from_samples(
            [{0: 0, 1: 1, 2: 0, 3: 1}], 'BINARY', energy=[0])
        bars_plot(sampleset, show=False, save=False)

    def test_load_yaml(self):
        load_from_yml('data/exp.yml')

    def test_load_exp_yaml(self):
        load_experiment_from_yml('data/exp.yml')

    def test_save_sequence(self):
        filename = str(uuid.uuid4()) + '.yml'
        seq = [0, 0, 1, 1, 1, 3, 3, 3, 2, 2, 2]
        counts = {0: 1, 1: 2, 3: 1, 2: 2}
        save_sequence_to_yaml(seq, counts, filename)
        seq2, counts2 = load_from_yml(filename)
        self.assertEqual(seq, seq2)
        self.assertEqual(counts, counts2)
        os.remove(filename)
