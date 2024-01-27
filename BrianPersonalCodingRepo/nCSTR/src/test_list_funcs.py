import unittest
import list_funcs as lf

class TestArrayFunctions(unittest.TestCase):
    def test_array_funcs(self) -> None:
        self.assertEqual(lf.generate_list_from_number(1,0),[],"base case test")
        self.assertEqual(lf.generate_list_from_number(1,1),[1],"1 element test")
        self.assertEqual(lf.generate_list_from_number(2.3,3),[2.3,2.3,2.3],"1 element test")
    def test_generate_arg_list(self) -> None:
        self.assertEqual(lf.generate_arg_list([[]]), [], "base case test")
        self.assertEqual(lf.generate_arg_list([[1]]), [(1,)], "single list single entry test")
        self.assertEqual(lf.generate_arg_list([[1],[2],[3]]), [(1,2,3)], "multi list, single entry test")
        self.assertEqual(lf.generate_arg_list([[1,2,3],[1,2,3],[1,2,3]]), [(1,1,1),(2,2,2),(3,3,3)], "multi list, multi entry test")
if __name__ == '__main__':
    unittest.main()