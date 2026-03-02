import sys
import os
from pathlib import Path
import importlib.util

# Set up path
src_dir = Path(__file__).parent.absolute()
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Manually load hazardous_warehouse_env from file
env_path = src_dir / "hazardous_warehouse_env.py"
spec = importlib.util.spec_from_file_location("hazardous_warehouse_env", env_path)
hazardous_warehouse_env = importlib.util.module_from_spec(spec)
sys.modules["hazardous_warehouse_env"] = hazardous_warehouse_env
spec.loader.exec_module(hazardous_warehouse_env)

# NOW import warehouse_z3_agent
from z3 import Not
from warehouse_z3_agent import build_warehouse_kb_fol, z3_entails


def query_safety(solver, loc, preds, x, y):
    """Query the safety of square (x, y).
    Returns "safe", "dangerous", or "unknown".
    """
    is_safe = z3_entails(solver, preds["Safe"](loc[(x, y)]))
    is_dangerous = z3_entails(solver, Not(preds["Safe"](loc[(x, y)])))
    if is_safe:
        return "safe"
    elif is_dangerous:
        return "dangerous"
    else:
        return "unknown"


def kb_sanity_check():
    solver, loc, preds = build_warehouse_kb_fol(width=4, height=4)

    # TELL percepts at (1,1)
    solver.add(Not(preds["Creaking"](loc[(1, 1)])))
    solver.add(Not(preds["Rumbling"](loc[(1, 1)])))

    # ASK whether (2,1) and (1,2) are safe
    status_2_1 = query_safety(solver, loc, preds, 2, 1)
    status_1_2 = query_safety(solver, loc, preds, 1, 2)

    # TELL percepts at (2,1)
    solver.add(preds["Creaking"](loc[(2, 1)]))
    solver.add(Not(preds["Rumbling"](loc[(2, 1)])))

    # ASK whether (3,1) is safe
    status_3_1 = query_safety(solver, loc, preds, 3, 1)

    # What does the solver conclude about (2,2)?
    status_2_2 = query_safety(solver, loc, preds, 2, 2)

    # TELL the solver the percepts at (1,2) (no creaking, but rumbling this time)
    solver.add(Not(preds["Creaking"](loc[(1, 2)])))
    solver.add(preds["Rumbling"](loc[(1, 2)]))

    # ASK again about (3,1) and (2,2)
    status_2_2_again = query_safety(solver, loc, preds, 2, 2)
    status_3_1_again = query_safety(solver, loc, preds, 3, 1)
    status_1_3 = query_safety(solver, loc, preds, 1, 3)

    return {
        "status_2_1": status_2_1,
        "status_1_2": status_1_2,
        "status_3_1": status_3_1,
        "status_2_2": status_2_2,
        "status_3_1_again": status_3_1_again,
        "status_2_2_again": status_2_2_again,
        "status_1_3": status_1_3,
    }


# ---------------------------------------------------------------------------
# Main — sanity check only
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Running KB sanity check...")
    check_results = kb_sanity_check()
    print("Sanity check results:")
    for key, value in check_results.items():
        print(f"  {key}: {value}")
