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


@pytest.mark.parametrize("recipes, output", [
    ("51589", 9),
    ("01245", 5),
    ("92510", 18),
    ("59414", 2018),
])
def test_find_recipes_index(recipes, output, mixer):
    result = mixer.find_recipes_index(recipes)

    assert result == output
