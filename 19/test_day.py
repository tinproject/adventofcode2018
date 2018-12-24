import pytest


from day import Processor


@pytest.fixture()
def example_data():
    example_input = """
    #ip 0
    seti 5 0 1
    seti 6 0 2
    addi 0 1 0
    addr 1 2 3
    setr 1 0 0
    seti 8 0 4
    seti 9 0 5
    """
    return [line.strip() for line in example_input.splitlines() if line.strip()]


def test_processor(example_data):
    expected_result = 6
    processor = Processor()

    processor.load_program(example_data)
    processor.run()
    result = processor.get_register_value(0)

    assert result == expected_result
