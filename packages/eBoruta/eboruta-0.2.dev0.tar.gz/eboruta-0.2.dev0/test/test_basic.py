from eBoruta import eBoruta
from sklearn.datasets import make_classification


def test_simplest():
    x, y = make_classification()

    selector = eBoruta()
    selector.fit(x, y)