from random import randint
import complexity.aproximator

if __name__ == "__main__":

    def quicksort(arr):
        less = []
        pivotlist = []
        more = []
        if len(arr) <= 1:
            return arr
        else:
            pivot = arr[0]
            for i in arr:
                if i < pivot:
                    less.append(i)
                elif i > pivot:
                    more.append(i)
                else:
                    pivotlist.append(i)
            less = quicksort(less)
            more = quicksort(more)
            return less + pivotlist + more


    def selection_sort(lst):
        for i, e in enumerate(lst):
            mn = min(range(i, len(lst)), key=lst.__getitem__)
            lst[i], lst[mn] = lst[mn], e
        return lst


    def initialize_data(n):
        return [randint(0, 10000) for i in range(n)]


    def cleanup():
        pass


    approximator = complexity.aproximator.ComplexityAndTime(30)
    # approximator.approximation(quicksort, initialize_data, cleanup)
    approximator.all_in(quicksort, initialize_data, cleanup, 100000, 3)
