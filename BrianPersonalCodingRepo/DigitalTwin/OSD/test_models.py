import unittest
import blender_model as bm
import feeder_model as fm
import monte_carlo as mc
from helper import listStrToFloat,parseMqttTopic,parseMqttPayload,createOuputTopic,topic_loc

class TestHelperFunctions(unittest.TestCase):

    def test_listStrToFloat(self) -> None:
        self.assertEqual(listStrToFloat(["1","2","3"]), [1,2,3])

    def test_parseMqttTopic(self) -> None:
        self.assertEqual(parseMqttTopic(""),[""])
        self.assertEqual(parseMqttTopic("ml/models/input"),["ml","models","input"])
        self.assertEqual(parseMqttTopic("ml/models/input")[1],"models")

    def test_parseMqttPayload(self) -> None:
        self.assertEqual(parseMqttPayload(b''),[""])
        self.assertEqual(parseMqttPayload(b'1,300,1000'),["1","300","1000"])

    def test_concatListOfString(self) -> None:
        self.assertEqual(createOuputTopic([]),"")
        self.assertEqual(createOuputTopic(["b"]),"b")
        self.assertEqual(createOuputTopic(["b","r","i","a","n"]),"b/r/i/a/n")
        self.assertEqual(createOuputTopic(["b","r","i","a","n"],"b","r"),"r/r/i/a/n")
        self.assertEqual(createOuputTopic(["ml","models","updateMass","input"],"input","output"),"ml/models/updateMass/output")
    
    def test_topic_loc(self) -> None:
        #self.assertEqual(topic_loc([],"brian"), False)
        self.assertEqual(topic_loc(["ml","models","updateMass","input"],"brian"), False)
        self.assertEqual(topic_loc(["ml"],"ml"), 0)
        self.assertEqual(topic_loc(["ml","models","updateMass","input"],"input"), 3)

class TestBlenderModel(unittest.TestCase):

    def test_tau(self) -> None:
        self.assertAlmostEqual(bm.tau(4.1, 0), 41000) # division by zero test
        self.assertAlmostEqual(bm.tau(4.1, 1000), .0041)  # normal test

    def test_flowOut(self) -> None:
        self.assertAlmostEqual(bm.flowOut(1000, 0, 4.1), 0)
        self.assertAlmostEqual(bm.flowOut(1000, 1001, 4.1), 4.104095904095904)

    def test_holdup(self) -> None:
        self.assertAlmostEqual(bm.holdup(1000, 0, 4.1), 4.1)
        self.assertAlmostEqual(bm.holdup(1000, 1001, 4.1), -0.004095904095904324)

    def test_updateMass(self) -> None:
        self.assertAlmostEqual(bm.updateMass(1000, 0, 4.1), 4.1) 
        self.assertAlmostEqual(bm.updateMass(1000, 1001, 4.1), 1000.995904095904)
         
class TestFeederModel(unittest.TestCase):

    def test_sat_density(self) -> None:
        with self.assertRaises(Exception):
            fm.sat_density(0)
        with self.assertRaises(Exception):
            fm.sat_density(-1)
        self.assertAlmostEqual(fm.sat_density(.26), 0.15967308385878232)

    SD0 = fm.sat_density(.26)
    def test_sat_feed_factor(self) -> None:
        self.assertAlmostEqual(fm.sat_feed_factor(self.SD0, -1), 0)
        self.assertAlmostEqual(fm.sat_feed_factor(self.SD0, 0), 0)
        self.assertAlmostEqual(fm.sat_feed_factor(self.SD0, 100), 15.967308385878232)

    def test_beta(self) -> None:
        with self.assertRaises(Exception):
            fm.beta(0)
        with self.assertRaises(Exception):
            fm.beta(-1)
        self.assertAlmostEqual(fm.beta(1.2), 1.2680000000000007)

    SFF0 = fm.sat_feed_factor(SD0, 100)
    def test_minFeedFactor(self) -> None:
        self.assertAlmostEqual(fm.min_feed_factor(self.SFF0), 5.416156394777305)

    
    MFF0 = fm.min_feed_factor(.26, 100)
    B0 = fm.beta(1.2)
    def test_app_feed_factor(self) -> None:
        self.assertAlmostEqual(fm.apparent_feed_factor(self.SFF0,self.MFF0,self.B0,500), 15.967308385878232)
        self.assertAlmostEqual(fm.apparent_feed_factor(self.SFF0,self.MFF0,self.B0,0),14.967308385878232)
        self.assertAlmostEqual(fm.apparent_feed_factor(self.SFF0,self.MFF0,self.B0,-100000),14.967308385878232)
        self.assertAlmostEqual(fm.apparent_feed_factor(self.SFF0,self.MFF0,self.B0,1000000),15.967308385878232)

    FR0: float = fm.apparent_feed_factor(SFF0,MFF0,B0,500)
    FR1: float = fm.apparent_feed_factor(SFF0,MFF0,B0,0)
    FR2: float = fm.apparent_feed_factor(SFF0,MFF0,B0,1000000)
    def test_feed_rate(self) -> None:
        self.assertAlmostEqual(fm.feed_rate(self.FR0,100), 1596.7308385878232)
        self.assertAlmostEqual(fm.feed_rate(self.FR1,100), 1496.7308385878232)
        self.assertAlmostEqual(fm.feed_rate(self.FR2,100), 1596.7308385878232)

