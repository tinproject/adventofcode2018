import pytest

from day3 import Claim, Fabric, get_canvas_square_inches_overlap


def test_get_claim_from_text():
    claim_text = "#123 @ 3,2: 5x4"
    expected_claim = Claim(claim_id=123, x=3, y=2, width=5, height=4)

    result = Claim.from_text(claim_text)

    assert result == expected_claim


@pytest.fixture()
def claims():
    return [
        Claim.from_text("#1 @ 1,3: 4x4"),
        Claim.from_text("#2 @ 3,1: 4x4"),
        Claim.from_text("#3 @ 5,5: 2x2"),
    ]


def test_get_canvas_square_inches_overlap(claims):
    expected_square_inches_overlap = 4
    fabric_canvas_size = 8

    result = get_canvas_square_inches_overlap(claims, fabric_canvas_size)

    assert result == expected_square_inches_overlap


def test_fabric_creation():
    fabric_side = 4
    expected_square_inches = fabric_side * fabric_side

    result = Fabric(fabric_side)

    assert result.fabric_side == fabric_side
    assert len(result.canvas) == expected_square_inches
    assert result.canvas.count(0) == expected_square_inches
    for element in result.canvas:
        assert element == 0


def test_fabric_get_tile_value():
    fabric_side = 4
    initial_value = 0
    fabric = Fabric(fabric_side, initial_value=initial_value)
    x = 2
    y = 2

    result = fabric.get_tile_value(x, y)

    assert result == initial_value


def test_fabric_put_claim_on_canvas():
    fabric_side = 4
    fabric = Fabric(fabric_side, initial_value=0)
    claim = Claim.from_text("#4 @ 1,1: 2x2")

    # Ensure we have an empty canvas
    assert fabric.canvas.count(0) == fabric_side * fabric_side

    fabric.put_claim_on_canvas(claim)
    result = fabric.canvas

    assert result.count(1) == claim.width * claim.height


def test_fabric_is_claim_overlaped(claims):
    overlaped_claims = [True, True, False]
    fabric_side = 8
    fabric = Fabric(fabric_side)

    for claim in claims:
        fabric.put_claim_on_canvas(claim)

    for claim, overlaped in zip(claims, overlaped_claims):
        assert fabric.is_claim_overlaped(claim) == overlaped
