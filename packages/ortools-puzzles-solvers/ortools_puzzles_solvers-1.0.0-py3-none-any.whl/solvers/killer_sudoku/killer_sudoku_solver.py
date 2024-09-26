from ortools.sat.python import cp_model
from solvers.common.grid import Grid
from solvers.constraints.column_all_different import ColumnAllDifferent
from solvers.constraints.row_all_different import RowAllDifferent
from solvers.constraints.solution_converter import to_solved_grid
from solvers.constraints.solver_status import status_to_message


class KillerSudokuSolver:
    def solve(self, grid_template: Grid) -> Grid:
        model = cp_model.CpModel()
        grid_length = grid_template.length
        solver_board = [
            [
                model.NewIntVar(1, grid_length, f"Cell({row},{col})")
                for col in range(grid_length)
            ]
            for row in range(grid_length)
        ]

        RowAllDifferent().apply(model, solver_board)
        ColumnAllDifferent().apply(model, solver_board)

        for region in grid_template.get_regions():
            constrained_cells = []
            for cell in region.cells:
                constrained_cells.append(solver_board[cell.row][cell.column])
            model.AddAllDifferent(constrained_cells)

        for sum_region in grid_template.get_sum_regions():
            constrained_cells = []
            for cell in sum_region.cells:
                constrained_cells.append(solver_board[cell.row][cell.column])
            model.AddAllDifferent(constrained_cells)
            summed_cells = sum(constrained_cells)
            model.Add(sum_region.get_sum() == summed_cells)

        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
            return to_solved_grid(solver, solver_board)
        else:
            raise Exception(
                f"Killer Sudoku could not be solved. Status = {status_to_message(status)}"
            )
