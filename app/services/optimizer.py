from itertools import combinations


def optimize_assignments(quotes, max_transporters):
    if not quotes or max_transporters <= 0:
        return None

    lanes = list(quotes.keys())

    transporters = sorted({
        transporter
        for lane_quotes in quotes.values()
        for transporter in lane_quotes
    })

    max_group_size = min(max_transporters, len(transporters))
    best_solution = None

    # Examine every possible group size within the limit.
    for number_of_transporters in range(1, max_group_size + 1):
        for transporter_group in combinations(
            transporters,
            number_of_transporters,
        ):
            assignments = {}
            total_cost = 0

            for lane in lanes:
                available_quotes = {
                    transporter: quotes[lane][transporter]
                    for transporter in transporter_group
                    if transporter in quotes[lane]
                }

                # This group cannot cover every lane.
                if not available_quotes:
                    break

                selected_transporter = min(
                    available_quotes,
                    key=available_quotes.get,
                )

                assignments[lane] = selected_transporter
                total_cost += available_quotes[selected_transporter]

            else:
                used_transporters = sorted(set(assignments.values()))

                candidate = {
                    "assignments": assignments,
                    "transporters": used_transporters,
                    "total_cost": total_cost,
                }

                if (
                    best_solution is None
                    or candidate["total_cost"] < best_solution["total_cost"]
                ):
                    best_solution = candidate

    return best_solution