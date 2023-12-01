import re
from os.path import join

class CachedProperty():
    def __init__(self, func, name=None):
        self.func = func
        self.name = name if name is not None else func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, instance, class_):
        if instance is None:
            return self
        res = self.func(instance)
        setattr(instance, self.name, res)
        return res


class CalibrationValue():
    __digit_pattern = re.compile('\d')

    def __init__(self, string: str):
        self.__original_string = string
    
    @property
    def pattern(self):
        return self.__digit_pattern

    @CachedProperty
    def cleaned(self):
        return self.__original_string.strip('\n')
    
    def __two_digits(self) -> tuple[str, str]:
        matches = self.__digit_pattern.findall(self.cleaned)
        try:
            return matches[0], matches[-1]
        except IndexError:
            return ()

    def __combine_digits(self, first: str, last: str) -> int:
        return int('{}{}'.format(first, last))

    def process_string(self) -> int:
        first, second = self.__two_digits()
        return self.__combine_digits(first=first, last=second)


folder_name = 'day_1'

def get_number_list(file_name: str, verbose:str=False):
    numbers = []
    with open(join(folder_name, file_name)) as f:
        for line in f:
            value = CalibrationValue(line)
            numbers.append(value.process_string())
            if verbose:
                print('{:<47} -> {:>2}'.format(value.cleaned, numbers[-1]))
    return numbers

if __name__ == '__main__':
    print("Running the example:")
    print("Here are the strings with their conversion to numbers:")
    l = get_number_list('input_1_example.txt', verbose=True)
    print("And the sum is {}".format(sum(l)))

    print("Now reading and processing the full file. . .")
    l = get_number_list('input_1.txt', verbose=False)
    print("And obtaining the sum {}".format(sum(l)))