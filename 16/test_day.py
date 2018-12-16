import pytest


from day import OpNames, behaves_like, get_num_of_opcodes_sample_behaves_like


@pytest.mark.parametrize("opname", [
    OpNames.mulr,
    OpNames.addi,
    OpNames.seti,
])
def test_behaves_like(opname):
    before = [3, 2, 1, 1]
    after = [3, 2, 2, 1]
    instruction = [9, 2, 1, 2]

    assert behaves_like(opname, instruction, before, after)


@pytest.mark.parametrize("opname", [
    OpNames.muli,
    OpNames.addr,
    OpNames.setr,
    OpNames.bani,
])
def test_not_behaves_like(opname):
    before = [3, 2, 1, 1]
    after = [3, 2, 2, 1]
    instruction = [9, 2, 1, 2]

    assert not behaves_like(opname, instruction, before, after)


def test_get_num_of_opcodes_sample_behaves_like():
    before = [3, 2, 1, 1]
    after = [3, 2, 2, 1]
    instruction = [9, 2, 1, 2]
    expected_number = 3

    result = get_num_of_opcodes_sample_behaves_like(instruction, before, after)

    assert result == expected_number
