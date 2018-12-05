from unittest import TestCase


def increment_dictionary_values(d, i):
    ret_d = dict(d)
    for k, v in ret_d.items():
        ret_d[k] = v + i
    return ret_d


class TestIncrementDictionaryValues(TestCase):
    def test_increment_dictionary_values(self):
        d = {'a': 1}
        dd = increment_dictionary_values(d, 1)
        ddd = increment_dictionary_values(d, -1)
        self.assertEqual(dd['a'], 2)
        self.assertEqual(ddd['a'], 0)


