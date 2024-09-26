from ortools.sat.python import cp_model


def status_to_message(status) -> str:
    if status == cp_model.INFEASIBLE:
        return "INFEASIBLE"
    elif status == cp_model.MODEL_INVALID:
        return "MODEL_INVALD"
    else:
        return "UNKNOWN"
