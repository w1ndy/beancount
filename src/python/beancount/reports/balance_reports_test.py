__author__ = "Martin Blais <blais@furius.ca>"

import unittest

from beancount.reports import balance_reports
from beancount.reports import base_test
from beancount.parser import options


class TestBalanceReports(unittest.TestCase):

    def test_all_reports_empty(self):
        # Test rendering all reports from empty liss of entries.
        entries = []
        errors = []
        options_map = options.OPTIONS_DEFAULTS.copy()

        for report_, format_ in base_test.iter_reports(balance_reports.__reports__):
            output = report_.render(entries, errors, options_map, format_)
            self.assertEqual(options.OPTIONS_DEFAULTS, options_map)
            self.assertTrue(isinstance(output, str))
