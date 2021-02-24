# `epic-hash` package

A package that helps you solve Google Hash Code competition in a systematic way.

## Installation

Go to `epic-hash` folder and run:

```bash
pip install .
```

Alternatively, you can also install it in an editable mode:

```bash
pip install . -e
```

## Content

- A runner class that handles reading input, writing output and validating and scoring output and execution of the solution.
- A utility function for parallelization.

## How To

An example, how to use the package, is in [`2020/practice`](https://github.com/AleksMat/hashcode-solutions/tree/master/2020/practice) folder. The procedure is the following:

1. At the beginning of the competition someone puts input files into `input` folder and pushes to git.
2. Someone implements utility functions for reading input, writing output and validating and scoring output. In the example functions are implemented in `solution_utils.py` script.
3. Each team member can start implementing solutions and using `epic-hash` in a way as shown in `solution1.py` script in the example.
4. When a solution is executed it will start producing outputs in a folder `output`. It will save an output if and only if it's score is better than a score of any previously saved output. The output naming convention is `<test case name>_<score>.out`.
5. Each team member commits and pushes their outputs with the highest scores.
6. Each team member can pull outputs from other team members to have them as a baseline for next executions. The merge conflicts could theoretically happen only if two members commit a different output with the same score...
7. Outputs can only be submitted to the competition site manually. Submitting them a few times during the competition should be enough.
