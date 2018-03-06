# Complexity Approximator

Console app provading information about complexity of your code/algorithm.
Approximator class allows to:
* predict complexity of your code
* predict execute time of your code with given data size
* predict maximum size of data size with given timeout

### Installation:
```
>> pip install git+https://github.com/mwoss/complexity_approximator
```
### Setup:
Before running application you have to insert your code in in_class.py file.
File is composed of three function: your base code, function that initialize necessary data, and cleanup function. 
After setup stage you can pass thoes functions as arguemnts to aproximator functions.

### Example of usage:
```
approximator = complexity.aproximator.ComplexityAndTime(30)
approximator.all_in(quicksort, initialize_data, cleanup, 100000, 3)
```
