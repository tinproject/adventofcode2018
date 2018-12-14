import pytest


from day import ChocolateMixer


@pytest.fixture()
def mixer():
    return ChocolateMixer()


@pytest.mark.parametrize("num_recipes, output", [
    (9, "5158916779"),
    (5, "0124515891"),
    (18, "9251071085"),
    (2018, "5941429882"),
])
def test_output_after_n_iterations(num_recipes, output, mixer):

    result = mixer.get_10_recipes_after_n(num_recipes)

    assert result == output
