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
        self.assertEqual(con_probability({"N": 1000, "k": 20, "I": 30}, 0, 0), 0.19)

    def test_con_prob_timesmall(self):
        self.assertEqual(con_probability({"N": 1000, "k": 20, "I": 30}, 0, 3), 0.10744983335291204)

    def test_con_prob_timelarge(self):
        self.assertEqual(con_probability({"N": 1000, "k": 20, "I": 30}, 0, 20), 0.004250446652671464)

    def test_lin_prob_timezero(self):
        self.assertEqual(lin_probability({"a": 5, "k": 20, "b": 3, "I": 30}, 0, 0), 0.19) # TODO wait what? Shouldn't it be 0.19? It says 2.0...

    def test_lin_prob_timesmall(self):
        self.assertEqual(lin_probability({"a": 5, "k": 20, "b": 3, "I": 30}, 0, 3), 0.004042611994059991)

    def test_lin_prob_timelarge(self):
        self.assertEqual(lin_probability({"a": 5, "k": 20, "b": 3, "I": 30}, 0, 20), 1.861372802109581e-27)

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

    def test_multihost_segment_bounds_1(self):
        t = TimeTree("((D_1:1, D_2:1):3, (R_3:2, R_4:2):2);")
        exp_coal_D = [(0.0, 1.0, 1.0), (3.0, 4.0, 1.0)] 
        exp_coal_R = [(0.0, 2.0, 2.0)]
        exp_none_D = [(1.0, 3.0, 2.0)]
        exp_none_R = [(2.0, 3.0, 1.0)]
        coal_D, coal_R, none_D, none_R = tree_segments_multihost(t, 3.0)
        self.assertEqual(exp_coal_D, coal_D)
        self.assertEqual(exp_coal_R, coal_R)
        self.assertEqual(exp_none_D, none_D)
        self.assertEqual(exp_none_R, none_R)

    def test_multihost_segment_bounds_2(self):
        t = TimeTree("((((R_4:1.5, R_5:1.5):1.5, R_6:3):1.5, (D_1:1, D_2:1):3.5):0.5, D_3:5);")
        exp_coal_D = [(0., 1., 1.), (2., 3., 1.), (3., 4.5, 1.5), (4.5, 5., 0.5)]
        exp_coal_R = [(0., 1.5, 1.5)]
        exp_none_D = [(0., 2., 2.), (1., 2., 1.)]
        exp_none_R = [(0., 2., 2.), (1.5, 2., 0.5)]
        coal_D, coal_R, none_D, none_R = tree_segments_multihost(t, 2.)
        self.assertEqual(exp_coal_D, coal_D)
        self.assertEqual(exp_coal_R, coal_R)
        self.assertEqual(exp_none_D, none_D)
        self.assertEqual(exp_none_R, none_R)

    def test_multihost_segment_bounds_3(self):
        t = TimeTree("((D_2:1, D_3:1):2, (D_1:1.5, R_4:1.5):1.5);")
        exp_coal_D = [(0., 1., 1.), (1.4, 1.5, 0.1), (1.5, 3., 1.5)] # TODO need to fix float error with .100000000000000009
        exp_coal_R = []
        exp_none_D = [(0., 1.4, 1.4), (1., 1.4, 0.4)] 
        exp_none_R = [(0., 1.4, 1.4)]
        coal_D, coal_R, none_D, none_R = tree_segments_multihost(t, 1.4)
        self.assertEqual(exp_coal_D, coal_D)
        self.assertEqual(exp_coal_R, coal_R)
        self.assertEqual(exp_none_D, none_D)
        self.assertEqual(exp_none_R, none_R)

    def test_multihost_segment_bounds_4(self):
        t = TimeTree("(((D_1:1, D_2:1):2.5, (R_3:2, R_4:2):1.5):2.5, R_5:6);")
        exp_coal_D = [(0., 1., 1.), (3., 3.5, 0.5), (3.5, 6., 2.5)]
        exp_coal_R = [(0., 2., 2.)]
        exp_none_D = [(1., 3., 2.)]
        exp_none_R = [(0., 3., 3.), (2., 3., 1.)]
        coal_D, coal_R, none_D, none_R = tree_segments_multihost(t, 3.)
        self.assertEqual(exp_coal_D, coal_D)
        self.assertEqual(exp_coal_R, coal_R)
        self.assertEqual(exp_none_D, none_D)
        self.assertEqual(exp_none_R, none_R)


class TestTreeLikelihood(unittest.TestCase):

    def test_con_likelihood_basic(self):
        # I did the calculations for this by hand and got an agreeing answer.
        t = TimeTree("((A:1, B:1):2, C:3);")
        self.assertEqual(tree_likelihood(t, con_population, con_probability, {"N0": 20}),
                -5.142852258439872)

    def test_con_likelihood_0(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertEqual(tree_likelihood(t, con_population, con_probability, {"N0": 1000}), \
                -22.450864265038337)

    def test_con_likelihood_1(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertEqual(tree_likelihood(t, con_population, con_probability, {"N0": 2000}), \
                -25.21705298727812)

    def test_con_likelihood_2(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertEqual(tree_likelihood(t, con_population, con_probability, {"N0": 10000}), \
                -31.649684637014524)

    def test_lin_likelihood_basic(self):
        # I did the calculations for this by hand and got an agreeing answer.
        t = TimeTree("((A:1, B:1):2, C:3);")
        self.assertEqual(tree_likelihood(t, lin_population, lin_probability, {"N0": 20, "b": 1}), \
                -4.944145552827423)

    def test_lin_likelihood_0(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertEqual(tree_likelihood(t, lin_population, lin_probability, {"N0": 1000, "b": 10}), \
                -22.383238808388455)

    def test_lin_likelihood_1(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertEqual(tree_likelihood(t, lin_population, lin_probability, {"N0": 2000, "b": 10}), \
                -25.18339798169222)

    def test_lin_likelihood_2(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertEqual(tree_likelihood(t, lin_population, lin_probability, {"N0": 1000, "b": 20}), \
                -22.31409139571443)


    def test_lin_failsafe(self):
        tree = TimeTree("(A:2, B:2):1;") 
        self.assertEqual(tree_likelihood(tree, lin_population, lin_probability, {"N0": 1000, "b": 1000, "k": 20}), -inf)

    def test_exp_likelihood_basic(self):
        # I did the calculations for this by hand and was off by ~0.01.
        # My first segment was off, but my second was right. This makes me think 
        # I made a simple computational error.
        t = TimeTree("((A:1, B:1):2, C:3);")
        self.assertEqual(tree_likelihood(t, exp_population, exp_probability, {"N0": 20, "r": 0.1}), \
                -4.772952580303521)

    def test_exp_likelihood_0(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertEqual(tree_likelihood(t, exp_population, exp_probability, {"N0": 1000, "r": 0.1}), \
                -21.78204636306974)

    def test_exp_likelihood_1(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertEqual(tree_likelihood(t, exp_population, exp_probability, {"N0": 2000, "r": 0.1}), \
                -24.547644036293818)

    def test_exp_likelihood_2(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertEqual(tree_likelihood(t, exp_population, exp_probability, {"N0": 1000, "r": 0.5}), \
                -19.109145638505797)

    def test_exp_failsafe(self):
        tree = TimeTree("(A:2, B:2):1;") 
        self.assertEqual(tree_likelihood(tree, exp_population, exp_probability, {"N0": 1000, "r": 4.0, "k": 20}), -inf)

if __name__ == "__main__":
    unittest.main()

