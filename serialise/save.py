import csv

from exceptionhandling.exception_handler import ExceptionHandler, Safe
from exceptionhandling.functor import Functor

class SaveDictsAsCsv(Functor):

    def __init__(self, file, policy: ExceptionHandler = Safe()):
        super().__init__(policy)
        self.file = file

    def apply(self, input):
        if len(input) > 0:
            with open(self.file, 'w') as open_file:
                w = csv.DictWriter(open_file, input[0].keys())
                for dict in input:
                    w.writerows(dict.items())