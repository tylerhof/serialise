import csv

from exceptionhandling.exception_handler import ExceptionHandler, Safe
from exceptionhandling.functor import Functor

class OpenFile(Functor):
    def __init__(self, file_path, functor_supplier, mode = 'w', policy: ExceptionHandler = Safe()):
        super().__init__(policy)
        self.file_path = file_path
        self.mode = mode
        self.functor_supplier = functor_supplier

    def apply(self, input, **kwargs):
        with open(self.file_path, self.mode) as open_file:
            self.functor_supplier(open_file)(input)

class SaveDictsAsCsv(Functor):

    def __init__(self, file, policy: ExceptionHandler = Safe()):
        super().__init__(policy)
        self.file = file

    def apply(self, input, **kwargs):
        if len(input) > 0:
            writer = csv.DictWriter(self.file, input[0].keys())
            writer.writeheader()
            for input_row in input:
                writer.writerow(input_row)
        return self.file