from ortools.sat.python import cp_model
from solvers.common.grid import Grid
from solvers.constraints.column_all_different import ColumnAllDifferent
from solvers.constraints.predefined_values import PredefinedValues
from solvers.constraints.row_all_different import RowAllDifferent
from solvers.constraints.solution_converter import to_solved_grid
from solvers.constraints.solver_status import status_to_message


class FutoshikiSolver:
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
        PredefinedValues(grid_template).apply(model, solver_board)

        for expr in grid_template.get_expressions():
            left_value = solver_board[expr.left.row][expr.left.column]
            right_value = solver_board[expr.right.row][expr.right.column]
            model.Add(expr.op.eval(left_value, right_value))

        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
            return to_solved_grid(solver, solver_board)
        else:
            raise Exception(
                f"Futoshiki could not be solved. Status = {status_to_message(status)}"
            )
