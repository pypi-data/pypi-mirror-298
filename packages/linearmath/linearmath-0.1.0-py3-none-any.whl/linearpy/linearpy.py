"""Custom Exceptions"""

class CanNotMultiplyException(Exception):
    pass


class InverseDoesNotExistException(Exception):
    pass


class DeterminantDoesNotExist(Exception):
    pass


class MatrixOrder:
    def __init__(self, rows: int, columns: int) -> None:
        self.rows = rows
        self.columns = columns

    def __str__(self) -> str:
        return f"{self.columns} by {self.rows}"

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, type(self)):
            raise ValueError(f" {type(self)} with {type(value)} is not supported")

        return self.columns == value.columns and self.rows == value.rows


class Matrix:
    """ """

    def __init__(self, matrix: list[list[float | int]]) -> None:
        # you should validate the matrix first
        self.matrix = matrix
        num_rows = len(self.matrix)
        num_columns = len(self.matrix[0])
        self.order = MatrixOrder(rows=num_rows, columns=num_columns)

    @property
    def rows(self):
        return self.order.rows

    @property
    def columns(self):
        return self.order.columns

    @property
    def matrix(self):
        return self._matrix


    @matrix.setter
    def matrix(self, value: list[list]):
        if isinstance(value, list):
            self._check_rows(value)
            for row in value:
                self._check_matrix_entries(row)

            # set value to matrix at this point
            self._matrix = value
        else:
            raise ValueError("you should pass a list of lists")

    @property
    def main_entries(self) -> list | None:
        """return main entries in a square matrix, return None if matrix is not square"""
        if not self.is_squar():
            return None

        main_entries = []

        for i in range(self.rows):  # it doesn't matter rows or columns
            main_entries.append(self.matrix[i][i])

        return main_entries

    def transpose(self):
        """Transpose a matrix and return new Matrix instance"""
        transpose_matrix = self._get_skeleton_matrix()

        for i in range(self.rows):
            for j in range(self.columns):
                # Transpose the matrix
                transpose_matrix[j].append(self.matrix[i][j])

        return Matrix(matrix=transpose_matrix)


    def determinant(self):
        """Calculate the determinant of the matrix"""
        if not self.is_squar():
            raise DeterminantDoesNotExist

        # Two by two matrix
        if self.order.rows == 2:
            # return det
            return (self.matrix[0][0] * self.matrix[1][1]) - (self.matrix[0][1] * self.matrix[1][0])

        factors = self.get_determinant_factors()
        determinant = 0
        for factor_index in range(len(factors)):
            # exlcude entries from the first row and from the column with index factor_index
            submatrix_skeleton = self._get_submatrix_skeleton()
            for i in range(self.rows):
                for j in range(self.columns):
                    if i != 0 and j != factor_index:
                        submatrix_skeleton[i - 1].append(self.matrix[i][j])


            submatrix = Matrix(submatrix_skeleton)
            determinant += factors[factor_index] * submatrix.determinant()

        return determinant



    def _get_submatrix_skeleton(self) -> list:
        """returns a matrix without the row and column given"""
        submatrix = []
        for i in range(self.rows - 1):
            submatrix.append([])

        return submatrix



    def get_determinant_factors(self):
        """
        Return entries of the first row,
        TODO: choose the row with most zeros later
        """

        factors = []
        for i in range(self.columns):
            if i % 2 == 0:
                factors.append(self.matrix[0][i])
            else:
                factors.append(-self.matrix[0][i])

        return factors



    def inverse(self):
        """find the inverse of the matrix , if it doesn't exist raise InverseDoesNotExistException"""
        factor = 1/8



    def is_squar(self) -> bool:
        """True when rows equals columns, False otherwise"""
        if self.columns == self.rows:
            return True

        return False

    def is_diagonal(self) -> bool:
        """True when all entries except main_entries are zero"""

        # only square matrix can be diagnoal
        if not self.is_squar():
            return False

        for i in range(self.rows):
            for j in range(self.columns):
                if i != j:
                    if self.matrix[i][j] != 0:
                        return False

        return True

    def is_symetric(self) -> bool:
        return self.transpose() == self

    def _check_rows(self, matrix: list) -> None:
        for row in matrix:
            if not isinstance(row, list):
                raise ValueError("matrix rows must be list")

    def _check_matrix_entries(self, row: list[int | float]):
        for entry in row:
            if not isinstance(entry, int | float):
                raise ValueError(
                    f"matrix entries must be int or float, found {type(entry)}!"
                )

    def __str__(self) -> str:
        string_repr = "\n"
        for row in self.matrix:
            string_repr += f" {row} \n".replace(",", " ")

        string_repr += "\n"
        return string_repr

    def __eq__(self, value) -> bool:
        if not isinstance(value, type(self)):
            raise ValueError(f"equality with '{type(value)}' is not supported")

        if not self.order == value.order:
            # Matricies with different order are not equal
            return False

        for i in range(self.order.rows):
            for j in range(self.order.columns):
                if self.matrix[i][j] != value.matrix[i][j]:
                    return False

        return True

    def __sum__(self, value):
        print("solo is summing matricies!")
        return

    def __mul__(self, value):
        """Perform matrix multiplication

        Args:
            value (Matrix): the matrix to be multiplied with

        exceptions:
            CanNotMultiplyException: when matrix multiplication cannot be performed  ( rows not equal columns)
        """

        # Check if matrix can be multiplied
        if not self._can_multiply(value):
            raise CanNotMultiplyException

        # Perform multiplication
        a = self.matrix  # For readability
        result = self._get_mul_result_matrix(value)
        for i in range(self.rows):
            row = Matrix([a[i]])
            for j in range(value.columns):
                column = Matrix(self._get_column(value, j))
                result[i][j] = row_by_column(row, column)

        return Matrix(result)

    def _get_column(self, matrix, index):
        """Return the column specified by index"""
        column = []
        for i in range(matrix.rows):
            column.append([matrix.matrix[i][index]])

        return column

    def _get_mul_result_matrix(self, value):
        """Return empty matrix with rows = self.order.rows and columns = value.order.columns"""

        matrix = []
        for i in range(self.order.rows):
            matrix.append([])
            for j in range(value.order.columns):
                matrix[i].append(0)

        return matrix

    def _can_multiply(self, value):
        """Check if value can be multipled with self.

        Args:
            value (_type_): _description_
        """
        return self.order.columns == value.order.rows

    def _mul_const(self, constant: int | float):
        """multiply matrix with constant 'c * matrix'"""
        new_matrix = self._get_skeleton_matrix()

        for i in range(self.rows):
            for j in range(self.order.columns):
                # Multiply each entry with constant
                new_matrix[i][j] = constant * self.matrix[i][j]

        return new_matrix

    def _get_skeleton_matrix(self):
        """return an empty matrix containing the same number of columns as the self.matrix"""

        skeleton_matrix = []
        for i in range(self.order.columns):
            skeleton_matrix.append([])

        return skeleton_matrix

    @classmethod
    def const_multiply(cls, constant, matrix):
        """Multiply a constant by a matrix , order matter, (constant * matrix) not (matrix * constant)"""
        new_matrix = cls._get_skeleton_matrix(matrix)

        for i in range(matrix.order.rows):
            for j in range(matrix.order.columns):
                # Multiply each entry with constant
                new_matrix[i].append(constant * matrix.matrix[i][j])

        return Matrix(new_matrix)


def row_by_column(row: Matrix, vector: Matrix):
    """
    multiply a row vector by a  column vector. the result is a single number

    Args:
        row (Matrix): _description_
        vector (Matrix): _description_
    """
    result = 0
    for i in range(row.columns):
        result += row.matrix[0][i] * vector.matrix[i][0]

    return result


def column_by_row(column: Matrix, row: Matrix):
    """TODO: Multiply a column by a row vector, return a full size matrix"""

