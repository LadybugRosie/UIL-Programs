class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)


class Object:
    def __init__(self, position: Vec, velocity: Vec):
        self.position = position  # position is a Vec
        self.velocity = velocity  # velocity is a Vec

    def move(self, time):
        self.position = Vec(
            self.position.x + self.velocity.x * time,
            self.position.y + self.velocity.y * time,
        )

    def __str__(self):
        return f"Object at ({self.position.x}, {self.position.y}) with velocity ({self.velocity.x}, {self.velocity.y})"


def main():
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
            "4. Release Angle\n"
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

        break

    print(f"You selected parameters: {knowns[0]} and {knowns[1]}")


if __name__ == "__main__":
    main()
