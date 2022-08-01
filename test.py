import unittest
from tree_likelihood import *
from population_models import *
from numpy import inf
from time_tree import *

#
# population_models.py
#

class TestPopulation(unittest.TestCase):

    def test_con_pop_timezero(self):
        self.assertEqual(con_population({"N": 1000, "I": 30}, 30), 1000)

    def test_con_pop_timenonzero(self):
        self.assertEqual(con_population({"N": 1000, "I": 30}, 10), 1000)

    def test_lin_pop_timezero(self):
        self.assertEqual(lin_population({"a": 5, "b": 3, "I": 30}, 30), 5)

    def test_lin_pop_timenonzero(self):
        self.assertEqual(lin_population({"a": 5, "b": 3, "I": 30}, 10), 65)


class TestProbability(unittest.TestCase):

    def test_con_prob_timezero(self):
        self.assertAlmostEqual(con_probability({"N": 1000, "k": 20, "I": 30}, 0, 0), 0.19)

    def test_con_prob_timesmall(self):
        self.assertAlmostEqual(con_probability({"N": 1000, "k": 20, "I": 30}, 0, 3), 0.1074498)

    def test_con_prob_timelarge(self):
        self.assertAlmostEqual(con_probability({"N": 1000, "k": 20, "I": 30}, 0, 20), 0.0042504)

    def test_lin_prob_timezero(self):
        self.assertAlmostEqual(lin_probability({"a": 5, "k": 20, "b": 3, "I": 30}, 0, 0), 0.19) # TODO wait what? Shouldn't it be 0.19? It says 2.0...

    def test_lin_prob_timesmall(self):
        self.assertAlmostEqual(lin_probability({"a": 5, "k": 20, "b": 3, "I": 30}, 0, 3), 0.0040426)

    def test_lin_prob_timelarge(self):
        self.assertAlmostEqual(lin_probability({"a": 5, "k": 20, "b": 3, "I": 30}, 0, 20), 1.8613728e-27)

#
# time_tree.py
#

class TestTimeTree(unittest.TestCase):

    def test_has_times(self):
        t = TimeTree("((A:1, B:1):1, C:2);")
        self.assertTrue(all([hasattr(n, "time") for n in t.traverse()]))

    def test_leaf_times(self):
        t = TimeTree("((A:1, B:1):1, C:2);")
        self.assertTrue(all([n.time == 0 for n in t.iter_leaves()]))

    # TODO I have not tested anything having to do with hosts.

#
# tree_likelihood.py
#

