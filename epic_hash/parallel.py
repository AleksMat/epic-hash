"""
A module implementing utilities for parallelization
"""
import itertools as it
from concurrent.futures import ProcessPoolExecutor

from tqdm.auto import tqdm


def parallelize(function, input, runner, param_list, workers=None):
    """ Executes the function in parallel

    :param function: A function to execute in parallel
    :type function: function
    :param input: An input object
    :type input: object
    :param runner
    :type Runner
    :param param_list: A list of tuples of parameters. Each tuple defines parameters for a single execution.
    :type param_list: list(tuple)
    :param workers: A number of concurrent processes used. Default is `None`, which will use all available processes
        on your machine.
    :type workers: int
    """
    process_num = len(param_list)

    if workers == 1:
        for params in tqdm(param_list, total=process_num):
            function(input, runner, *params)

    with ProcessPoolExecutor(max_workers=workers) as executor:
        list(tqdm(executor.map(
            function,
            it.repeat(input, times=process_num),
            it.repeat(runner, times=process_num),
            *list(zip(*param_list))
        ), total=process_num))
