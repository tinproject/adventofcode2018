from array import array
from dataclasses import dataclass
import re


FABRIC_CANVAS_SIDE = 1000


@dataclass()
class Claim:
    claim_id: int
    x: int
    y: int
    width: int
    height: int

    _claim_regex = re.compile(r"^#(?P<id>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<w>\d+)x(?P<h>\d+)$")

    @classmethod
    def from_text(cls, claim_text):
        m = cls._claim_regex.match(claim_text)
        if not m:
            raise ValueError(f"The claims seems to be not valid: '{claim_text}'")
        claim = cls(
            claim_id=int(m.group('id')),
            x=int(m.group('x')),
            y=int(m.group('y')),
            width=int(m.group('w')),
            height=int(m.group('h')),
        )
        return claim


def get_claims_from_file():
    with open('./input', 'rt') as f:
        values = [Claim.from_text(line) for line in f]
    return values


class Fabric:
    def __init__(self, fabric_side=1000, initial_value=0):
        self.fabric_side = fabric_side
        self.canvas = array('i', (initial_value for _ in range(fabric_side*fabric_side)))

    def _get_tile_index_from_coords(self, x, y):
        return x * self.fabric_side + y

    def get_tile_value(self, x, y):
        return self.canvas[self._get_tile_index_from_coords(x, y)]

    def put_claim_on_canvas(self, claim):
        for i in range(claim.x, claim.x + claim.width):
            for j in range(claim.y, claim.y + claim.height):
                self.canvas[self._get_tile_index_from_coords(i, j)] += 1

    def get_number_of_overlaped_tiles(self):
        non_used_tiles_number = self.canvas.count(0)
        used_but_non_overlaped_tiles_number = self.canvas.count(1)
        total_tiles = self.fabric_side * self.fabric_side
        return total_tiles - non_used_tiles_number - used_but_non_overlaped_tiles_number


def get_canvas_square_inches_overlap(claims, fabric_side=FABRIC_CANVAS_SIDE):
    fabric = Fabric(fabric_side)

    for claim in claims:
        fabric.put_claim_on_canvas(claim)

    return fabric.get_number_of_overlaped_tiles()


def solve():
    claims = get_claims_from_file()

    # Part 1
    overlaped_tiles = get_canvas_square_inches_overlap(claims)
    print(f"Part1 - The overlaped square inches tiles are: {overlaped_tiles}")

    # Part 2
    # common_letters = get_letters_in_common(box_ids)
    # print(f"Part2 - The letters in common are: {common_letters}")


if __name__ == "__main__":
    solve()
