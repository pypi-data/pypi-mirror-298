from typing import List
from solvers.common.cell import Cell
from solvers.common.expr import Expression
from solvers.common.less_than_op import LessThanOp
from solvers.common.region import Region
from solvers.common.sum_region import SumRegion


class Grid:
    def __init__(self, length: int) -> None:
        self.length = length
        self.rows: List[List[Cell]] = []
        self.columns: List[List[Cell]] = []
        self.regions: List[Region] = []
        self.sum_regions: List[SumRegion] = []
        self.expressions: List[Expression] = []
        self.__init_with_empty_cells()

    def __init_with_empty_cells(self):
        for row in range(self.length):
            new_row = []
            self.rows.append(new_row)
            for column in range(self.length):
                cell = Cell(row, column)
                new_row.append(cell)
        for column in range(self.length):
            new_column = []
            self.columns.append(new_column)
            for row in range(self.length):
                new_column.append(self.rows[row][column])

    def get_cell(self, row: int, column: int) -> Cell:
        return self.rows[row][column]

    def set_cell_value(self, row: int, column: int, value: int) -> None:
        self.get_cell(row, column).set_value(value)

    def get_rows(self) -> List[List[Cell]]:
        return self.rows

    def get_regions(self) -> List[Region]:
        return self.regions

    def get_sum_regions(self) -> List[SumRegion]:
        return self.sum_regions

    def create_region(self):
        region = Region()
        self.regions.append(region)
        return region

    def create_sum_region(self, sum: int):
        region = SumRegion(sum)
        self.sum_regions.append(region)
        return region

    def add_less_than_expr(self, left: Cell, right: Cell) -> None:
        self.expressions.append(Expression(left, right, LessThanOp()))

    def get_expressions(self) -> List[Expression]:
        return self.expressions
