import pulp

def solve_value_problem(num_coins, lineup_size, probabilities, head_points, tail_points, max_repeating, required_lineups, min_appearances, max_appearances):
    counts = [{'H': 0, 'T': 0} for _ in range(num_coins)]  # Initialize count for each coin
    previous_lineups = []  # Keep track of previous lineups to ensure uniqueness
    lineups = []  # Store generated lineups

    for _ in range(required_lineups):
        prob = pulp.LpProblem("ValueOptimizationProblem", pulp.LpMaximize)
        heads_vars = [pulp.LpVariable(f"heads_{i+1}", cat='Binary') for i in range(num_coins)]
        tails_vars = [pulp.LpVariable(f"tails_{i+1}", cat='Binary') for i in range(num_coins)]

        # Objective function: maximize the expected value
        prob += pulp.lpSum([heads_vars[i] * probabilities[i] * head_points[i] + tails_vars[i] * (1 - probabilities[i]) * tail_points[i] for i in range(num_coins)])
        
        for i in range(num_coins):
            prob += heads_vars[i] + tails_vars[i] <= 1  # Each coin can be either heads or tails, not both
            
            # Adding min and max appearances constraints
            if i+1 in min_appearances:
                if 'H' in min_appearances[i+1]:
                    prob += heads_vars[i] >= min_appearances[i+1]['H']
                if 'T' in min_appearances[i+1]:
                    prob += tails_vars[i] >= min_appearances[i+1]['T']
            if i+1 in max_appearances:
                if 'H' in max_appearances[i+1]:
                    prob += heads_vars[i] <= max_appearances[i+1]['H']
                if 'T' in max_appearances[i+1]:
                    prob += tails_vars[i] <= max_appearances[i+1]['T']
        
        # Ensure unique lineups
        for prev_lineup in previous_lineups:
            prob += pulp.lpSum([heads_vars[i] if (i + 1, 'H') in prev_lineup else tails_vars[i] for i in range(num_coins)]) <= lineup_size - 1

        prob.solve(pulp.PULP_CBC_CMD(msg=False))
        
        # Extract solution and calculate total EV
        solution = []
        total_ev = 0
        for i in range(num_coins):
            if heads_vars[i].varValue == 1:
                solution.append((i + 1, 'H'))
                counts[i]['H'] += 1
                total_ev += probabilities[i] * head_points[i]
            elif tails_vars[i].varValue == 1:
                solution.append((i + 1, 'T'))
                counts[i]['T'] += 1
                total_ev += (1 - probabilities[i]) * tail_points[i]

        lineups.append({'lineup': solution, 'total_ev': total_ev})
        previous_lineups.append(solution)

    return lineups, counts
