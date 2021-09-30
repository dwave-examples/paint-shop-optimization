
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


## Usage

To run a small demo, run the command:

```bash
python carpaintshop.py --filename data/exp.yml
```

The command-line arguments specify the Python program, the keyword argument 
`filename`, and the path to the small data set. The small data set file includes 
sequence of cars under `sequence` and the number of black cars to be painted 
black for each car ensemble under `counts`. 

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
