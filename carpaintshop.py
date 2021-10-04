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

import numpy as np
import dimod
from dwave.system import LeapHybridCQMSampler
from fire import Fire
from warnings import warn
from helper import load_from_yml, bars_plot


# from Yarkoni et. al "Multi-car paint shop optimization with quantum
# annealing: "https://arxiv.org/pdf/2109.07876.pdf


def get_paint_shop_cqm(sequence, k, mode=1):
    """Create a CQM object for paint shop optimization problem

    Args:
        sequence (Iterable): the sequence of cars
        k (dict): dictionary of number of black colors for each car
        mode (int): Mode sets the objective type. If set to 1, it uses
            (x_i+1 - x_i)^2 as the objective to count the number of switches.
           If mode is set to any other number, it will use the objective in
            https://arxiv.org/pdf/2109.07876.pdf

    Returns:
        `dimod.ConstraintQuadraticModel`: A model object for optimization of
            paint shop color switches

    """
    x = [dimod.Binary(i) for i, car in enumerate(sequence)]
    cqm = dimod.ConstrainedQuadraticModel()
    num_switches = dimod.quicksum(
        (x[i + 1] - x[i]) ** 2 for i in range(len(x) - 1))
    if mode == 1:
        cqm.set_objective(num_switches)
    else:
        cqm.set_objective(dimod.quicksum(
            -(2 * x[i] - 1) * (2 * x[i + 1] - 1) for i in range(len(x) - 1)))

    for car, number in k.items():
        index = [i for i, c in enumerate(sequence) if c == car]
        constraint = dimod.quicksum(x[i] for i in index)
        cqm.add_constraint(constraint == number)
    return cqm, num_switches


def get_random_sequence(num_cars=5, seed=111, unique_cars=8,
                        min_colors=None, max_colors=None):
    """Generate a random paint shop problem

    Args:
        num_cars (int): The number of cars
        seed (int): The seed for random sequence generation
        unique_cars (int): The number of unique cars
        min_colors (int): Minimum number of black colors for each car
        max_colors (int): Maximum number of black colors for each car (default
            None, will set the max to a random number at most one less that
            the number of cars)

    Returns:
          tuple: The first one is an iterable of cars in a sequence. The second
            returned value is a mapping with cars and number of black colors as
            keys and values.

    """
    np.random.seed(seed)
    sequence = np.random.randint(0, unique_cars, size=num_cars)
    unique, counts = np.unique(sequence, return_counts=True)
    counts = dict(zip(unique, counts))
    mapping = {}
    for car, num_colors in counts.items():
        a = int(num_colors * 1 / 3) if not min_colors else min_colors
        b = int(num_colors * 2 / 3) if not max_colors else max_colors
        if b <= a:
            b = a + 1
        mapping[car] = np.random.randint(a, b)
    return sequence, mapping


def get_paint_shop_bqm(cqm: dimod.ConstrainedQuadraticModel, penalty=2.0):
    """Create a BQM object from a CQM assuming that only linear equality
    constraints are present.

    Args:
        cqm: The `dimod.ConstrainedQuadraticModel for paint shop optimization
        penalty (float): The strength of penalty coefficient for all the
            equality constraints

    Returns:
        `dimod.BinaryQuadraticModel`: A BQM model in which the equality
            constraints are converted to a quadratic objective.

    """
    bqm = dimod.BinaryQuadraticModel('BINARY')
    bqm.offset = cqm.objective.offset
    bqm.add_linear_from(cqm.objective.linear)
    bqm.add_quadratic_from(cqm.objective.quadratic)
    for c in cqm.constraints.values():
        bqm.update(penalty * (c.lhs - c.rhs) ** 2)
    return bqm


def main(num_cars=10, seed=111, mode=1,
         num_unique_cars=3, min_colors=None, max_colors=None,
         filename=None, time_limit=None, **config):
    """Run paint shop optimization demo using the CQM solver

    Args:
        num_cars (int): The number of cars
        seed (int): The seed for random sequence generation
        num_unique_cars (int): The number of unique cars
        min_colors (int): Minimum number of black colors for each car
        max_colors (int): Maximum number of black colors for each car (default
            None, will set the max to a random number at most one less that
            the number of cars)
        mode (int): Mode sets the objective type. If set to 1, it uses
            (x_i+1 - x_i)^2 as the objective to count the number of switches
            if mode is set to any other number, it will use the objective in
            https://arxiv.org/pdf/2109.07876.pdf
        filename (str): The name of sequence file in yaml form. If used,
            the parameters of random sequence generation will be ignored.
        time_limit (float): time_limit parameter for hybrid solver
        **config:
            Keyword arguments passed to :meth:`dwave.cloud.client.Client.from_config`.

    """
    if filename is None:
        sequence, mapping = get_random_sequence(num_cars, seed,
                                                num_unique_cars,
                                                min_colors, max_colors)
    else:
        sequence, mapping = load_from_yml(filename)

    print('Problem')
    print('-------')
    print(f'Number of cars: {len(sequence)}')
    print(f'Number of unique cars ensembles: {len(mapping)}')
    print(f'Number of cars need to be painted black: ')
    if len(mapping) <= 10:
        print(f'{mapping}')
    else:
        print('The list of values is too long')

    cqm, num_switches = get_paint_shop_cqm(sequence, mapping, mode)
    sampler = LeapHybridCQMSampler(**config)

    min_time_limit = sampler.min_time_limit(cqm)
    if time_limit and time_limit < min_time_limit:
        time_limit = min_time_limit
        warn('Time limit is less than the minimum allowed, '
             f'changing to the minimum allowed {min_time_limit}')

    sampleset = sampler.sample_cqm(cqm, time_limit=time_limit).aggregate()
    sampleset = sampleset.filter(lambda x: cqm.check_feasible(x.sample))
    if filename is None:
        image_name = f'color_sequence_image'
    else:
        image_name = f'{filename}_color_sequence_image'

    print('\nSolutions')
    print('---------')
    if len(sampleset) == 0:
        print('No feasible solution found.')
    else:
        sampleset = sampleset.truncate(3)
        for index, sample in enumerate(sampleset.samples()):
            if cqm.check_feasible(sample):
                print(f'{index + 1:}  ')
                print(f'Objective: '
                      f'{cqm.objective.energy(sample): 8.2f}, ', end='')
                print(f'Number of switches: '
                      f'{num_switches.energy(sample): 8.2f}')
                bars_plot(sample,
                          name=image_name + f'_{index}_{mode}.png')


if __name__ == '__main__':
    Fire(main)
