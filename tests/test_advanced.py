# -*- coding: utf-8 -*-

import pytest
import satellite


# Parameterized testing. Change the test cases to generate more.

@pytest.mark.parametrize("test_input_a, test_input_b, expected", [
    (3, 5, 8),
    (2, 4, 6),
    (5, 5, 10),
])
def test_adder(test_input_a, test_input_b, expected):
    assert satellite.core.add_two_things(test_input_a, test_input_b) == expected
