"""Report classes for all reports that display ending balances of accounts.
"""
__author__ = "Martin Blais <blais@furius.ca>"

import re

from beancount.reports import base
from beancount.reports import tree_table
from beancount.core import realization


class BalancesReport(base.HTMLReport,
                     metaclass=base.RealizationMeta):
    """Print out the trial balance of accounts matching an expression."""

    names = ['balances', 'bal', 'trial']
    default_format = 'text'

    @classmethod
    def add_args(cls, parser):
        parser.add_argument('-e', '--filter-expression', '--expression', '--regexp',
                            action='store', default=None,
                            help="Filter expression for which account balances to display.")

        parser.add_argument('-c', '--at-cost', '--cost', action='store_true',
                            help="Render values at cost, convert the units to cost value")

    def render_real_text(self, real_root, options_map, file):
        if self.args.filter_expression:
            regexp = re.compile(self.args.filter_expression)
            real_root = realization.filter(
                real_root,
                lambda real_account: regexp.search(real_account.account))
        if real_root:
            realization.dump_balances(real_root,
                                      self.args.at_cost, True, file=file)

    def render_real_htmldiv(self, real_root, options_map, file):
        text = tree_table.table_of_balances(real_root,
                                            options_map['operating_currency'],
                                            self.formatter,
                                            classes=['trial'])

        balance_cost = realization.compute_balance(real_root).cost()
        if not balance_cost.is_empty():
            text += """
              Total Balance: <span class="num">{}</span>
            """.format(balance_cost)

        file.write(text)


class BalanceSheetReport(base.HTMLReport,
                         metaclass=base.RealizationMeta):
    """Print out a balance sheet."""

    names = ['balsheet']
    default_format = 'html'

    def render_real_htmldiv(self, real_root, options_map, file):
        operating_currencies = options_map['operating_currency']
        assets = tree_table.table_of_balances(
            realization.get(real_root, options_map['name_assets']),
            operating_currencies,
            self.formatter)
        liabilities = tree_table.table_of_balances(
            realization.get(real_root, options_map['name_liabilities']),
            operating_currencies,
            self.formatter)
        equity = tree_table.table_of_balances(
            realization.get(real_root, options_map['name_equity']),
            operating_currencies,
            self.formatter)

        file.write("""
               <div class="halfleft">

                 <div id="assets">
                  <h3>Assets</h3>
                  {assets}
                 </div>

               </div>
               <div class="halfright">

                 <div id="liabilities">
                  <h3>Liabilities</h3>
                  {liabilities}
                 </div>
                 <div class="spacer">
                 </div>
                 <div id="equity">
                  <h3>Equity</h3>
                  {equity}
                 </div>

               </div>
            """.format(**locals()))


class IncomeStatementReport(base.HTMLReport,
                            metaclass=base.RealizationMeta):
    """Print out an income statement."""

    names = ['income']
    default_format = 'html'

    def render_real_htmldiv(self, real_root, options_map, file):
        # Render the income statement tables.
        operating_currencies = options_map['operating_currency']
        income = tree_table.table_of_balances(
            realization.get(real_root, options_map['name_income']),
            operating_currencies,
            self.formatter)
        expenses = tree_table.table_of_balances(
            realization.get(real_root, options_map['name_expenses']),
            operating_currencies,
            self.formatter)

        file.write("""
           <div id="income" class="halfleft">

             <div id="income">
              <h3>Income</h3>
              {income}
             </div>

           </div>
           <div class="halfright">

             <div id="expenses">
              <h3>Expenses</h3>
              {expenses}
             </div>

           </div>
        """.format(**locals()))


__reports__ = [
    BalancesReport,
    BalanceSheetReport,
    IncomeStatementReport,
    ]
