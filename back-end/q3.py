import unittest
from datetime import datetime


def _get_nums(nums):
    return ', '.join(map(lambda x: str(x), nums))


def _format_date(date):
    return  date.strftime('%Y-%m-%d')


def gt_num_filter(num, col_name):
    return '{} > {}'.format(col_name, num)


def lt_num_filter(num, col_name):
    return '{} < {}'.format(col_name, num)


def eq_num_filter(num, col_name):
    return '{} = {}'.format(col_name, num)


def in_nums_filter(nums, col_name):
    return '{} IN ({})'.format(col_name, _get_nums(nums))


def not_in_nums_filter(nums, col_name):
    return '{} NOT IN ({})'.format(col_name, _get_nums(nums))


def eq_str_filter(s, col_name):
    return '{} = \'{}\''.format(col_name, s)


def gt_date_filter(date, col_name):
    return '{} > \'{}\''.format(col_name, _format_date(date))


def lt_date_filter(date, col_name):
    return '{} < \'{}\''.format(col_name, _format_date(date))


def eq_date_filter(date, col_name):
    return '{} = \'{}\''.format(col_name, _format_date(date))


class FiltersTest(unittest.TestCase):

    def test_gt_num_filter_returns_greater_than_num(self):
        f = gt_num_filter(42, 'id')
        self.assertEqual('id > 42', f)

    def test_lt_num_filter_returns_less_than_num(self):
        f = lt_num_filter(42, 'id')
        self.assertEqual('id < 42', f)

    def test_eq_num_filter_returns_equal_to_num(self):
        f = eq_num_filter(42, 'id')
        self.assertEqual('id = 42', f)

    def test_in_nums_filter_returns_in_numbers_nums(self):
        f = in_nums_filter([1, 2, 3], 'id')
        self.assertEqual('id IN (1, 2, 3)', f)

    def test_not_in_nums_filter_returns_not_in_numbers_nums(self):
        f = not_in_nums_filter([1, 2, 3], 'id')
        self.assertEqual('id NOT IN (1, 2, 3)', f)

    def test_eq_str_filter_returns_equal_to_string(self):
        f = eq_str_filter('forty-two', 'id')
        self.assertEqual('id = \'forty-two\'', f)

    def test_gt_date_filter_returns_greater_than_date(self):
        date = datetime(1970, 1, 1)
        f = gt_date_filter(date, 'date')
        self.assertEqual('date > \'1970-01-01\'', f)

    def test_lt_date_filter_returns_less_than_date(self):
        date = datetime(1970, 1, 1)
        f = lt_date_filter(date, 'date')
        self.assertEqual('date < \'1970-01-01\'', f)

    def test_eq_date_filter_returns_equals_to_date(self):
        date = datetime(1970, 1, 1)
        f = eq_date_filter(date, 'date')
        self.assertEqual('date = \'1970-01-01\'', f)


class QueryStringBuilder():

    def __init__(self, table):
        self.table = table
        self.applied_filters = []

    def add_filter(self, f):
        self.applied_filters.append(f)
        return self

    def build(self):
        if self.applied_filters:
            return 'SELECT * FROM {} WHERE {};'.format(self.table, ' AND '.join(self.applied_filters))
        else:
            return 'SELECT * FROM {};'.format(self.table)


TABLE = 'STUDENTS'
A_FILTER = 'A < 5'
ANOTHER_FILTER = 'B = 42'
YET_ANOTHER_FILTER = 'C NOT IN (100, 200, 300)'


class QueryStringBuilderTest(unittest.TestCase):

    def setUp(self):
        self.builder = QueryStringBuilder(TABLE)

    def test_query_with_no_filters_selects_the_whole_table(self):
        query = self.builder.build()
        self.assertEqual('SELECT * FROM {};'.format(TABLE), query)

    def test_query_with_one_filter(self):
        query = self.builder.add_filter(A_FILTER).build()
        self.assertEqual('SELECT * FROM {} WHERE {};'.format(TABLE, A_FILTER), query)

    def test_query_with_more_than_one_filter(self):
        query = self.builder\
            .add_filter(A_FILTER)\
            .add_filter(ANOTHER_FILTER)\
            .add_filter(YET_ANOTHER_FILTER)\
            .build()
        self.assertEqual('SELECT * FROM {} WHERE {} AND {} AND {};'
                         .format(TABLE, A_FILTER, ANOTHER_FILTER, YET_ANOTHER_FILTER), query)

