import unittest

#
# population_models.py
#
from population_models import *

class TestPopulation(unittest.TestCase):
    
    def test_con_zero(self):
        self.assertEqual(con_population({"N0": 1000}, 0), 1000)

    def test_con_nonzero(self):
        self.assertEqual(con_population({"N0": 1000}, 20), 1000)

    def test_lin_zero(self):
        self.assertEqual(lin_population({"N0": 1000, "b": 20}, 0), 1000)

    def test_lin_nonzero(self):
        self.assertEqual(lin_population({"N0": 1000, "b": 20}, 5), 900)

    def test_exp_zero(self):
        self.assertEqual(exp_population({"N0": 1000, "r": 0.2}, 0), 1000)

    def test_con_zero(self):
        self.assertEqual(exp_population({"N0": 1000, "r": 0.2}, 5), 368)

class TestProbability(unittest.TestCase):

    def test_con_zero(self):
        self.assertEqual(con_probability({"N0": 1000, "k": 20}, 0), 0.19)

    def test_con_small(self):
        self.assertEqual(con_probability({"N0": 1000, "k": 20}, 0.123), 0.18561118307253321)

    def test_con_large(self):
        self.assertEqual(con_probability({"N0": 1000, "k": 20}, 123.456), 1.2349923998740305e-11)

    def test_lin_zero(self):
        self.assertEqual(lin_probability({"N0": 1000, "k": 20, "b": 5}, 0), 0.19)

    def test_lin_small(self):
        self.assertEqual(lin_probability({"N0": 1000, "k": 20, "b": 5}, 0.123), 0.1857240689796149)

    def test_lin_large(self):
        self.assertEqual(lin_probability({"N0": 1000, "k": 20, "b": 5}, 123.456), 7.004166250572144e-17)

    def test_exp_zero(self):
        self.assertEqual(exp_probability({"N0": 1000, "k": 20, "r": 0.1}, 0), 0.19)

    def test_exp_small(self):
        self.assertEqual(exp_probability({"N0": 1000, "k": 20, "r": 0.1}, 0.123), 0.1878811825975959)

    def test_exp_large(self):
        self.assertEqual(exp_probability({"N0": 1000, "k": 20, "r": 0.1}, 12.345), 0.006371726862993659)

#
# time_tree.py
#
from time_tree import *

class TestTimeTree(unittest.TestCase):

    def test_has_times(self):
        t = TimeTree("((A:1, B:1):1, C:2);")
        self.assertTrue(all([hasattr(n, "time") for n in t.traverse()]))

    def test_leaf_times(self):
        t = TimeTree("((A:1, B:1):1, C:2);")
        self.assertTrue(all([n.time == 0 for n in t.iter_leaves()]))

    # TODO: I have not tested anything having to do with hosts.

#
# tree_likelihood.py
#
from tree_likelihood import *

class TestTreeBoundaries(unittest.TestCase):

    def test_within_tolerance(self):
        self.assertTrue(within_tolerance(0.1, 0.1003), "0.003 difference should be within tolerance")

    def test_outside_tolerance(self):
        self.assertFalse(within_tolerance(0.1, 0.2), "0.1 difference should not be within tolerance")
    
    def test_closest_parent_simple(self):
        t = TimeTree("((A:1, B:1):1, C:2);")
        p = t.get_common_ancestor(t&"A", t&"C")
        self.assertEqual(closest_parent_node(t, 1), p, "Common ancestor did not match")

    def test_closest_parent_complex(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        p = t.get_common_ancestor(t&"C", t&"E")
        self.assertEqual(closest_parent_node(t, 1), p, "Common ancestor did not match")

    def test_sampling_groups_one(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertEqual(len(sampling_groups(t)), 1, "There should only be one sampling group")

    def test_sampling_groups_multi(self):
        t = TimeTree("((A:2, B:2):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertEqual(len(sampling_groups(t)), 2, "There should be two sampling groups")

    def test_count_lineages_0(self):
        t = TimeTree("(((A:1, B:1):3, C:5):2, (D:2, E:3):3);")
        self.assertEqual(count_lineages(t, 0), 1)
    
    def test_count_lineages_1(self):
        t = TimeTree("(((A:1, B:1):3, C:5):2, (D:2, E:3):3);")
        self.assertEqual(count_lineages(t, 1), 3)
    
    def test_count_lineages_2(self):
        t = TimeTree("(((A:1, B:1):3, C:5):2, (D:2, E:3):3);")
        self.assertEqual(count_lineages(t, 5), 2)
    
    def test_count_lineages_3(self):
        t = TimeTree("(((A:1, B:1):3, C:5):2, (D:2, E:3):3);")
        self.assertEqual(count_lineages(t, 6), 2)
    
    def test_count_lineages_4(self):
        t = TimeTree("(((A:1, B:1):3, C:5):2, (D:2, E:3):3);")
        self.assertEqual(count_lineages(t, 7), 0)

class TestTreeLikelihood(unittest.TestCase):

    def test_con_likelihood_basic(self):
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
        t = TimeTree("((A:1, B:1):2, C:3);")
        self.assertEqual(tree_likelihood(t, lin_population, lin_probability, {"N0": 20, "b": 1}), \
                -4.944145552827423)

    def test_lin_likelihood_0(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertEqual(tree_likelihood(t, lin_population, lin_probability, {"N0": 1000, "b": 10}), \
                -22.358429151813432)

    def test_lin_likelihood_1(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertEqual(tree_likelihood(t, lin_population, lin_probability, {"N0": 2000, "b": 10}), \
                -25.171199217855392)

    def test_lin_likelihood_2(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertEqual(tree_likelihood(t, lin_population, lin_probability, {"N0": 1000, "b": 20}), \
                -22.262644483747312)

    def test_exp_likelihood_basic(self):
        t = TimeTree("((A:1, B:1):2, C:3);")
        self.assertEqual(tree_likelihood(t, exp_population, exp_probability, {"N0": 20, "r": 0.1}), \
                -4.768249652206723)

    def test_exp_likelihood_0(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertEqual(tree_likelihood(t, exp_population, exp_probability, {"N0": 1000, "r": 0.1}), \
                -21.540268162312763)

    def test_exp_likelihood_1(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertEqual(tree_likelihood(t, exp_population, exp_probability, {"N0": 2000, "r": 0.1}), \
                -24.308783956388865)

    def test_exp_likelihood_2(self):
        t = TimeTree("((A:1, B:1):2, ((C:0.7, D:0.7):1.3, E:2):1);")
        self.assertEqual(tree_likelihood(t, exp_population, exp_probability, {"N0": 1000, "r": 0.5}), \
                -17.916859396867185)


if __name__ == "__main__":
    unittest.main()

