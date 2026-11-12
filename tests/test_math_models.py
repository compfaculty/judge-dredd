import math
import pytest
from judge_dredd.math_models import bradley_terry_probability, synthetic_severity

def test_bt_equal():
    assert bradley_terry_probability(2, 2) == .5

def test_bt_complement():
    for x, y in [(0, 1), (10, -10), (-1000, 1000), (4.5, 2)]:
        assert bradley_terry_probability(x, y) + bradley_terry_probability(y, x) == pytest.approx(1)

def test_bt_one_unit():
    assert bradley_terry_probability(1, 0) == pytest.approx(math.e / (1 + math.e))

def test_bt_monotone():
    assert bradley_terry_probability(2, 0) > bradley_terry_probability(1, 0)

def test_synthetic_score():
    assert synthetic_severity(.2, .2, .1) == pytest.approx(.52)

def test_invalid_features():
    with pytest.raises(ValueError):
        synthetic_severity(1.1, 0, 0)
