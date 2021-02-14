import unittest
from statsutils import *

class TestBayesian(unittest.TestCase):

    def test_1_errors(self):
        """
          Bayesian Suite 에는 반드시 likelihood() 함수가 정의되어 있어야 한다.
        :return:
        """
        class NoLikelihood(BayesSuite):
            """ """
        with self.assertRaises(NoLikelihoodError):
            suite = NoLikelihood([1,2,3])

    def test_2_diceProb(self):
        class Dice(BayesSuite):
            def likelihood(self, data, hypo):
                n_sides = hypo

                if data > n_sides:
                    return 0
                else:
                    return 1 / n_sides

        suite = Dice([4, 6, 8, 12, 20])  ## 주사위의 sides.

        for roll in [6, 8, 7, 7, 5, 4]:  ## 주사위에서 나온 눈금으로 update.
            suite.update(roll)

        self.assertDictEqual(suite.d,
                             {4: 0.0,
                              6: 0.0,
                              8: 0.9158452719690099,
                              12: 0.08040342579700499,
                              20: 0.003751302233985067})