class TestMonteCarloTest(unittest.TestCase):
    def test_monte_carlo_single_function(self) -> None:
        self.assertEqual(mc.monte_carlo(fm.sat_density, []), [], "base case (0 simulation) test")
        self.assertEqual(mc.monte_carlo(fm.sat_density, [(.25,)]), [fm.sat_density(.25)], "single entry case test")
        self.assertEqual(mc.monte_carlo(fm.sat_density, [(.25,),(.20,),(.30,)]), [fm.sat_density(.25), fm.sat_density(.20), fm.sat_density(.30)], "three entry case test")
        self.assertEqual(mc.monte_carlo(fm.sat_feed_factor, [(.25, 1.0),(.25, 1.0),(.25, 1.0)]), [fm.sat_feed_factor(.25, 1), fm.sat_feed_factor(.25, 1), fm.sat_feed_factor(.25, 1)], "multi argument test")
    def test_mc_arg(self) -> None:
        self.assertEqual(mc.mc_arg([[]]), [], "base case test")
        self.assertEqual(mc.mc_arg([[1]]), [(1,)], "single list single entry test")
        self.assertEqual(mc.mc_arg([[1],[2],[3]]), [(1,2,3)], "multi list, single entry test")
        self.assertEqual(mc.mc_arg([[1,2,3],[1,2,3],[1,2,3]]), [(1,1,1),(2,2,2),(3,3,3)], "multi list, multi entry test")
    def test_rv_prob(self) -> None:
        with self.assertRaises(Exception): # zero answers - base case 
            mc.rv_prob([[]],[(0,0)])
        self.assertEqual(mc.rv_prob([[1]],[(0,1,2),(0,4,8)]), [[0,1],[0,1]], "list size mismatch (more bin tuples) - single column, single row, 2 bins test")
        self.assertEqual(mc.rv_prob([[1],[1],[1]],[(0,1,2)]), [[0,0,0,0,1,1,1,1],
                                                               [0,0,1,1,0,0,1,1],
                                                               [0,1,0,1,0,1,0,1],
                                                               [0,0,0,0,0,0,0,1]], "list size mismatch (more lists) test")
        self.assertEqual(mc.rv_prob([[1],[1],[1]],[(0,1,2),(1,2,3)]), [[0,0,0,0,1,1,1,1],
                                                                       [1,1,2,2,1,1,2,2],
                                                                       [1,2,1,2,1,2,1,2],
                                                                       [0,0,0,0,1,0,0,0]], "list size mismatch (more lists, bin > 1) test")
        with self.assertRaises(Exception): # zero answers - ends with base case
            mc.rv_prob([[1]],[(0,1)])
        self.assertEqual(mc.rv_prob([[0]],[(0,1)]), [[0],[1]], "single column, single input, 1 bin, border case error test")
        self.assertEqual(mc.rv_prob([[1,2,2.9,-1,0]],[(0,1,2,3)]), [[0,1,2],[.25,.25,.5]], "single column, 3 input, 3 bins, 1 sample out of range test")
        self.assertEqual(mc.rv_prob([[1],[2],[3]],[(0,1,2),(0,3,6),(0,2,4)]), [[0,0,0,0,1,1,1,1],
                                                                               [0,0,3,3,0,0,3,3],
                                                                               [0,2,0,2,0,2,0,2],
                                                                               [0,0,0,0,0,2,0,0]], "3 column, single input, 2,2,2 bins test")
        self.assertEqual(mc.rv_prob([[1,0,1.5,1],[1.9,0,.5,1],[2.9,0,2,1]],[(0,1,2),(0,1,2),(0,1,2,3)]), [[0,0,0,0,0,0,1,1,1,1,1,1], # (0,1,2)
                                                                                                          [0,0,0,1,1,1,0,0,0,1,1,1], # (0,1,2)
                                                                                                          [0,1,2,0,1,2,0,1,2,0,1,2], # (0,1,2,3)
                                                                                                          [.25,0,0,0,0,0,0,0,.25,0,.25,.25]], "3 column, two input, 2,2,3 bins test")

if __name__ == '__main__':
    unittest.main()