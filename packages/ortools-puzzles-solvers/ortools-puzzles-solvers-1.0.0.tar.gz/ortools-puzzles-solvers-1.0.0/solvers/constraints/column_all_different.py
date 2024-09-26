from typing import Any, List

from solvers.constraints.puzzle_constraint import PuzzleConstraint


class ColumnAllDifferent(PuzzleConstraint):
    def apply(self, model, board: List[List[Any]]) -> None:
        for col_index in range(len(board[0])):
            rows = []
            for row_index in range(len(board)):
                rows.append(board[row_index][col_index])
            model.AddAllDifferent(rows)
