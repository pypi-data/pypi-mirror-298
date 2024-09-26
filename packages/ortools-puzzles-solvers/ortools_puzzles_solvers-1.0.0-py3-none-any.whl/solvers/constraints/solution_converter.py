from solvers.common.grid import Grid


def to_solved_grid(solver, solved_board) -> Grid:
    grid_length = len(solved_board)
    grid = Grid(grid_length)
    for row_index in range(grid_length):
        for column_index in range(grid_length):
            solved_cell_value = solver.Value(solved_board[row_index][column_index])
            cell = grid.get_cell(row_index, column_index)
            cell.set_value(solved_cell_value)
    return grid