class TestTreeSegments(unittest.TestCase):

    def test_num_segments_1(self):
        t = TimeTree("((A:1, A:1):2, A:3);")
        self.assertEqual(len(tree_segments(t)), 2)

    def test_num_segments_2(self):
        t = TimeTree("((((A:1.5, A:1.5):1.5, A:3):1.5, (A:1, A:1):3.5):0.5, A:5);")
        self.assertEqual(len(tree_segments(t)), 5)

    def test_multihost_num_segments_1(self):
        pass # TODO I need to write tests for the multihost stuff.

    def test_multihost_num_segments_2(self):
        pass

    def test_segment_bounds_1(self):
        t = TimeTree("((A:1, A:1):2, A:3);")
        expected = [(0, 1.0, 1.0), (1.0, 3.0, 2.0)]
        self.assertEqual(tree_segments(t), expected)

    def test_segment_bounds_1(self):
        t = TimeTree("((((A:1.5, A:1.5):1.5, A:3):1.5, (A:1, A:1):3.5):0.5, A:5);")
        expected = [(0, 1.0, 1.0), (1.0, 1.5, 0.5), (1.5, 3.0, 1.5), (3.0, 4.5, 1.5), (4.5, 5.0, 0.5)]
        self.assertEqual(tree_segments(t), expected)

    def assertListsAlmostEqual(self, expected, actual):
        message = "Lists {2} and {3} did not match"
        for exp_lst, act_lst in zip(expected, actual):
            for exp_tup, act_tup in zip(exp_lst, act_lst):
                for exp_n, act_n in zip(exp_tup, act_tup):
                    self.assertEqual(round(exp_n, 7), round(act_n, 7), message.format(str(act_n), str(exp_n), str(act_lst), str(exp_lst)))

    def test_multihost_segment_bounds_1(self):
        t = TimeTree("((D_1:1, D_2:1):3, (R_3:2, R_4:2):2);")
        t.populate_hosts({"D": 0, "R": 1})
        exp_coal_D = [(0.0, 1.0, 1.0), (3.0, 4.0, 1.0)] 
        exp_coal_R = [(0.0, 2.0, 2.0)]
        exp_none_D = [(1.0, 3.0, 2.0)]
        exp_none_R = [(2.0, 3.0, 1.0)]
        actual = tree_segments_multihost(t, 3.)
        self.assertListsAlmostEqual([exp_coal_D, exp_coal_R, exp_none_D, exp_none_R], actual)

    def test_multihost_segment_bounds_2(self):
        t = TimeTree("((((R_4:1.5, R_5:1.5):1.5, R_6:3):1.5, (D_1:1, D_2:1):3.5):0.5, D_3:5);")
        t.populate_hosts({"D": 0, "R": 1})
        exp_coal_D = [(0., 1., 1.), (2., 3., 1.), (3., 4.5, 1.5), (4.5, 5., 0.5)]
        exp_coal_R = [(0., 1.5, 1.5)]
        exp_none_D = [(0., 2., 2.), (1., 2., 1.)]
        exp_none_R = [(0., 2., 2.), (1.5, 2., 0.5)]
        actual = tree_segments_multihost(t, 2.)
        self.assertListsAlmostEqual([exp_coal_D, exp_coal_R, exp_none_D, exp_none_R], actual)

    def test_multihost_segment_bounds_3(self):
        t = TimeTree("((D_2:1, D_3:1):2, (D_1:1.5, R_4:1.5):1.5);")
        t.populate_hosts({"D": 0, "R": 1})
        exp_coal_D = [(0, 1, 1), (1.4, 1.5, 0.1), (1.5, 3, 1.5)]
        exp_coal_R = []
        exp_none_D = [(0, 1.4, 1.4), (1, 1.4, 0.4)]
        exp_none_R = [(0, 1.4, 1.4)]
        actual = tree_segments_multihost(t, 1.4)
        self.assertListsAlmostEqual([exp_coal_D, exp_coal_R, exp_none_D, exp_none_R], actual)

    def test_multihost_segment_bounds_4(self):
        t = TimeTree("(((D_1:1, D_2:1):2.5, (R_3:2, R_4:2):1.5):2.5, R_5:6);")
        t.populate_hosts({"D": 0, "R": 1})
        exp_coal_D = [(0., 1., 1.), (3., 3.5, 0.5), (3.5, 6., 2.5)]
        exp_coal_R = [(0., 2., 2.)]
        exp_none_D = [(1., 3., 2.)]
        exp_none_R = [(0., 3., 3.), (2., 3., 1.)]
        actual = tree_segments_multihost(t, 3.)
        self.assertListsAlmostEqual([exp_coal_D, exp_coal_R, exp_none_D, exp_none_R], actual)


class TestTreeLikelihood(unittest.TestCase):

    def test_con_likelihood_basic(self):
        # I did the calculations for this by hand and got an agreeing answer.
        t = TimeTree("((A:1, B:1):2, C:3);")
        self.assertAlmostEqual(tree_likelihood(t, con_population, con_probability, {"N": 20, "I": 5}),
                -5.1428523)

    def test_con_likelihood_0(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertAlmostEqual(tree_likelihood(t, con_population, con_probability, {"N": 1000, "I": 5}), \
                -22.4508643)

    def test_con_likelihood_1(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertAlmostEqual(tree_likelihood(t, con_population, con_probability, {"N": 2000, "I": 5}), \
                -25.2170530)

    def test_con_likelihood_2(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertAlmostEqual(tree_likelihood(t, con_population, con_probability, {"N": 10000, "I": 5}), \
                -31.6496846)

    def test_lin_likelihood_basic(self):
        # I did the calculations for this by hand and got an agreeing answer.
        t = TimeTree("((A:1, B:1):2, C:3);")
        self.assertAlmostEqual(tree_likelihood(t, lin_population, lin_probability, {"a": 5, "b": 1, "I": 6}), \
                -3.7924884)

    def test_lin_likelihood_0(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertAlmostEqual(tree_likelihood(t, lin_population, lin_probability, {"a": 5, "b": 10, "I": 6}), \
                -10.4679727)

    def test_lin_likelihood_1(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertAlmostEqual(tree_likelihood(t, lin_population, lin_probability, {"a": 5, "b": 20, "I": 6}), \
                -12.9087445)

    def test_lin_likelihood_2(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertAlmostEqual(tree_likelihood(t, lin_population, lin_probability, {"a": 5, "b": 30, "I": 6}), \
                -14.4146358)


if __name__ == "__main__":
    unittest.main()

