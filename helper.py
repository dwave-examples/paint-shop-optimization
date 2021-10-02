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

import yaml
import dimod
import numpy as np
import matplotlib.pyplot as plt
from typing import Mapping
import os


_golden_ratio = (1 + 5 ** 0.5) / 2


def load_from_yml(filename):
    """Load an experiment configuration from a yaml file. For examples,
    take a look at `data` folder

    Args:
        filename (str): The name of the data file (use full or relative path)

    Returns:
          tuple: The first one is an iterable of cars in a sequence. The second
            returned value is a mapping with cars and number of black colors as
            keys and values.

    """

    with open(filename, 'r') as file_handle:
        data = next(iter(yaml.safe_load_all(file_handle)))
    sequence = data['sequence']
    k = data['counts']
    return sequence, k


def load_experiment_from_yml(filename):
    """Load an experiment configuration from a yaml file. For examples,
    take a look at `benchmark_experiments` folder

    Args:
        filename (str): The name of the experiment file (use full or
            relative path)

    Returns:
        dict: The yaml file as a dictionary

    """
    with open(filename, 'r') as file_handle:
        data = next(iter(yaml.safe_load_all(file_handle)))
    return data


def bars_plot(sampleset, show=False, save=True, name='image.png'):
    """Create a bar image for a given binary string.

    Args:
        sampleset (dimod.SampleSet): `dimod.SampleSet` or a sample-like
        show (bool): Whether to show the plot (default=False)
        save (bool): Whether to save the plot (default=True)
        name (str): A file name to save the plot (default='image.png')

    """
    if isinstance(sampleset, dimod.SampleSet):
        sample = sampleset.first.sample
        sample = [sample[v] for v in sampleset.variables]
    elif isinstance(sampleset, Mapping):
        sample = [v for key, v in sampleset.items()]
    else:
        sample = sampleset

    width = int(len(sample) / _golden_ratio)
    sample = 1 - np.array(sample)
    plt.imshow(np.repeat(sample, width).reshape(-1, width).T, cmap='gray')
    plt.yticks([])
    if save:
        filename = os.path.basename(name)
        plt.savefig(os.path.join('images', filename))
    if show:
        plt.show()


if __name__ == '__main__':
    bars_plot({0: 1.0, 1: 1.0, 2: 1.0, 3: 1.0, 4: 0.0, 5: 0.0, 6: 0.0, 7: 0.0,
               8: 0.0, 9: 0.0, 10: 1.0, 11: 1.0, 12: 1.0, 13: 1.0})
