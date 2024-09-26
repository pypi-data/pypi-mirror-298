from typing import Any, List

from solvers.constraints.puzzle_constraint import PuzzleConstraint


class RowAllDifferent(PuzzleConstraint):
    def apply(self, model, board: List[List[Any]]) -> None:
        for row_index in range(len(board)):
            model.AddAllDifferent(board[row_index])
