from itertools import combinations


def optimize_assignments(quotes, max_transporters):
    lanes = list(quotes.keys())

    transporters = set()

    for lane_quotes in quotes.values():
        transporters.update(lane_quotes.keys())

    transporters = list(transporters)

    # Start with the maximum number of transporters
    # and work downward.
    for number_of_transporters in range(
        max_transporters,
        0,
        -1,
    ):

        best_solution = None

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

                if not available_quotes:
                    break

                selected_transporter = min(
                    available_quotes,
                    key=available_quotes.get,
                )

                assignments[lane] = selected_transporter
                total_cost += available_quotes[selected_transporter]

            else:
                used_transporters = set(assignments.values())

                if len(used_transporters) <= max_transporters:

                    if (
                        best_solution is None
                        or total_cost < best_solution["total_cost"]
                    ):
                        best_solution = {
                            "assignments": assignments,
                            "transporters": list(used_transporters),
                            "total_cost": total_cost,
                        }

        # If we found a valid solution using this many
        # transporters, this is the maximum feasible count.
        if best_solution is not None:
            return best_solution

    return None