# matrix.py

from diffexp import DiffExp

class Matrix:
    """Collections of differential expression objects
    Arg:
        diff_exp_filename: One differential expresssion matrix filename
    Attribute:
        expression(list): A list of DiffExp objects
    Method:
        __iter__: Return iterator of the diff_exp input
    """

    def __init__(self, diff_exp_filename):
        self.diff_exp_filename = diff_exp_filename
        with open(diff_exp_filename) as diff_exp_file:
            self.expressions = [DiffExp(info) for info in diff_exp_file]

    def __repr__(self):
        return f"Matrix({self.diff_exp_filename})"

    def __iter__(self):
        """Return iterator of the diff_exp input"""

        return iter(self.expressions)
