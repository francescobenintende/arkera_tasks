from unittest import TestCase


def largest_loss(pricesLst):
    if len(pricesLst) < 2:
        return 0

    max_price = 0
    min_val = float('inf')

    for price in pricesLst:
        min_val = min(min_val, price - max_price)
        max_price = max(max_price, price)

    return -min_val


class TestLargestLoss(TestCase):

    def test_should_return_zero_if_there_are_no_prices(self):
        pricesLst = []
        loss = largest_loss(pricesLst)
        self.assertEqual(0, loss)

    def test_should_return_zero_if_there_is_one_price(self):
        pricesLst = [42]
        loss = largest_loss(pricesLst)
        self.assertEqual(0, loss)

    def test_should_return_negative_difference_if_prices_have_one_negative_difference(self):
        pricesLst = [8, 1, 2, 3, 5]
        loss = largest_loss(pricesLst)
        self.assertEqual(7, loss)

    def test_should_return_largest_negative_difference_if_there_are_multiple_negative_differences(self):
        pricesLst = [34, 5, 8, 21, 13, 1]
        loss = largest_loss(pricesLst)
        self.assertEqual(33, loss)

    def test_should_return_smallest_negative_difference_if_prices_are_increasing(self):
        pricesLst = [1, 2, 3, 5, 8, 13, 21]
        loss = largest_loss(pricesLst)
        self.assertEqual(-1, loss)