from itertools import combinations
from math import isfinite


def optimize_assignments(quotes, max_transporters):
    if not isinstance(max_transporters, int) or isinstance(max_transporters, bool):
        raise ValueError("max_transporters must be a positive integer")

    if max_transporters <= 0:
        raise ValueError("max_transporters must be a positive integer")

    if not isinstance(quotes, dict) or not quotes:
        return None

    for lane, lane_quotes in quotes.items():
        if not isinstance(lane, str) or not lane.strip():
            raise ValueError("Lane names must be non-empty strings")

        if not isinstance(lane_quotes, dict) or not lane_quotes:
            return None

        for transporter, cost in lane_quotes.items():
            if not isinstance(transporter, str) or not transporter.strip():
                raise ValueError("Transporter names must be non-empty strings")

            if (
                isinstance(cost, bool)
                or not isinstance(cost, (int, float))
                or not isfinite(cost)
                or cost < 0
            ):
                raise ValueError("Quotes must be finite, non-negative numbers")

    transporters = sorted({
        transporter
        for lane_quotes in quotes.values()
        for transporter in lane_quotes
    })

    max_group_size = min(max_transporters, len(transporters))
    best_solution = None

    for number_of_transporters in range(1, max_group_size + 1):
        for transporter_group in combinations(
            transporters,
            number_of_transporters,
        ):
            assignments = {}
            total_cost = 0

            for lane, lane_quotes in quotes.items():
                available_quotes = {
                    transporter: lane_quotes[transporter]
                    for transporter in transporter_group
                    if transporter in lane_quotes
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