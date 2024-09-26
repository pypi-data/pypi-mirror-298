from typing import Any, List
from solvers.common.grid import Grid

from solvers.constraints.puzzle_constraint import PuzzleConstraint


class PredefinedValues(PuzzleConstraint):
    def __init__(self, grid_template: Grid) -> None:
        self.grid_template = grid_template

    def apply(self, model, board: List[List[Any]]) -> None:
        for row_index in range(len(board)):
            for column_index in range(len(board[row_index])):
                cell = self.grid_template.get_cell(row_index, column_index)
                cell_to_solve = board[row_index][column_index]
                cell_value = cell.get_value()
                if cell_value is not None:
                    model.Add(cell_to_solve == cell_value)
