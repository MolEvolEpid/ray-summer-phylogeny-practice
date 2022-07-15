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
        self.assertEqual(con_population({"N0": 1000}, 0), 1000)

    def test_con_pop_timenonzero(self):
        self.assertEqual(con_population({"N0": 1000}, 20), 1000)

    def test_lin_pop_timezero(self):
        self.assertEqual(lin_population({"N0": 1000, "b": 20}, 0), 1000)

    def test_lin_pop_timenonzero(self):
        self.assertEqual(lin_population({"N0": 1000, "b": 20}, 5), 900)

    def test_exp_pop_timezero(self):
        self.assertEqual(exp_population({"N0": 1000, "r": 0.2}, 0), 1000)

    def test_exp_pop_timenonzero(self):
        self.assertEqual(exp_population({"N0": 1000, "r": 0.2}, 5), 367.87944117144235)

class TestProbability(unittest.TestCase):

    def test_all_prob_timezero(self):
        self.assertEqual(con_probability({"N0": 1000, "k": 20}, 0), 0.19)

    def test_con_prob_timesmall(self):
        self.assertEqual(con_probability({"N0": 1000, "k": 20}, 0.123), 0.18561118307253321)

    def test_con_prob_timelarge(self):
        self.assertEqual(con_probability({"N0": 1000, "k": 20}, 123.456), 1.2349923998740305e-11)

    def test_lin_prob_timesmall(self):
        self.assertEqual(lin_probability({"N0": 1000, "k": 20, "b": 5}, 0.123), 0.1857240689796149)

    def test_lin_prob_timelarge(self):
        self.assertEqual(lin_probability({"N0": 1000, "k": 20, "b": 5}, 123.456), 7.004166250572144e-17)

    def test_exp_prob_timezero(self):
        self.assertEqual(exp_probability({"N0": 1000, "k": 20, "r": 0.1}, 0), 0.19)

    def test_exp_prob_timesmall(self):
        self.assertEqual(exp_probability({"N0": 1000, "k": 20, "r": 0.1}, 0.123), 0.1878811825975959)

    def test_exp_prob_timelarge(self):
        self.assertEqual(exp_probability({"N0": 1000, "k": 20, "r": 0.1}, 12.345), 0.006371726862993659)

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

    def test_num_segments_simple_aligned(self):
        t = TimeTree("((A:1, B:1):2, C:3);")
        self.assertEqual(len(tree_segments(t)), 2)

    def test_num_segments_complex_aligned(self):
        t = TimeTree("((((A:1.5, B:1.5):1.5, C:3):1.5, (D:1, E:1):3.5):0.5, F:5);")
        self.assertEqual(len(tree_segments(t)), 5)

    def test_num_segments_unaligned(self):
        pass # TODO Code's not ready for this yet, but I should write them

    def test_segment_bounds_simple_aligned(self):
        t = TimeTree("((A:1, B:1):2, C:3);")
        expected = [(0, 1.0, 1.0), (1.0, 3.0, 2.0)]
        self.assertEqual(tree_segments(t), expected)

    def test_segment_bounds_complex_aligned(self):
        t = TimeTree("((((A:1.5, B:1.5):1.5, C:3):1.5, (D:1, E:1):3.5):0.5, F:5);")
        expected = [(0, 1.0, 1.0), (1.0, 1.5, 0.5), (1.5, 3.0, 1.5), (3.0, 4.5, 1.5), (4.5, 5.0, 0.5)]
        self.assertEqual(tree_segments(t), expected)

    def test_segment_bounds_unaligned(self):
        pass

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

