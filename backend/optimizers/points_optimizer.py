import pulp

def solve_points_problem(num_coins, lineup_size, head_points, tail_points, max_repeating, required_lineups, min_appearances, max_appearances):
    counts = [{'H': 0, 'T': 0} for _ in range(num_coins)]
    previous_lineups = []
    lineups = []

    for _ in range(required_lineups):
        prob = pulp.LpProblem("PointsOptimizationProblem", pulp.LpMaximize)
        
        heads_vars = [pulp.LpVariable(f"heads_{i+1}", cat='Binary') for i in range(num_coins)]
        tails_vars = [pulp.LpVariable(f"tails_{i+1}", cat='Binary') for i in range(num_coins)]

        prob += pulp.lpSum([heads_vars[i] * head_points[i] + tails_vars[i] * tail_points[i] for i in range(num_coins)])

        for i in range(num_coins):
            prob += heads_vars[i] + tails_vars[i] <= 1
            # Adding min and max appearances constraints
            if i+1 in min_appearances:
                prob += heads_vars[i] >= min_appearances[i+1].get('H', 0)
                prob += tails_vars[i] >= min_appearances[i+1].get('T', 0)
            if i+1 in max_appearances:
                prob += heads_vars[i] <= max_appearances[i+1].get('H', 1)
                prob += tails_vars[i] <= max_appearances[i+1].get('T', 1)

        for prev_lineup in previous_lineups:
            prob += pulp.lpSum([heads_vars[i] if (i + 1, 'H') in prev_lineup else tails_vars[i] for i in range(num_coins)]) <= lineup_size - 1

        prob.solve(pulp.PULP_CBC_CMD(msg=False))

        solution = []
        total_points = 0
        for i in range(num_coins):
            if heads_vars[i].varValue == 1:
                solution.append((i + 1, 'H'))
                counts[i]['H'] += 1
                total_points += head_points[i]
            elif tails_vars[i].varValue == 1:
                solution.append((i + 1, 'T'))
                counts[i]['T'] += 1
                total_points += tail_points[i]

        lineups.append({'lineup': solution, 'total_points': total_points})
        previous_lineups.append(solution)

    return lineups, counts
