"""
The main module for running Hash Code solutions
"""
import copy
import os

from .exceptions import OutputValidationError


class Runner:
    """ The main class that runs the entire process

    It's public methods are:
        - run
        - submit
    """
    def __init__(self, *, solution, location, load_input, save_output, validate_and_score_output,
                 report_all_scores=False):
        """
        :param solution: A solution function
        :type solution: function
        :param location: Location of the solution, this will be used to find input and output folders
        :type location: str
        :param load_input: A function that loads input
        :type load_input: function
        :param save_output: A function that saves output
        :type save_output: function
        :param validate_and_score_output: A function that validates and scores output
        :type validate_and_score_output: function
        :param report_all_scores: If `True` it will print scores for every submit, even if they are not the best
        :type report_all_scores: bool
        """
        self.solution = solution
        self.load_input = load_input
        self.save_output = save_output
        self.validate_and_score_output = validate_and_score_output
        self.report_all_scores = report_all_scores

        self.input_folder = None
        self.output_folder = None
        self.test_cases = []
        self._prepare_io(location)

        self.chosen_test_case = None
        self.input = None

    def _prepare_io(self, location):
        """ Collects input and output paths and input test case names
        """
        round_folder = os.path.dirname(location)
        self.input_folder = os.path.join(round_folder, 'input')
        self.output_folder = os.path.join(round_folder, 'output')

        if not os.path.exists(self.input_folder):
            raise IOError(f'Input folder not found at location {self.input_folder}')
        if not os.path.exists(self.output_folder):
            os.mkdir(self.output_folder)

        for filename in os.listdir(self.input_folder):
            if filename.endswith('.in'):
                self.test_cases.append(filename.rsplit('.', 1)[0])
        self.test_cases.sort()

        if not self.test_cases:
            raise IOError(f'There should be at least one test case in input folder {self.input_folder}')

    def run(self, test_case=None, **kwargs):
        """ A method that starts to run the solution evaluation

        :param test_case: Either an index of test case (sorted alphabetically) or a name. In case it is None this will
            run solution on all test cases
        :type test_case: int or str or None
        :param kwargs: Any keyword arguments that will be passed forward to the solution function
        """
        if test_case is None:
            for test_case in self.test_cases:
                self.run(test_case=test_case, **kwargs)
            return

        self.chosen_test_case = self._parse_test_case_input(test_case)

        input_path = os.path.join(self.input_folder, f'{self.chosen_test_case}.in')
        self.input = self.load_input(input_path)

        print(f'Starting to run a solution for test case {self.chosen_test_case}')
        self.solution(copy.deepcopy(self.input), self, **kwargs)

    def _parse_test_case_input(self, test_case):
        """ A helper function that parses parameter test_case
        """
        if isinstance(test_case, str):
            if test_case.endswith('.in'):
                test_case = test_case.rsplit('.', 1)[0]

            if test_case not in self.test_cases:
                raise ValueError(f"Parameter 'test_case' should be one of the {self.test_cases}, but {test_case} "
                                 f"was given")
            return test_case

        if isinstance(test_case, int):
            test_count = len(self.test_cases)
            if not 0 <= test_case < test_count:
                raise ValueError(f"Parameter 'test_case' can only be an integer from interval [0, {test_count}), "
                                 f"but {test_case} was given")
            return self.test_cases[test_case]

        raise ValueError(f"Parameter 'test_case' can only be a string, an integer or None, but {test_case} was given")

    def submit(self, output, suppress_errors=False):
        """ A method for submitting the output

        :param output: A problem output
        :type output: object
        :param suppress_errors: If `True` it will suppress validation errors and end silently. Default is `False`.
        :type suppress_errors: bool
        """
        errors_to_catch = OutputValidationError if suppress_errors else ()
        try:
            score = self.validate_and_score_output(self.input, output)
        except errors_to_catch:
            return

        max_score = self._collect_max_score()

        if score > max_score:
            print(f'Test case {self.chosen_test_case}: score improved {max_score} -> {score}')

            output_filename = f'{self.chosen_test_case}_{score}.out'
            output_path = os.path.join(self.output_folder, output_filename)

            if not os.path.exists(output_path):
                self.save_output(output_path, output)
        elif self.report_all_scores:
            print(f'Obtained score {score} (best score is {max_score})')

    def _collect_max_score(self):
        """ Collects currently max score by checking at output filenames
        """
        max_score = 0
        for filename in os.listdir(self.output_folder):
            if filename.startswith(self.chosen_test_case):
                filename = filename.rsplit('.', 1)[0]
                score = int(filename.rsplit('_', 1)[1])

                max_score = max(score, max_score)

        return max_score
