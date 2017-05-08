from math import log2, pow, sqrt
from sympy import LambertW
from complexity.logger import Logger
import complexity.logger
from complexity.myexceptions import FewMeasurePointsException
import stopit
from timeit import default_timer


def sample_exception_handler(function):
    def handler(*args):
        try:
            return function(*args)
        except FewMeasurePointsException:
            print("Not enough sample to even guess complexity of function\n)"
                  "Complexity of your algorithm is over O(n^5)."
                  "for default timeout")
            return

    return handler


class ComplexityAndTime:
    def __init__(self, timeout):
        self.logger = Logger()
        self.complexity = None
        self.iterations = 0
        self.time = timeout
        self.single_elem_time = 0
        w, h = 9, 2
        self.time_matrix = [[0 for x in range(w)] for y in range(h)]

    @complexity.logger.log_fun
    @sample_exception_handler
    def approximation(self, fun, initialize_data, cleaning_function):
        def measure():
            with stopit.ThreadingTimeout(self.time) as stop:
                assert stop.EXECUTING == stop.state
                self.measurements(fun, initialize_data, cleaning_function)
            self.check_time(stop)

        measure()
        return self.complexity

    @complexity.logger.log_fun
    def measurements(self, function, initialize_data, cleaning_function):
        self.logger.log_msg("Starting measuring complexity of function: " + function.__name__, 'INFO')
        result = []
        for q in range(3):
            start_size = 1000
            for i in range(2):
                time1 = self.time_function(initialize_data, start_size, function)
                for j in range(9):
                    self.time_matrix[i][j] += (time1[j])
                start_size += 3000
                self.iterations += 1
        for x in range(9):
            result.append(abs(1 - (self.time_matrix[1][x] / 3) / (self.time_matrix[0][x] / 3)))
            self.logger.log_msg(list(ComplexityFunctions.complexities.keys())[x] + " difference from set function is "
                                + str(result[x]), 'INFO')
        min_index = result.index(min(result))
        self.single_elem_time = self.time_matrix[1][min_index]
        self.complexity = list(ComplexityFunctions.complexities.keys())[min_index]
        self.logger.log_msg("\n", 'INFO')
        cleaning_function()

    def time_function(self, initialize_data, data_size, function):
        test_counter = 0
        data = initialize_data(data_size)
        time_start = default_timer()
        function(data)
        time_end = default_timer()
        proper_time = time_end - time_start
        time_list = []
        for iterator in ComplexityFunctions.complexities.values():
            time_list.append(proper_time / iterator(data_size))
        test_counter += 1
        self.logger.log_msg("Finished test " + str(test_counter), 'INFO')
        return time_list

    def get_complexity(self):
        return "Probably complexity of your function: " + self.complexity

    def check_time(self, stop):
        if stop.TIMED_OUT == stop.state:
            if self.time_matrix[1][8] == 0 or self.iterations % 2 != 0:
                self.complexity = 'n^5'
                raise FewMeasurePointsException
            else:
                incomplete_result = []
                diver = self.iterations / 2
                for x in range(9):
                    incomplete_result.append(
                        abs(1 - (self.time_matrix[1][x] / diver) / (self.time_matrix[0][x] / diver)))
                min_index = incomplete_result.index(min(incomplete_result))
                if min_index < 8:
                    min_index += 1
                self.complexity = list(ComplexityFunctions.complexities.keys())[min_index]
                print("Coulnd't gather enough data to approximate function \n"
                      "Probably function has not higher complexity than: " + self.complexity)

    @complexity.logger.log_fun
    def time_for_data(self, initialize_data, size, function, cleaning_function):
        if self.complexity is None:
            self.approximation(function, initialize_data, cleaning_function)
        else:
            if self.single_elem_time == 0:
                print("Time_for_data fun error. Couldnt't get sample due to timeout in approximation function\n")
                return
            print("Probably time for execute that algorithm for: " + str(size) + ' elements is ' +
                  str(self.single_elem_time * ComplexityFunctions.complexities.get(self.complexity)(size)) +
                  ' seconds.')

    @complexity.logger.log_fun
    def max_size_pred(self, function, initialize_data, cleaning_function, time):
        if self.complexity is None:
            self.approximation(function, initialize_data, cleaning_function)
        else:
            if self.single_elem_time == 0:
                print("Time_for_data fun error. Couldnt't get sample due to timeout in approximation function\n")
                return
            print("Probably size of problem for time: " + str(time) + 's is ' +
                  str(ComplexityFunctions.complexities.get(self.complexity)(int(time / self.single_elem_time))) +
                  ' elements.')

    @complexity.logger.log_fun
    def all_in(self, function, initialize_data, cleaning_function, size, time):
        print("Starting all-in function!\n")
        self.approximation(function, initialize_data, cleaning_function)
        self.time_for_data(initialize_data, size, function, cleaning_function)
        self.max_size_pred(function, initialize_data, cleaning_function, time)
        print(self.get_complexity())


class ComplexityFunctions:
    complexities = {
        'const': lambda n: 1,
        'log(n)': lambda n: log2(n),
        'n': lambda n: n,
        'nlog(n)': lambda n: n * log2(n),
        'n^2': lambda n: n ** 2,
        'n^3': lambda n: n ** 3,
        'n^4': lambda n: n ** 4,
        'n^5': lambda n: n ** 5,
        'n^6': lambda n: n ** 6,
    }

    reversed_complexities = {
        'const': lambda n: 1,
        'log(n)': lambda n: 2 ** n,
        'nlog(n)': lambda n: n / LambertW(n),
        'n': lambda n: n,
        'n^2': lambda n: sqrt(n),
        'n^3': lambda n: pow(n, 1 / 3.0),
        'n^4': lambda n: pow(n, 1 / 4.0),
        'n^5': lambda n: pow(n, 1 / 5.0),
        'n^6': lambda n: pow(n, 1 / 6.0)
    }
