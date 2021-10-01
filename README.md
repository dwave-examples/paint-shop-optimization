
# Multi-car paint shop optimization

An example for generalization of binary paint shop optimization outlined in 
"Yarkoni et. al. Multi-car paint shop optimization with quantum annealing". 
The goal of the optimization is to minimize the number of color switches between cars in a paint shop queue. This problem is known to be NP-hard. We demonstrate
how to formulate this problem using `dimod.ConstrainedQuadraticModel`.

The problem instances used in this example are generated randomly. You can also
follow the example in `data/exp.yaml` to generate your instances. The instance in the mentioned file is taken from the paper by Yarkoni et. al.


The formulation of this optimization problem can be summarized as:
1) Minimize the number of color changes
2) Ensuring that the correct number of cars are colored white/black

Suppose that we have `N` cars in a sequence. Each car can be painted with black or white color. The goal of the optimization is to reduce the number of times color switches since there is a cost and waste associated with replacing the color.

In the original paper the authors work with spin variables that take the values {-1,1}, we instead work with binary variables with values in {0, 1}. A spin variable `s` can be converted to a binary variable `x` as follows.

![equation](http://latex.codecogs.com/gif.latex?x%20%3D%20%28s%20&plus;%201%29%20/%202)

We can optimize the number of color switches by counting the number of times the binary value of adjacent cars changes.

<img src="https://latex.codecogs.com/gif.latex?f_1 = \sum_{i=0}^{i=N-2}(x_i - x_{i+1})^2" />

Alternatively, we can reduce the number of color changes by minimizing a function that rewards (assigns negative value) assigning a similar color to adjacent cars. This function can easily be expressed in terms of spin variables. When two cars in the sequence have the same color, the product of their value is positive and if the colors are different, the product is negative.

<img src="https://latex.codecogs.com/gif.latex?f_2 = -\sum_{i=0}^{i=N-2} s_i s_{i+1}" />

equivalently, the equation above can be written as

<img src="https://latex.codecogs.com/gif.latex?f_2 = -\sum_{i=0}^{i=N-2} (2x_i - 1) (2x_{i+1}-1)" />

You can show that the number of color switches is related to the objective function that maximized the number of similar adjacent colors as shown below

<img src="https://latex.codecogs.com/gif.latex?N - 1 + f_2 = 2 f_1" />


## Usage

To run a small demo, run the command:

```bash
python carpaintshop.py --filename data/exp.yml
```

The command-line arguments specify the Python program, the keyword argument 
`filename`, and the path to the small data set. The small data set file includes a sequence of cars under `sequence` and the number of black cars to be painted black for each car ensemble under `counts`. 

To run the demo on a random instance, run the command:

```bash
python carpaintshop.py --num-cars 10
```

You can configure a seed, and a few other parameters to generate your desired
random problem. For the full list of parameters please see the docstring of the
`main` function in `carpaintshop.py`. 

## References

[1] Yarkoni et. al. Multi-car paint shop optimization with quantum annealing, 
[arxiv](https://arxiv.org/pdf/2109.07876.pdf)

## License

Released under the Apache License 2.0. See [LICENSE](LICENSE) file.
