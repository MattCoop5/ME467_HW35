def build_warehouse_kb_fol(width=4, height=4):
    Location = DeclareSort("Location")
    Damaged_fn = Function("Damaged", Location, BoolSort())
    Forklift_fn = Function("Forklift", Location, BoolSort())
    Creaking_fn = Function("Creaking", Location, BoolSort())
    Rumbling_fn = Function("Rumbling", Location, BoolSort())
    Safe_fn = Function("Safe", Location, BoolSort())
    Adjacent_fn = Function("Adjacent", Location, Location, BoolSort())
    loc = {}
    for x in range(1, width + 1):
        for y in range(1, height + 1):
            loc[(x, y)] = Const(f"L_{x}_{y}", Location)
    solver = Solver()

    # Adjacency (closed-world)
    for x in range(1, width + 1):
        for y in range(1, height + 1):
            adj_set = set(get_adjacent(x, y, width, height))
            for x2 in range(1, width + 1):
                for y2 in range(1, height + 1):
                    if (x2, y2) in adj_set:
                        solver.add(Adjacent_fn(loc[(x, y)], loc[(x2, y2)]))
                    else:
                        solver.add(Not(Adjacent_fn(loc[(x, y)], loc[(x2, y2)])))
    # Quantified physics rules
    Lp = Const("Lp", Location)
    solver.add(
        ForAll(L, Creaking_fn(L) == Exists(Lp, And(Adjacent_fn(L, Lp), Damaged_fn(Lp))))
    )
    solver.add(
        ForAll(
            L, Rumbling_fn(L) == Exists(Lp, And(Adjacent_fn(L, Lp), Forklift_fn(Lp)))
        )
    )
    solver.add(ForAll(L, Safe_fn(L) == And(Not(Damaged_fn(L)), Not(Forklift_fn(L)))))
    # Initial knowledge
    solver.add(Safe_fn(loc[(1, 1)]))
    predicates = {
        "Creaking": Creaking_fn,
        "Rumbling": Rumbling_fn,
        "Safe": Safe_fn,
        "Damaged": Damaged_fn,
        "Forklift": Forklift_fn,
        "Adjacent": Adjacent_fn,
    }
    return solver, loc, predicates
