import math
import sys


class Vec:
    """
    A simple 2D vector class for projectile motion calculations.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def magnitude(self):
        return (self.x**2 + self.y**2) ** 0.5

    def angle(self):
        return math.atan2(self.y, self.x)

    def polar(self):
        return (self.magnitude(), self.angle())


# Kinematic equations for projectile motion


def time_of_flight(v: Vec, g: float) -> float:
    return (2 * v.y) / g


def horizontal_range(v: Vec, g: float) -> float:
    return (2 * v.x * v.y) / g


def max_height(v: Vec, g: float) -> float:
    return (v.y**2) / (2 * g)


def initial_speed(v: Vec) -> float:
    return v.magnitude()


def release_angle(v: Vec) -> float:
    return math.degrees(v.angle())


# Solvers for different pairs of known parameters


def solve_from_v0_theta(v0: float, theta: float, g: float) -> Vec:
    return Vec(v0 * math.cos(math.radians(theta)), v0 * math.sin(math.radians(theta)))


def solve_from_v0_t(v0: float, t: float, g: float) -> Vec:
    vy = (g * t) / 2
    vx = math.sqrt(v0**2 - vy**2)
    return Vec(vx, vy)


def solve_from_v0_r(v0: float, r: float, g: float) -> Vec:
    vx = (r * g) / (2 * math.sqrt(v0**2 - ((r * g) / (2 * v0)) ** 2))
    vy = math.sqrt(v0**2 - vx**2)
    return Vec(vx, vy)


def solve_from_v0_h(v0: float, h: float, g: float) -> Vec:
    vy = math.sqrt(2 * g * h)
    vx = math.sqrt(v0**2 - vy**2)
    return Vec(vx, vy)


def solve_from_t_range(t: float, r: float, g: float) -> Vec:
    vx = r / t
    vy = (g * t) / 2
    return Vec(vx, vy)


def solve_from_t_height(t: float, h: float, g: float) -> Vec:
    vy = g * t / 2
    vx = math.sqrt(2 * g * h)
    return Vec(vx, vy)


def solve_from_t_theta(t: float, theta: float, g: float) -> Vec:
    theta_rad = math.radians(theta)
    vy = (g * t) / 2
    vx = vy / math.tan(theta_rad)
    return Vec(vx, vy)


def solve_from_r_height(r: float, h: float, g: float) -> Vec:
    vy = math.sqrt(2 * g * h)
    vx = r * g / (2 * vy)
    return Vec(vx, vy)


def solve_from_r_theta(r: float, theta: float, g: float) -> Vec:
    theta_rad = math.radians(theta)
    vx = math.sqrt((r * g) / (2 * math.sin(theta_rad) * math.cos(theta_rad)))
    vy = vx * math.tan(theta_rad)
    return Vec(vx, vy)


def solve_from_theta_height(theta: float, h: float, g: float) -> Vec:
    theta_rad = math.radians(theta)
    vy = math.sqrt(2 * g * h)
    vx = vy / math.tan(theta_rad)
    return Vec(vx, vy)


SOLVERS = {
    # Use of magic numbers here is intentional to map parameter pairs to solver functions
    # due to the limited scope of the example
    frozenset(("1", "2")): solve_from_v0_t,
    frozenset(("1", "3")): solve_from_v0_r,
    frozenset(("1", "4")): solve_from_v0_theta,
    frozenset(("1", "5")): solve_from_v0_h,
    frozenset(("2", "3")): solve_from_t_range,
    frozenset(("2", "4")): solve_from_t_theta,
    frozenset(("2", "5")): solve_from_t_height,
    frozenset(("3", "4")): solve_from_r_theta,
    frozenset(("3", "5")): solve_from_r_height,
    frozenset(("4", "5")): solve_from_theta_height,
}

# Main interaction function


def main():
    """
    Main function to interact with the user and compute projectile motion parameters.
    """
    while True:
        gravity = input("Enter gravitational acceleration (positive number): \n> ")
        if not gravity.replace(".", "", 1).isdigit() or float(gravity) <= 0:
            print("Please enter a valid positive number for gravity.")
            continue
        gravity = float(gravity)
        break
    VALID_PARAMS = {"1", "2", "3", "4", "5"}
    while True:
        knowns = input(
            "Enter exactly two known parameters (numbers 1–5, space-separated):\n"
            "1. Initial Speed\n"
            "2. Time of Flight\n"
            "3. Horizontal Range\n"
            "4. Release Angle (Degrees)\n"
            "5. Maximum Height\n"
            "> "
        ).split()

        if len(knowns) != 2:
            print("Please enter exactly two parameters.")
            continue

        if not all(k in VALID_PARAMS for k in knowns):
            print("Parameters must be numbers from 1 to 5.")
            continue

        if knowns[0] == knowns[1]:
            print("Please enter two different parameters.")
            continue

        knowns = frozenset(knowns)
        break

    solver = SOLVERS.get(knowns)

    if solver is None:
        raise ValueError("No solver available for the given parameter combination.")

    prompts = {
        "1": "Initial speed v0: ",
        "2": "Time of flight T: ",
        "3": "Horizontal range R: ",
        "4": "Release angle θ (degrees): ",
        "5": "Maximum height H: ",
    }

    def read_number(prompt, allow_zero_or_negative=False):
        while True:
            s = input(prompt).strip()
            try:
                x = float(s)
            except ValueError:
                print("Please enter a valid number.")
                continue
            if (not allow_zero_or_negative) and x <= 0:
                print("Please enter a positive number.")
                continue
            return x

    values = {}
    ordered_knowns = tuple(sorted(knowns))

    for k in ordered_knowns:
        # angle can be any float; the rest should be positive
        allow_any = k == "4"
        values[k] = read_number(prompts[k], allow_zero_or_negative=allow_any)

    # Call solver in the same order as the tuple key ("1","4") -> (v0, theta), etc.
    try:
        v = solver(values[ordered_knowns[0]], values[ordered_knowns[1]], gravity)
    except ValueError as e:
        print(f"Error in calculation: {e}")
        sys.exit(1)

    print("\nComputed velocity components:")
    print(f"vx = {v.x}")
    print(f"vy = {v.y}")

    print("\nDerived parameters:")
    print(f"Initial speed v0: {initial_speed(v): .4f}")
    print(f"Release angle θ (deg): {release_angle(v): .4f}")
    print(f"Time of flight T: {time_of_flight(v, gravity): .4f}")
    print(f"Horizontal range R: {horizontal_range(v, gravity): .4f}")
    print(f"Maximum height H: {max_height(v, gravity): .4f}")
    print("")


if __name__ == "__main__":
    main()
