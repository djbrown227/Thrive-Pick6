import pulp
import math

def solve_probability_problem(num_coins, lineup_size, probabilities, max_repeating, required_lineups, min_appearances, max_appearances):
    def add_constraints(prob, heads_vars, tails_vars, counts):
        prob += pulp.lpSum([heads_vars[i] + tails_vars[i] for i in range(num_coins)]) == lineup_size
        for i in range(num_coins):
            coin = i + 1
            prob += heads_vars[i] + tails_vars[i] <= 1
            if counts[i]['H'] < min_appearances.get(coin, {}).get('H', 0):
                prob += heads_vars[i] == 1
            if counts[i]['H'] >= max_appearances.get(coin, {}).get('H', lineup_size):
                prob += heads_vars[i] == 0
            if counts[i]['T'] < min_appearances.get(coin, {}).get('T', 0):
                prob += tails_vars[i] == 1
            if counts[i]['T'] >= max_appearances.get(coin, {}).get('T', lineup_size):
                prob += tails_vars[i] == 0

    counts = [{'H': 0, 'T': 0} for _ in range(num_coins)]
    previous_lineups = []
    lineups = []

    for _ in range(required_lineups):
        prob = pulp.LpProblem("ProbabilityOptimizationProblem", pulp.LpMaximize)

        heads_vars = [pulp.LpVariable(f"heads_{i+1}", cat='Binary') for i in range(num_coins)]
        tails_vars = [pulp.LpVariable(f"tails_{i+1}", cat='Binary') for i in range(num_coins)]

        prob += pulp.lpSum([heads_vars[i] * math.log(probabilities[i]) + tails_vars[i] * math.log(1 - probabilities[i]) for i in range(num_coins)])

        # Add constraints
        add_constraints(prob, heads_vars, tails_vars, counts)

        # Ensure unique lineups
        for prev_lineup in previous_lineups:
            prob += pulp.lpSum([heads_vars[i] if (i + 1, 'H') in prev_lineup else tails_vars[i] for i in range(num_coins)]) <= lineup_size - 1

        prob.solve(pulp.PULP_CBC_CMD(msg=False))

        solution = []
        total_log_probability = 0
        for i in range(num_coins):
            if heads_vars[i].varValue == 1:
                solution.append((i + 1, 'H'))
                counts[i]['H'] += 1
                total_log_probability += math.log(probabilities[i])
            elif tails_vars[i].varValue == 1:
                solution.append((i + 1, 'T'))
                counts[i]['T'] += 1
                total_log_probability += math.log(1 - probabilities[i])

        total_probability = math.exp(total_log_probability)
        lineups.append({'lineup': solution, 'total_probability': total_probability})
        previous_lineups.append(solution)

    return lineups, counts
