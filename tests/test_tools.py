import unittest
from unittest import TestCase

# noinspection PyProtectedMember
from quasargui.tools import *


class TestFlatten(TestCase):
    def test_empty(self):
        self.assertEqual(flatten([]), [])
        self.assertEqual(flatten([[]]), [])

    def test_single_level(self):
        self.assertEqual(flatten([[1, 2]]), [1, 2])
        self.assertEqual(flatten([[1, 2], [3]]), [1, 2, 3])

    def test_multiple_levels(self):
        self.assertEqual(flatten([[[1, 2]], [3]]), [[1, 2], 3])
        self.assertEqual(flatten([[1, [2]], [[3]]]), [1, [2], [3]])

    def xtest_different_type(self):
        """
        does not work with non-lists inside, but also the typechecker shows error if uncommented
        """
        # self.assertEqual(flatten([{'a': 2}]), [{'a': 2}])


class TestMergeClasses(TestCase):
    def test_empty(self):
        self.assertEqual(merge_classes(''), '')
        self.assertEqual(merge_classes('', ''), '')
        self.assertEqual(merge_classes('', '', ''), '')

    def test_concatenation(self):
        self.assertEqual(merge_classes('a'), 'a')
        self.assertEqual(merge_classes('a bc'), 'a bc')
        self.assertEqual(merge_classes('a', 'bc'), 'a bc')
        self.assertEqual(merge_classes('a bc', 'bc'), 'a bc bc')
        self.assertEqual(merge_classes('a bc', '', 'bc'), 'a bc bc')


class TestBulidProps(TestCase):
    def test_empty(self):
        self.assertEqual(build_props({}, {}), {})
        self.assertEqual(build_props({}, {}, {}), {})

    def test_overrides_without_special(self):
        self.assertEqual(build_props(
            {
                'default_only': 1,
                'overwritten_by_props': 1,
            },
            {
                'overwritten_by_props': 2,
                'props_only': 2,
            }),
            {
                'default_only': 1,
                'overwritten_by_props': 2,
                'props_only': 2
            })

    def test_overrides_with_special(self):
        self.assertEqual(build_props(
            {
                'default_only': 1,
                'overwritten_by_props': 1,
                'overwritten_by_specials': 1,
                'overwritten_by_both': 1
            },
            {
                'overwritten_by_props': 2,
                'props_only': 2,
                'overwritten_by_both': 2,
                'prop_and_special': 2
            },
            {
                'overwritten_by_specials': 3,
                'overwritten_by_both': 3,
                'prop_and_special': 3
            }),
            {
                'default_only': 1,
                'overwritten_by_props': 2,
                'props_only': 2,
                'overwritten_by_specials': 3,
                'overwritten_by_both': 2,
                'prop_and_special': 2
            })


class TestStrBetween(TestCase):

    def test_empty_str(self):
        with self.assertRaises(ValueError):
            str_between('', '', '')
        with self.assertRaises(ValueError):
            str_between('', 'a', '')
        with self.assertRaises(ValueError):
            str_between('', '', 'b')
        with self.assertRaises(ValueError):
            str_between('what', '', '')

    def test_string_not_found(self):
        self.assertEqual(str_between('what', 'from', 'to'), '')
        self.assertEqual(str_between('from what', 'from', 'to'), ' what')
        self.assertEqual(str_between('what to', 'from', 'to'), '')

    def test_string_found(self):
        self.assertEqual(str_between('from what to', 'from', 'to'), ' what ')
        self.assertEqual(str_between('not this from what to not this', 'from', 'to'), ' what ')
        self.assertEqual(str_between('not this from what to from not this to', 'from', 'to'), ' what ')


if __name__ == '__main__':
    unittest.main()
